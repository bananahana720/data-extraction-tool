#!/usr/bin/env python3
"""
Story Template Generator

Generates standardized story templates with acceptance criteria tables,
wiring checklists, and submission summaries for the Data Extraction Tool project.

Usage:
    python scripts/generate_story_template.py --story-number 4.1 --epic 4 --title "Semantic Analysis Foundation"
"""

import argparse
import sys
from datetime import datetime
from pathlib import Path

import structlog
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

# Configure structured logging
logger = structlog.get_logger()

# Constants
TEMPLATE_DIR = Path(__file__).parent / "templates"
OUTPUT_DIR = Path(__file__).parent.parent / "docs" / "stories"
DEFAULT_OWNER = "Team"
DEFAULT_ESTIMATE = 4


class StoryTemplateGenerator:
    """Generates story markdown files from Jinja2 templates."""

    def __init__(self, template_dir: Path = TEMPLATE_DIR):
        """
        Initialize the template generator.

        Args:
            template_dir: Directory containing Jinja2 templates
        """
        self.template_dir = template_dir
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)), trim_blocks=True, lstrip_blocks=True
        )
        logger.info("initialized_template_generator", template_dir=str(template_dir))

    def generate_story(
        self,
        story_number: str,
        epic: str,
        title: str,
        owner: str = DEFAULT_OWNER,
        estimate: int = DEFAULT_ESTIMATE,
        output_dir: Path = OUTPUT_DIR,
        dry_run: bool = False,
    ) -> Path:
        """
        Generate a story markdown file from template.

        Args:
            story_number: Story number (e.g., "4.1")
            epic: Epic number (e.g., "4")
            title: Story title
            owner: Story owner/assignee
            estimate: Estimated hours
            output_dir: Directory to write output file
            dry_run: If True, only preview without writing

        Returns:
            Path to generated file (or would-be path if dry_run)

        Raises:
            TemplateNotFound: If template file doesn't exist
            IOError: If file write fails
        """
        # Prepare template variables
        title_slug = self._create_slug(title)
        story_key = f"{story_number}-{title_slug}"

        variables = {
            "story_number": story_number,
            "epic": epic,
            "title": title,
            "title_slug": title_slug,
            "story_key": story_key,
            "owner": owner,
            "estimate": estimate,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "acceptance_criteria": self._generate_ac_template(),
            "wiring_checklist": self._generate_wiring_checklist(),
            "submission_summary": self._generate_submission_summary(),
        }

        # Render template
        try:
            template = self.env.get_template("story.md.j2")
            rendered = template.render(**variables)
            logger.info(
                "rendered_template", story_number=story_number, variables_count=len(variables)
            )
        except TemplateNotFound as e:
            logger.error("template_not_found", template=str(e))
            raise

        # Write or preview output
        output_path = output_dir / f"{story_key}.md"

        if dry_run:
            print("\n=== DRY RUN - Generated Story Preview ===\n")
            print(rendered)
            print(f"\n=== Would write to: {output_path} ===")
        else:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path.write_text(rendered, encoding="utf-8")
            logger.info("wrote_story_file", path=str(output_path), size=len(rendered))

        return output_path

    def _create_slug(self, title: str) -> str:
        """
        Create URL-safe slug from title.

        Args:
            title: Story title

        Returns:
            Slugified title
        """
        # Replace spaces and special chars with hyphens
        slug = title.lower()
        slug = "".join(c if c.isalnum() or c == "-" else "-" for c in slug)
        # Remove consecutive hyphens and trim
        while "--" in slug:
            slug = slug.replace("--", "-")
        slug = slug.strip("-")
        return slug

    def _generate_ac_template(self) -> list:
        """Generate acceptance criteria template structure."""
        return [
            {
                "id": 1,
                "description": "TODO: Define acceptance criterion",
                "evidence": "TODO: Add evidence/implementation notes",
            },
            {
                "id": 2,
                "description": "TODO: Define acceptance criterion",
                "evidence": "TODO: Add evidence/implementation notes",
            },
            {
                "id": 3,
                "description": "TODO: Define acceptance criterion",
                "evidence": "TODO: Add evidence/implementation notes",
            },
        ]

    def _generate_wiring_checklist(self) -> dict:
        """Generate wiring checklist template."""
        return {
            "bom": ["TODO: List new dependencies/packages"],
            "logging": ["TODO: Add structured logging points"],
            "cli": ["TODO: Define CLI flags/commands"],
            "testing": ["TODO: List test requirements"],
        }

    def _generate_submission_summary(self) -> dict:
        """Generate submission summary template."""
        return {
            "files_created": ["TODO: List new files"],
            "files_modified": ["TODO: List modified files"],
            "tests_added": ["TODO: List test files"],
            "coverage": "TODO: Report coverage %",
        }

    def validate_template(self, template_name: str = "story.md.j2") -> bool:
        """
        Validate that a template exists and is loadable.

        Args:
            template_name: Name of template file

        Returns:
            True if template is valid, False otherwise
        """
        try:
            self.env.get_template(template_name)
            return True
        except TemplateNotFound:
            return False


