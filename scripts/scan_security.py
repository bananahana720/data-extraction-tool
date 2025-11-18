#!/usr/bin/env python3
"""
Security Scanner

Comprehensive security scanning including hardcoded secrets detection,
vulnerability checking, permission validation, and security reporting.

Usage:
    python scripts/scan_security.py                    # Full security scan
    python scripts/scan_security.py --secrets-only     # Only scan for secrets
    python scripts/scan_security.py --deps-only        # Only check dependencies
    python scripts/scan_security.py --history          # Scan git history
    python scripts/scan_security.py --pre-commit       # Pre-commit hook mode
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set

import structlog
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text

# Try to import optional dependencies
try:
    import git

    HAS_GITPYTHON = True
except ImportError:
    HAS_GITPYTHON = False

try:
    from safety import check as safety_check

    HAS_SAFETY = True
except ImportError:
    HAS_SAFETY = False

# tomli not currently used, but kept for future TOML config support
HAS_TOMLI = False

try:
    from bandit.core import config as bandit_config
    from bandit.core import manager as bandit_manager

    HAS_BANDIT = True
except ImportError:
    HAS_BANDIT = False

# Configure structured logging
logger = structlog.get_logger()
console = Console()

# Constants
PROJECT_ROOT = Path(__file__).parent.parent
SCANIGNORE_FILE = PROJECT_ROOT / ".scanignore"
SECURITY_CONFIG_FILE = PROJECT_ROOT / ".security.yaml"
REPORTS_DIR = PROJECT_ROOT / "docs" / "security-reports"
CACHE_DIR = PROJECT_ROOT / ".cache" / "security"

# Severity levels
SEVERITY_LEVELS = {
    "CRITICAL": "red",
    "HIGH": "bright_red",
    "MEDIUM": "yellow",
    "LOW": "bright_yellow",
    "INFO": "cyan",
}

# Secret patterns to detect
SECRET_PATTERNS = {
    "aws_access_key": {
        "pattern": r"AKIA[0-9A-Z]{16}",
        "severity": "CRITICAL",
        "description": "AWS Access Key ID",
    },
    "aws_secret_key": {
        "pattern": r"aws[_\-]?secret[_\-]?access[_\-]?key\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}['\"]?",
        "severity": "CRITICAL",
        "description": "AWS Secret Access Key",
    },
    "github_token": {
        "pattern": r"gh[ps]_[A-Za-z0-9]{36}",
        "severity": "CRITICAL",
        "description": "GitHub Personal Access Token",
    },
    "api_key_generic": {
        "pattern": r"(?i)(api[_\-]?key|apikey|api_secret)['\"]?\s*[:=]\s*['\"]?[a-zA-Z0-9\-_]{32,}['\"]?",
        "severity": "HIGH",
        "description": "Generic API Key",
    },
    "private_key": {
        "pattern": r"-----BEGIN\s+(RSA|DSA|EC|OPENSSH|PGP)\s+PRIVATE\s+KEY-----",
        "severity": "CRITICAL",
        "description": "Private Cryptographic Key",
    },
    "jwt_token": {
        "pattern": r"eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}",
        "severity": "HIGH",
        "description": "JWT Token",
    },
    "slack_webhook": {
        "pattern": r"https://hooks\.slack\.com/services/T[A-Z0-9]{8}/B[A-Z0-9]{8}/[A-Za-z0-9]{24}",
        "severity": "MEDIUM",
        "description": "Slack Webhook URL",
    },
    "database_connection": {
        "pattern": r"(mongodb|postgres|postgresql|mysql|mssql|redis)://[^/\s]+:[^@/\s]+@[^/\s]+",
        "severity": "CRITICAL",
        "description": "Database Connection String with Credentials",
    },
    "password_in_url": {
        "pattern": r"://[^/\s]+:[^@/\s]+@",
        "severity": "HIGH",
        "description": "Password in URL",
    },
    "bearer_token": {
        "pattern": r"(?i)bearer\s+[a-z0-9\-_.]{20,}",
        "severity": "HIGH",
        "description": "Bearer Token",
    },
}

# File extensions to scan
SCAN_EXTENSIONS = {
    ".py",
    ".js",
    ".ts",
    ".jsx",
    ".tsx",
    ".java",
    ".go",
    ".rs",
    ".cpp",
    ".c",
    ".h",
    ".hpp",
    ".cs",
    ".rb",
    ".php",
    ".swift",
    ".kt",
    ".scala",
    ".sh",
    ".bash",
    ".zsh",
    ".fish",
    ".ps1",
    ".bat",
    ".cmd",
    ".yml",
    ".yaml",
    ".json",
    ".xml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".config",
    ".env",
    ".properties",
    ".sql",
    ".md",
    ".txt",
    ".dockerfile",
    "Dockerfile",
}

# Sensitive file patterns
SENSITIVE_FILES = {
    ".env": {"severity": "HIGH", "permissions": 0o600},
    ".env.*": {"severity": "HIGH", "permissions": 0o600},
    "*.key": {"severity": "CRITICAL", "permissions": 0o600},
    "*.pem": {"severity": "CRITICAL", "permissions": 0o600},
    "*.p12": {"severity": "CRITICAL", "permissions": 0o600},
    "*.pfx": {"severity": "CRITICAL", "permissions": 0o600},
    "id_rsa*": {"severity": "CRITICAL", "permissions": 0o600},
    "id_dsa*": {"severity": "CRITICAL", "permissions": 0o600},
    "id_ecdsa*": {"severity": "CRITICAL", "permissions": 0o600},
    "id_ed25519*": {"severity": "CRITICAL", "permissions": 0o600},
    ".ssh/*": {"severity": "HIGH", "permissions": 0o600},
    "credentials*": {"severity": "HIGH", "permissions": 0o600},
    ".aws/credentials": {"severity": "CRITICAL", "permissions": 0o600},
    ".netrc": {"severity": "HIGH", "permissions": 0o600},
}


@dataclass
class SecurityFinding:
    """Represents a security finding."""

    finding_type: str  # "secret", "vulnerability", "permission"
    severity: str
    description: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    matched_pattern: Optional[str] = None
    remediation: Optional[str] = None
    false_positive: bool = False
    commit_hash: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None


class SecurityScanner:
    """Comprehensive security scanner for the codebase."""

    def __init__(self, project_root: Path = PROJECT_ROOT):
        """Initialize the security scanner."""
        self.project_root = project_root
        self.findings: List[SecurityFinding] = []
        self.scan_ignore_patterns: Set[str] = set()
        self.false_positive_hashes: Set[str] = set()
        self.stats = {
            "files_scanned": 0,
            "secrets_found": 0,
            "vulnerabilities_found": 0,
            "permission_issues": 0,
            "total_findings": 0,
        }

        # Load .scanignore patterns
        self._load_scan_ignore()

        # Load false positive cache
        self._load_false_positives()

        logger.info("initialized_security_scanner", project_root=str(project_root))

    def _load_scan_ignore(self) -> None:
        """Load patterns from .scanignore file."""
        if SCANIGNORE_FILE.exists():
            with open(SCANIGNORE_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        self.scan_ignore_patterns.add(line)
            logger.info("loaded_scanignore", patterns=len(self.scan_ignore_patterns))

    def _load_false_positives(self) -> None:
        """Load false positive hashes from cache."""
        cache_file = CACHE_DIR / "false_positives.json"
        if cache_file.exists():
            try:
                with open(cache_file, "r") as f:
                    data = json.load(f)
                    self.false_positive_hashes = set(data.get("hashes", []))
                logger.info("loaded_false_positives", count=len(self.false_positive_hashes))
            except Exception as e:
                logger.warning("failed_to_load_false_positives", error=str(e))

    def _save_false_positives(self) -> None:
        """Save false positive hashes to cache."""
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache_file = CACHE_DIR / "false_positives.json"
        try:
            with open(cache_file, "w") as f:
                json.dump({"hashes": list(self.false_positive_hashes)}, f)
            logger.info("saved_false_positives", count=len(self.false_positive_hashes))
        except Exception as e:
            logger.error("failed_to_save_false_positives", error=str(e))

    def _should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned based on ignore patterns."""
        relative_path = file_path.relative_to(self.project_root)
        path_str = str(relative_path)

        # Check against ignore patterns
        for pattern in self.scan_ignore_patterns:
            if pattern in path_str or path_str.startswith(pattern):
                return False

        # Check file extension
        if file_path.suffix not in SCAN_EXTENSIONS and file_path.name not in ["Dockerfile"]:
            return False

        # Skip common directories
        skip_dirs = {
            ".git",
            ".venv",
            "venv",
            "node_modules",
            "__pycache__",
            ".pytest_cache",
            ".mypy_cache",
            "dist",
            "build",
            ".tox",
        }
        for parent in file_path.parents:
            if parent.name in skip_dirs:
                return False

        return True

    def scan_secrets(self, use_gitleaks: bool = True) -> List[SecurityFinding]:
        """Scan for hardcoded secrets and credentials."""
        findings = []

        if use_gitleaks and self._is_gitleaks_available():
            # Use GitLeaks for comprehensive scanning
            findings.extend(self._scan_with_gitleaks())

        # Also run our custom pattern matching
        findings.extend(self._scan_with_patterns())

        self.findings.extend(findings)
        self.stats["secrets_found"] = len(findings)
        return findings

    def _is_gitleaks_available(self) -> bool:
        """Check if GitLeaks is installed and available."""
        try:
            result = subprocess.run(["gitleaks", "version"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            logger.warning("gitleaks_not_installed")
            return False

    def _scan_with_gitleaks(self) -> List[SecurityFinding]:
        """Run GitLeaks scanner."""
        findings = []

        try:
            # Run gitleaks with JSON output
            cmd = [
                "gitleaks",
                "detect",
                "--source",
                str(self.project_root),
                "--report-format",
                "json",
                "--report-path",
                "/tmp/gitleaks-report.json",
                "--no-git",
            ]

            subprocess.run(cmd, capture_output=True, text=True)

            # Parse results
            if Path("/tmp/gitleaks-report.json").exists():
                with open("/tmp/gitleaks-report.json", "r") as f:
                    gitleaks_findings = json.load(f)

                for finding in gitleaks_findings:
                    findings.append(
                        SecurityFinding(
                            finding_type="secret",
                            severity="HIGH",
                            description=finding.get("Description", "Secret detected"),
                            file_path=finding.get("File"),
                            line_number=finding.get("StartLine"),
                            matched_pattern=finding.get("Match"),
                            remediation="Remove or encrypt this secret and rotate credentials",
                        )
                    )

        except Exception as e:
            logger.error("gitleaks_scan_failed", error=str(e))

        return findings

    def _scan_with_patterns(self) -> List[SecurityFinding]:
        """Scan files using custom regex patterns."""
        findings = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console,
        ) as progress:

            # Collect files to scan
            files_to_scan = []
            for root, _, files in os.walk(self.project_root):
                for file_name in files:
                    file_path = Path(root) / file_name
                    if self._should_scan_file(file_path):
                        files_to_scan.append(file_path)

            task = progress.add_task("Scanning for secrets...", total=len(files_to_scan))

            for file_path in files_to_scan:
                self.stats["files_scanned"] += 1
                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    for pattern_name, pattern_info in SECRET_PATTERNS.items():
                        regex = re.compile(pattern_info["pattern"], re.IGNORECASE | re.MULTILINE)
                        for match in regex.finditer(content):
                            # Calculate line number
                            line_number = content[: match.start()].count("\n") + 1

                            # Generate hash for deduplication
                            finding_hash = hashlib.md5(
                                f"{file_path}:{line_number}:{match.group()}".encode()
                            ).hexdigest()

                            # Skip if marked as false positive
                            if finding_hash in self.false_positive_hashes:
                                continue

                            findings.append(
                                SecurityFinding(
                                    finding_type="secret",
                                    severity=pattern_info["severity"],
                                    description=pattern_info["description"],
                                    file_path=str(file_path.relative_to(self.project_root)),
                                    line_number=line_number,
                                    matched_pattern=(
                                        match.group()[:50] + "..."
                                        if len(match.group()) > 50
                                        else match.group()
                                    ),
                                    remediation=self._get_remediation(pattern_name),
                                )
                            )

                except Exception as e:
                    logger.warning("failed_to_scan_file", file=str(file_path), error=str(e))

                progress.update(task, advance=1)

        return findings

    def _get_remediation(self, pattern_type: str) -> str:
        """Get remediation advice for a pattern type."""
        remediations = {
            "aws_access_key": "Rotate AWS credentials immediately and use IAM roles or AWS Secrets Manager",
            "github_token": "Revoke token in GitHub settings and use environment variables",
            "private_key": "Remove key from repository, regenerate if compromised, use key management service",
            "database_connection": "Use environment variables or secrets management for connection strings",
            "jwt_token": "Tokens should not be hardcoded; implement proper token management",
        }
        return remediations.get(
            pattern_type,
            "Remove hardcoded secret and use environment variables or secrets management",
        )

    def scan_dependencies(self) -> List[SecurityFinding]:
        """Check for vulnerable dependencies."""
        findings = []

        # Check Python dependencies
        if HAS_SAFETY:
            findings.extend(self._scan_python_deps_safety())
        else:
            findings.extend(self._scan_python_deps_pip_audit())

        # Check JavaScript dependencies if package.json exists
        if (self.project_root / "package.json").exists():
            findings.extend(self._scan_npm_deps())

        self.findings.extend(findings)
        self.stats["vulnerabilities_found"] = len(findings)
        return findings

    def _scan_python_deps_safety(self) -> List[SecurityFinding]:
        """Scan Python dependencies using safety."""
        findings = []

        try:
            # Get installed packages
            result = subprocess.run(
                ["pip", "list", "--format", "json"], capture_output=True, text=True
            )

            if result.returncode == 0:
                packages = json.loads(result.stdout)

                # Check with safety
                for vuln in safety_check.check(packages):
                    findings.append(
                        SecurityFinding(
                            finding_type="vulnerability",
                            severity=self._map_cvss_to_severity(vuln.get("cvss", 0)),
                            description=f"{vuln['package']} {vuln['installed_version']}: {vuln['description']}",
                            remediation=f"Update to {vuln['safe_version']} or later",
                        )
                    )

        except Exception as e:
            logger.error("safety_scan_failed", error=str(e))

        return findings

    def _scan_python_deps_pip_audit(self) -> List[SecurityFinding]:
        """Scan Python dependencies using pip-audit."""
        findings = []

        try:
            # Check if pip-audit is available
            result = subprocess.run(
                ["pip-audit", "--format", "json"], capture_output=True, text=True
            )

            if result.returncode == 0:
                audit_results = json.loads(result.stdout)

                for vuln in audit_results.get("vulnerabilities", []):
                    findings.append(
                        SecurityFinding(
                            finding_type="vulnerability",
                            severity=self._map_cvss_to_severity(vuln.get("cvss_score", 0)),
                            description=f"{vuln['name']} {vuln['version']}: {vuln['description']}",
                            remediation=f"Update to {vuln.get('fixed_version', 'latest secure version')}",
                        )
                    )

        except FileNotFoundError:
            logger.info("pip_audit_not_installed")
        except Exception as e:
            logger.error("pip_audit_scan_failed", error=str(e))

        return findings

    def _scan_npm_deps(self) -> List[SecurityFinding]:
        """Scan npm dependencies for vulnerabilities."""
        findings = []

        try:
            result = subprocess.run(
                ["npm", "audit", "--json"], cwd=self.project_root, capture_output=True, text=True
            )

            if result.stdout:
                audit_data = json.loads(result.stdout)

                for advisory_id, advisory in audit_data.get("advisories", {}).items():
                    findings.append(
                        SecurityFinding(
                            finding_type="vulnerability",
                            severity=advisory["severity"].upper(),
                            description=f"{advisory['module_name']}: {advisory['title']}",
                            remediation=advisory.get("recommendation", "Update to secure version"),
                        )
                    )

        except FileNotFoundError:
            logger.info("npm_not_available")
        except Exception as e:
            logger.error("npm_audit_failed", error=str(e))

        return findings

    def _map_cvss_to_severity(self, cvss_score: float) -> str:
        """Map CVSS score to severity level."""
        if cvss_score >= 9.0:
            return "CRITICAL"
        elif cvss_score >= 7.0:
            return "HIGH"
        elif cvss_score >= 4.0:
            return "MEDIUM"
        else:
            return "LOW"

    def scan_permissions(self) -> List[SecurityFinding]:
        """Validate file permissions for sensitive files."""
        findings = []

        if os.name != "posix":
            logger.info("permission_scan_skipped", reason="Not a POSIX system")
            return findings

        for pattern, info in SENSITIVE_FILES.items():
            for file_path in self.project_root.glob(pattern):
                if not file_path.is_file():
                    continue

                # Get current permissions
                stat_info = file_path.stat()
                current_mode = stat_info.st_mode & 0o777
                expected_mode = info["permissions"]

                if current_mode > expected_mode:  # More permissive than expected
                    findings.append(
                        SecurityFinding(
                            finding_type="permission",
                            severity=info["severity"],
                            description="Overly permissive file permissions",
                            file_path=str(file_path.relative_to(self.project_root)),
                            remediation=f"Change permissions to {oct(expected_mode)} (chmod {oct(expected_mode)[2:]} {file_path})",
                        )
                    )

        self.findings.extend(findings)
        self.stats["permission_issues"] = len(findings)
        return findings

    def scan_with_sast(self) -> List[SecurityFinding]:
        """Integrate with Static Application Security Testing (SAST) tools like Bandit."""
        findings = []

        if HAS_BANDIT:
            findings.extend(self._scan_with_bandit())
        else:
            logger.warning("bandit_not_installed", message="Install bandit for SAST scanning")

        # Check for other SAST tools in the future
        # Could add support for:
        # - semgrep
        # - pylint security checks
        # - flake8-bandit

        self.findings.extend(findings)
        self.stats["sast_findings"] = len(findings)
        return findings

    def _scan_with_bandit(self) -> List[SecurityFinding]:
        """Run Bandit security linter."""
        findings = []

        try:
            # Configure Bandit
            conf = bandit_config.BanditConfig()
            manager = bandit_manager.BanditManager(conf, "file")

            # Discover Python files to scan
            python_files = []
            for ext in [".py"]:
                for file_path in self.project_root.rglob(f"*{ext}"):
                    if self._should_scan_file(file_path):
                        python_files.append(str(file_path))

            if not python_files:
                logger.info("no_python_files_to_scan")
                return findings

            # Run Bandit on discovered files
            manager.discover_files(python_files)
            manager.run_tests()

            # Convert Bandit results to our format
            for issue in manager.get_issue_list():
                severity_map = {
                    "HIGH": "HIGH",
                    "MEDIUM": "MEDIUM",
                    "LOW": "LOW",
                    "UNDEFINED": "INFO",
                }

                findings.append(
                    SecurityFinding(
                        finding_type="sast",
                        severity=severity_map.get(issue.severity, "INFO"),
                        description=f"{issue.test}: {issue.text}",
                        file_path=issue.fname,
                        line_number=issue.lineno,
                        matched_pattern=issue.code if hasattr(issue, "code") else None,
                        remediation=f"Review and fix: {issue.test_id} - {issue.issue_text}",
                    )
                )

            logger.info("bandit_scan_completed", findings_count=len(findings))

        except Exception as e:
            logger.error("bandit_scan_failed", error=str(e))

            # Fallback: Try running bandit as CLI command
            try:
                result = subprocess.run(
                    ["bandit", "-r", str(self.project_root), "-f", "json"],
                    capture_output=True,
                    text=True,
                )

                if result.stdout:
                    bandit_output = json.loads(result.stdout)
                    for issue in bandit_output.get("results", []):
                        findings.append(
                            SecurityFinding(
                                finding_type="sast",
                                severity=issue.get("issue_severity", "INFO"),
                                description=f"{issue.get('test_name', 'Unknown')}: {issue.get('issue_text', 'Security issue')}",
                                file_path=issue.get("filename"),
                                line_number=issue.get("line_number"),
                                remediation=f"Fix issue: {issue.get('test_id', 'Unknown')}",
                            )
                        )
                    logger.info("bandit_cli_scan_completed", findings_count=len(findings))

            except Exception as cli_error:
                logger.error("bandit_cli_scan_failed", error=str(cli_error))

        return findings

    def scan_git_history(self, max_commits: int = 100) -> List[SecurityFinding]:
        """Scan git history for previously committed secrets."""
        findings = []

        if not HAS_GITPYTHON:
            logger.warning("git_history_scan_skipped", reason="GitPython not installed")
            return findings

        try:
            repo = git.Repo(self.project_root)

            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
            ) as progress:

                progress.add_task(f"Scanning last {max_commits} commits...")

                for commit in list(repo.iter_commits(max_count=max_commits)):
                    # Check commit message
                    for pattern_name, pattern_info in SECRET_PATTERNS.items():
                        regex = re.compile(pattern_info["pattern"], re.IGNORECASE)
                        if regex.search(commit.message):
                            findings.append(
                                SecurityFinding(
                                    finding_type="secret",
                                    severity=pattern_info["severity"],
                                    description=f"{pattern_info['description']} in commit message",
                                    commit_hash=commit.hexsha[:8],
                                    author=commit.author.email,
                                    date=datetime.fromtimestamp(commit.committed_date).isoformat(),
                                    remediation="Secret found in commit history - consider rewriting history if not pushed",
                                )
                            )

                    # Check diff
                    if commit.parents:
                        diffs = commit.diff(commit.parents[0], create_patch=True)
                        for diff in diffs:
                            if diff.diff:
                                diff_text = diff.diff.decode("utf-8", errors="ignore")
                                for pattern_name, pattern_info in SECRET_PATTERNS.items():
                                    regex = re.compile(pattern_info["pattern"], re.IGNORECASE)
                                    if regex.search(diff_text):
                                        findings.append(
                                            SecurityFinding(
                                                finding_type="secret",
                                                severity=pattern_info["severity"],
                                                description=f"{pattern_info['description']} in commit diff",
                                                file_path=diff.a_path or diff.b_path,
                                                commit_hash=commit.hexsha[:8],
                                                author=commit.author.email,
                                                date=datetime.fromtimestamp(
                                                    commit.committed_date
                                                ).isoformat(),
                                                remediation="Secret in git history - rotate credentials and consider cleaning history",
                                            )
                                        )

        except Exception as e:
            logger.error("git_history_scan_failed", error=str(e))

        return findings

    def generate_report(
        self, output_format: str = "markdown", output_file: Optional[Path] = None
    ) -> str:
        """Generate comprehensive security report."""
        # Calculate statistics
        self.stats["total_findings"] = len(self.findings)

        # Group findings by severity
        findings_by_severity = {}
        for severity in SEVERITY_LEVELS.keys():
            findings_by_severity[severity] = [f for f in self.findings if f.severity == severity]

        # Generate report
        if output_format == "markdown":
            report = self._generate_markdown_report(findings_by_severity)
        elif output_format == "json":
            report = self._generate_json_report(findings_by_severity)
        else:
            report = self._generate_text_report(findings_by_severity)

        # Save report
        if output_file:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(report)
            logger.info("saved_security_report", file=str(output_file))

        return report

    def _generate_markdown_report(self, findings_by_severity: Dict) -> str:
        """Generate markdown format security report."""
        report = f"""# Security Scan Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Project:** {self.project_root.name}

## Summary

- **Files Scanned:** {self.stats['files_scanned']}
- **Total Findings:** {self.stats['total_findings']}
- **Secrets Found:** {self.stats['secrets_found']}
- **Vulnerabilities:** {self.stats['vulnerabilities_found']}
- **Permission Issues:** {self.stats['permission_issues']}

## Findings by Severity

"""

        for severity, findings in findings_by_severity.items():
            if findings:
                report += f"### {severity} ({len(findings)} findings)\n\n"

                for finding in findings[:10]:  # Limit to first 10 per severity
                    report += f"**Type:** {finding.finding_type}\n"
                    report += f"**Description:** {finding.description}\n"
                    if finding.file_path:
                        report += f"**File:** `{finding.file_path}`"
                        if finding.line_number:
                            report += f" (line {finding.line_number})"
                        report += "\n"
                    if finding.matched_pattern:
                        report += f"**Match:** `{finding.matched_pattern}`\n"
                    if finding.commit_hash:
                        report += f"**Commit:** {finding.commit_hash} by {finding.author} on {finding.date}\n"
                    if finding.remediation:
                        report += f"**Remediation:** {finding.remediation}\n"
                    report += "\n---\n\n"

                if len(findings) > 10:
                    report += f"*... and {len(findings) - 10} more {severity} findings*\n\n"

        report += """
## Recommendations

1. **Immediate Actions:**
   - Rotate any exposed credentials immediately
   - Remove secrets from source code
   - Update vulnerable dependencies

2. **Preventive Measures:**
   - Use environment variables for sensitive configuration
   - Implement pre-commit hooks to prevent secret commits
   - Regular dependency updates and security scanning
   - Use secrets management tools (e.g., HashiCorp Vault, AWS Secrets Manager)

3. **Best Practices:**
   - Never commit credentials, even in development
   - Use .gitignore for sensitive files
   - Implement least-privilege file permissions
   - Regular security audits and training
"""

        return report

    def _generate_json_report(self, findings_by_severity: Dict) -> str:
        """Generate JSON format security report."""
        report_data = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "project": self.project_root.name,
                "scanner_version": "1.0.0",
            },
            "statistics": self.stats,
            "findings": [],
        }

        for finding in self.findings:
            report_data["findings"].append(
                {
                    "type": finding.finding_type,
                    "severity": finding.severity,
                    "description": finding.description,
                    "file_path": finding.file_path,
                    "line_number": finding.line_number,
                    "matched_pattern": finding.matched_pattern,
                    "remediation": finding.remediation,
                    "commit_hash": finding.commit_hash,
                    "author": finding.author,
                    "date": finding.date,
                    "false_positive": finding.false_positive,
                }
            )

        return json.dumps(report_data, indent=2)

    def _generate_text_report(self, findings_by_severity: Dict) -> str:
        """Generate plain text report."""
        lines = []
        lines.append("SECURITY SCAN REPORT")
        lines.append("=" * 50)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Total Findings: {self.stats['total_findings']}")
        lines.append("")

        for severity, findings in findings_by_severity.items():
            if findings:
                lines.append(f"{severity}: {len(findings)} findings")
                for finding in findings[:5]:
                    lines.append(f"  - {finding.description}")
                    if finding.file_path:
                        lines.append(f"    File: {finding.file_path}")
                lines.append("")

        return "\n".join(lines)

    def display_findings(self) -> None:
        """Display findings in the console."""
        if not self.findings:
            console.print("[green]✓ No security issues found![/green]")
            return

        # Group by severity
        findings_by_severity = {}
        for severity in SEVERITY_LEVELS.keys():
            findings_by_severity[severity] = [f for f in self.findings if f.severity == severity]

        # Display summary
        summary = f"""[bold]Security Scan Results[/bold]

Total Findings: [bold red]{self.stats['total_findings']}[/bold red]
Files Scanned: {self.stats['files_scanned']}

Breakdown by Type:
  • Secrets: {self.stats['secrets_found']}
  • Vulnerabilities: {self.stats['vulnerabilities_found']}
  • Permissions: {self.stats['permission_issues']}"""

        console.print(Panel(summary, title="🔒 Security Summary", border_style="red"))

        # Display findings table
        if self.findings:
            table = Table(title="Security Findings", box=box.ROUNDED)
            table.add_column("Severity", style="bold")
            table.add_column("Type")
            table.add_column("Description")
            table.add_column("Location")

            # Show top findings only
            for finding in self.findings[:20]:
                severity_style = SEVERITY_LEVELS.get(finding.severity, "white")
                location = finding.file_path or "N/A"
                if finding.line_number:
                    location += f":{finding.line_number}"

                table.add_row(
                    Text(finding.severity, style=severity_style),
                    finding.finding_type,
                    (
                        finding.description[:60] + "..."
                        if len(finding.description) > 60
                        else finding.description
                    ),
                    location,
                )

            console.print("\n")
            console.print(table)

            if len(self.findings) > 20:
                console.print(f"\n[dim]... and {len(self.findings) - 20} more findings[/dim]")


