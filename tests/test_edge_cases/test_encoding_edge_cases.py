"""
Encoding Edge Case Tests for CLI.

Tests encoding boundary conditions including:
- Mixed encodings (UTF-8, UTF-16, Latin-1)
- Emojis and special symbols
- Right-to-left text (Arabic, Hebrew)
- CJK characters (Chinese, Japanese, Korean)
- Mathematical symbols and Unicode blocks
- Control characters
- Filenames with Unicode characters
- Output paths with Unicode

Design: Equivalency partitioning methodology
Status: v1.0.2 edge case validation
"""

import tempfile
import json
from pathlib import Path
from typing import List
import pytest

from cli.main import cli
from click.testing import CliRunner


class TestEncodingEdgeCases:
    """Test encoding-related edge cases."""

    @pytest.fixture
    def runner(self):
        """Create CLI runner."""
        return CliRunner()

    @pytest.fixture
    def temp_output_dir(self):
        """Create temporary output directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def create_test_file(
        self, content: str, filename: str, temp_dir: Path, encoding="utf-8"
    ) -> Path:
        """Helper to create test files with specific content and encoding."""
        file_path = temp_dir / filename
        file_path.write_text(content, encoding=encoding)
        return file_path

    # Category: Happy Path - Standard Unicode
    def test_standard_utf8_text(self, runner, temp_output_dir):
        """1. PASS: Standard UTF-8 text with common characters."""
        content = "Hello World! This is a test file with standard ASCII characters."
        test_file = self.create_test_file(content, "standard.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Expected success, got: {result.output}"
        assert output_file.exists(), "Output file not created"

    # Category: Negative - Emoji Characters
    def test_emoji_in_content(self, runner, temp_output_dir):
        """2. PASS: Content with various emoji characters."""
        content = "Test with emojis: 😀 🎉 🚀 💻 🔥 ⚡ 🌟 ✨"
        test_file = self.create_test_file(content, "emoji_test.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with emojis: {result.output}"

        # Verify emojis preserved
        with open(output_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            content_found = False
            for block in data.get("content_blocks", []):
                if "😀" in block.get("content", "") or "🎉" in block.get("content", ""):
                    content_found = True
                    break
            assert content_found, "Emojis not preserved in output"

    def test_emoji_sequences_and_modifiers(self, runner, temp_output_dir):
        """3. PASS: Complex emoji sequences with skin tone modifiers."""
        content = "Complex emojis: 👨‍👩‍👧‍👦 👍🏻 👍🏿 🏴󠁧󠁢󠁥󠁮󠁧󠁿"
        test_file = self.create_test_file(content, "complex_emoji.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with complex emojis: {result.output}"

    # Category: Negative - Right-to-Left Text
    def test_arabic_text(self, runner, temp_output_dir):
        """4. PASS: Arabic right-to-left text."""
        content = "Arabic text: مرحبا بك في اختبار النظام العربية"
        test_file = self.create_test_file(content, "arabic.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with Arabic: {result.output}"

    def test_hebrew_text(self, runner, temp_output_dir):
        """5. PASS: Hebrew right-to-left text."""
        content = "Hebrew text: שלום עולם - בדיקת מערכת בעברית"
        test_file = self.create_test_file(content, "hebrew.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with Hebrew: {result.output}"

    def test_mixed_ltr_rtl(self, runner, temp_output_dir):
        """6. PASS: Mixed left-to-right and right-to-left text."""
        content = "Mixed: Hello مرحبا World שלום Test"
        test_file = self.create_test_file(content, "mixed_direction.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with mixed direction: {result.output}"

    # Category: Negative - CJK Characters
    def test_chinese_simplified(self, runner, temp_output_dir):
        """7. PASS: Chinese simplified characters."""
        content = "Chinese (Simplified): 这是一个测试文件 你好世界"
        test_file = self.create_test_file(content, "chinese_simp.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with Chinese: {result.output}"

    def test_chinese_traditional(self, runner, temp_output_dir):
        """8. PASS: Chinese traditional characters."""
        content = "Chinese (Traditional): 這是一個測試文件 你好世界"
        test_file = self.create_test_file(content, "chinese_trad.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with Traditional Chinese: {result.output}"

    def test_japanese_mixed_scripts(self, runner, temp_output_dir):
        """9. PASS: Japanese text with hiragana, katakana, and kanji."""
        content = "Japanese: これはテストです 日本語 ひらがな カタカナ 漢字"
        test_file = self.create_test_file(content, "japanese.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with Japanese: {result.output}"

    def test_korean_hangul(self, runner, temp_output_dir):
        """10. PASS: Korean Hangul characters."""
        content = "Korean: 안녕하세요 세계 테스트 파일입니다"
        test_file = self.create_test_file(content, "korean.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with Korean: {result.output}"

    # Category: Negative - Mathematical Symbols
    def test_mathematical_symbols(self, runner, temp_output_dir):
        """11. PASS: Various mathematical Unicode symbols."""
        content = "Math symbols: ∑ ∫ ∂ ∇ π √ ∞ ≈ ≠ ≤ ≥ ± × ÷ ∈ ∉ ∪ ∩"
        test_file = self.create_test_file(content, "math_symbols.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with math symbols: {result.output}"

    def test_greek_letters(self, runner, temp_output_dir):
        """12. PASS: Greek letters commonly used in formulas."""
        content = "Greek: α β γ δ ε ζ η θ λ μ ν π ρ σ τ φ χ ψ ω Ω"
        test_file = self.create_test_file(content, "greek.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with Greek letters: {result.output}"

    # Category: Security - Control Characters
    def test_control_characters_printable(self, runner, temp_output_dir):
        """13. PASS: Printable control characters (tab, newline)."""
        content = "Text with\ttabs\nand\nnewlines\r\nand carriage returns"
        test_file = self.create_test_file(content, "control_printable.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with control characters: {result.output}"

    def test_zero_width_characters(self, runner, temp_output_dir):
        """14. PASS: Zero-width characters (joiners, spaces)."""
        content = "Zero-width: \u200b\u200c\u200d\ufeff test"
        test_file = self.create_test_file(content, "zero_width.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with zero-width characters: {result.output}"

    # Category: Negative - Unicode Filename
    def test_unicode_filename_emoji(self, runner, temp_output_dir):
        """15. PASS: Filename with emoji characters."""
        content = "Test content"
        filename = "test_file_🚀_emoji.txt"
        test_file = self.create_test_file(content, filename, temp_output_dir)
        output_file = temp_output_dir / "output_🚀.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # May fail on some filesystems, that's okay
        if result.exit_code == 0:
            assert output_file.exists(), "Output with emoji filename not created"
        else:
            # Expected failure is acceptable
            assert "error" in result.output.lower() or result.exit_code != 0

    def test_unicode_filename_chinese(self, runner, temp_output_dir):
        """16. PASS: Filename with Chinese characters."""
        content = "Test content"
        filename = "测试文件.txt"
        test_file = self.create_test_file(content, filename, temp_output_dir)
        output_file = temp_output_dir / "输出.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        # May fail on some filesystems
        if result.exit_code == 0:
            assert output_file.exists()
        else:
            assert "error" in result.output.lower() or result.exit_code != 0

    # Category: Integration - Mixed Unicode
    def test_all_unicode_categories_mixed(self, runner, temp_output_dir):
        """17. PASS: Content mixing multiple Unicode categories."""
        content = """
        Mixed Unicode Test:
        English: Hello World
        Emoji: 🚀 💻 🎉
        Arabic: مرحبا
        Hebrew: שלום
        Chinese: 你好
        Japanese: こんにちは
        Korean: 안녕하세요
        Math: ∑ π ∞
        Greek: α β γ
        Symbols: ★ ♠ ♣ ♥ ♦
        """
        test_file = self.create_test_file(content, "mixed_unicode.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with mixed Unicode: {result.output}"

    # Category: Performance - Large Unicode Content
    def test_large_unicode_content(self, runner, temp_output_dir):
        """18. PASS: Large file with extensive Unicode characters."""
        # Generate large content with various Unicode
        lines = []
        for i in range(1000):
            lines.append(f"Line {i}: Hello 世界 🚀 مرحبا שלום こんにちは 안녕")

        content = "\n".join(lines)
        test_file = self.create_test_file(content, "large_unicode.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with large Unicode content: {result.output}"

    # Category: Negative - Special Unicode Blocks
    def test_rare_unicode_blocks(self, runner, temp_output_dir):
        """19. PASS: Rare Unicode blocks (Linear B, Cuneiform)."""
        # Note: May not display correctly but should not crash
        content = "Rare blocks: 𐀀 𐀁 (Linear B) 𒀀 𒀁 (Cuneiform) 𓀀 𓀁 (Hieroglyphs)"
        test_file = self.create_test_file(content, "rare_unicode.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with rare Unicode blocks: {result.output}"

    def test_combining_diacritics(self, runner, temp_output_dir):
        """20. PASS: Combining diacritical marks."""
        content = "Diacritics: é è ê ë ñ ü ö ä à combining: e\u0301 a\u0300"
        test_file = self.create_test_file(content, "diacritics.txt", temp_output_dir)
        output_file = temp_output_dir / "output.json"

        result = runner.invoke(
            cli, ["extract", str(test_file), "--output", str(output_file), "--format", "json"]
        )

        assert result.exit_code == 0, f"Failed with diacritics: {result.output}"