def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Generate story template for Data Extraction Tool")

    parser.add_argument("--story-number", required=True, help="Story number (e.g., 4.1)")

    parser.add_argument("--epic", required=True, help="Epic number (e.g., 4)")

    parser.add_argument("--title", required=True, help="Story title")

    parser.add_argument(
        "--owner", default=DEFAULT_OWNER, help=f"Story owner (default: {DEFAULT_OWNER})"
    )

    parser.add_argument(
        "--estimate",
        type=int,
        default=DEFAULT_ESTIMATE,
        help=f"Estimated hours (default: {DEFAULT_ESTIMATE})",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=OUTPUT_DIR,
        help=f"Output directory (default: {OUTPUT_DIR})",
    )

    parser.add_argument("--dry-run", action="store_true", help="Preview without writing file")

    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    try:
        args = parse_arguments()

        # Ensure templates directory exists
        if not TEMPLATE_DIR.exists():
            TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
            # Create default template if it doesn't exist
            default_template = TEMPLATE_DIR / "story.md.j2"
            if not default_template.exists():
                create_default_template(default_template)

        generator = StoryTemplateGenerator()

        output_path = generator.generate_story(
            story_number=args.story_number,
            epic=args.epic,
            title=args.title,
            owner=args.owner,
            estimate=args.estimate,
            output_dir=args.output_dir,
            dry_run=args.dry_run,
        )

        if not args.dry_run:
            print(f"✅ Generated story template: {output_path}")

        return 0

    except Exception as e:
        logger.error("generation_failed", error=str(e))
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


def create_default_template(path: Path):
    """Create a default story template if none exists."""
    template_content = """# Story {{ story_number }}: {{ title }}

Status: backlog

## Story

As a [role],
I want [feature/capability],
So that [benefit/value].

### Story Header

- **Story Key:** `{{ story_key }}` (Epic {{ epic }}, Story ID {{ story_number }})
- **Dependencies:** None
- **Estimate:** {{ estimate }} hours
- **Owner:** {{ owner }}

### Story Body

[Implementation details]

## Acceptance Criteria

{% for ac in acceptance_criteria %}
{{ ac.id }}. **{{ ac.description }}**
   - Evidence: {{ ac.evidence }}
{% endfor %}

## Tasks / Subtasks

{% for item in wiring_checklist.bom %}
- [ ] BOM: {{ item }}
{% endfor %}
{% for item in wiring_checklist.logging %}
- [ ] Logging: {{ item }}
{% endfor %}
{% for item in wiring_checklist.cli %}
- [ ] CLI: {{ item }}
{% endfor %}
{% for item in wiring_checklist.testing %}
- [ ] Testing: {{ item }}
{% endfor %}

## Dev Notes

### Submission Summary

**Files Created:**
{% for file in submission_summary.files_created %}
- {{ file }}
{% endfor %}

**Files Modified:**
{% for file in submission_summary.files_modified %}
- {{ file }}
{% endfor %}

**Tests Added:**
{% for test in submission_summary.tests_added %}
- {{ test }}
{% endfor %}

**Coverage:** {{ submission_summary.coverage }}

### Completion Notes

- **{{ date }}:** Story created with template generator
"""
    path.write_text(template_content, encoding="utf-8")
    logger.info("created_default_template", path=str(path))


if __name__ == "__main__":
    sys.exit(main())