def main():
    """Main entry point for security scanner."""
    parser = argparse.ArgumentParser(description="Security Scanner")
    parser.add_argument("--secrets-only", action="store_true", help="Only scan for secrets")
    parser.add_argument("--deps-only", action="store_true", help="Only check dependencies")
    parser.add_argument(
        "--permissions-only", action="store_true", help="Only check file permissions"
    )
    parser.add_argument("--sast-only", action="store_true", help="Only run SAST analysis")
    parser.add_argument("--history", action="store_true", help="Scan git history for secrets")
    parser.add_argument(
        "--max-commits", type=int, default=100, help="Maximum commits to scan in history"
    )
    parser.add_argument(
        "--format", choices=["markdown", "json", "text"], default="markdown", help="Report format"
    )
    parser.add_argument("--output", type=Path, help="Output file for report")
    parser.add_argument(
        "--pre-commit", action="store_true", help="Pre-commit hook mode (fail on findings)"
    )
    parser.add_argument(
        "--use-gitleaks", action="store_true", default=True, help="Use GitLeaks if available"
    )

    args = parser.parse_args()

    scanner = SecurityScanner()

    try:
        # Run selected scans
        if args.secrets_only:
            scanner.scan_secrets(use_gitleaks=args.use_gitleaks)
        elif args.deps_only:
            scanner.scan_dependencies()
        elif args.permissions_only:
            scanner.scan_permissions()
        elif args.sast_only:
            scanner.scan_with_sast()
        elif args.history:
            scanner.scan_git_history(max_commits=args.max_commits)
        else:
            # Run all scans
            with console.status("[bold green]Running security scans...") as status:
                status.update("Scanning for secrets...")
                scanner.scan_secrets(use_gitleaks=args.use_gitleaks)

                status.update("Checking dependencies...")
                scanner.scan_dependencies()

                status.update("Validating permissions...")
                scanner.scan_permissions()

                status.update("Running SAST analysis...")
                scanner.scan_with_sast()

        # Display results
        scanner.display_findings()

        # Generate report if requested
        if args.output or args.format != "markdown":
            output_file = args.output
            if not output_file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                ext = "json" if args.format == "json" else "md"
                output_file = REPORTS_DIR / f"security_report_{timestamp}.{ext}"

            scanner.generate_report(args.format, output_file)
            console.print(f"\n[green]Report saved to: {output_file}[/green]")

        # Exit with error code if findings in pre-commit mode
        if args.pre_commit and scanner.findings:
            critical_or_high = [f for f in scanner.findings if f.severity in ["CRITICAL", "HIGH"]]
            if critical_or_high:
                console.print(
                    "\n[red]❌ Pre-commit check failed: Critical/High security issues found[/red]"
                )
                sys.exit(1)

        # Success message
        if not scanner.findings:
            console.print(
                "\n[green]✓ Security scan completed successfully with no findings[/green]"
            )

    except Exception as e:
        console.print(f"[red]Error during security scan: {e}[/red]")
        logger.exception("security_scan_error")
        sys.exit(1)


if __name__ == "__main__":
    main()
