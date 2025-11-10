#!/usr/bin/env python3
"""
Test script to verify poppler_path configuration works correctly.
"""

from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


def test_poppler_config():
    """Test that poppler_path configuration is properly loaded."""

    print("=" * 70)
    print("Testing poppler_path Configuration Support")
    print("=" * 70)

    # Test 1: Dict config
    print("\n[Test 1] Dictionary Configuration")
    try:
        from extractors.pdf_extractor import PdfExtractor

        config = {
            "tesseract_cmd": "C:/test/tesseract.exe",
            "poppler_path": "C:/test/poppler/bin",
            "ocr_dpi": 150,
        }

        extractor = PdfExtractor(config=config)

        assert extractor.tesseract_cmd == "C:/test/tesseract.exe", "Tesseract path mismatch"
        assert extractor.poppler_path == "C:/test/poppler/bin", "Poppler path mismatch"
        assert extractor.ocr_dpi == 150, "OCR DPI mismatch"

        print(f"  ✓ tesseract_cmd: {extractor.tesseract_cmd}")
        print(f"  ✓ poppler_path: {extractor.poppler_path}")
        print(f"  ✓ ocr_dpi: {extractor.ocr_dpi}")
        print("  PASSED")

    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False

    # Test 2: ConfigManager
    print("\n[Test 2] ConfigManager Configuration")
    try:
        from infrastructure import ConfigManager

        # Create test config
        test_config = {
            "extractors": {
                "pdf": {
                    "tesseract_cmd": "C:/test2/tesseract.exe",
                    "poppler_path": "C:/test2/poppler/bin",
                    "ocr_dpi": 200,
                }
            }
        }

        config_manager = ConfigManager(config_file=test_config)
        extractor = PdfExtractor(config=config_manager)

        assert extractor.tesseract_cmd == "C:/test2/tesseract.exe", "Tesseract path mismatch"
        assert extractor.poppler_path == "C:/test2/poppler/bin", "Poppler path mismatch"
        assert extractor.ocr_dpi == 200, "OCR DPI mismatch"

        print(f"  ✓ tesseract_cmd: {extractor.tesseract_cmd}")
        print(f"  ✓ poppler_path: {extractor.poppler_path}")
        print(f"  ✓ ocr_dpi: {extractor.ocr_dpi}")
        print("  PASSED")

    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False

    # Test 3: Defaults
    print("\n[Test 3] Default Configuration")
    try:
        extractor = PdfExtractor()

        assert extractor.tesseract_cmd is None, "Default tesseract_cmd should be None"
        assert extractor.poppler_path is None, "Default poppler_path should be None"
        assert extractor.ocr_dpi == 300, "Default OCR DPI should be 300"

        print(f"  ✓ tesseract_cmd: {extractor.tesseract_cmd} (default)")
        print(f"  ✓ poppler_path: {extractor.poppler_path} (default)")
        print(f"  ✓ ocr_dpi: {extractor.ocr_dpi} (default)")
        print("  PASSED")

    except Exception as e:
        print(f"  ✗ FAILED: {e}")
        return False

    print("\n" + "=" * 70)
    print("✓ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nThe poppler_path configuration is working correctly.")
    print("You can now use it in your config.yaml:")
    print(
        """
extractors:
  pdf:
    tesseract_cmd: C:/path/to/tesseract.exe
    poppler_path: C:/path/to/poppler/Library/bin
    """
    )

    return True


if __name__ == "__main__":
    success = test_poppler_config()
    sys.exit(0 if success else 1)
