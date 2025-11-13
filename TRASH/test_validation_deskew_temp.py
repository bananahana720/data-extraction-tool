    @patch("src.data_extract.normalize.validation.TESSERACT_AVAILABLE", True)
    @patch("src.data_extract.normalize.validation.determine_skew")
    @patch("src.data_extract.normalize.validation.rotate")
    @patch("src.data_extract.normalize.validation.ImageEnhance", create=True)
    @patch("src.data_extract.normalize.validation.ImageFilter", create=True)
    @patch("src.data_extract.normalize.validation.Image", create=True)
    def test_preprocess_image_applies_deskew_for_significant_angle(
        self, mock_image_class, mock_filter, mock_enhance, mock_rotate, mock_determine_skew
    ):
        """Test that deskew is applied when skew angle is significant (>0.1 degrees)."""
        import numpy as np
        
        # Create mock image
        mock_image = MagicMock()
        mock_image.mode = "RGB"
        mock_grayscale = MagicMock()
        mock_image.convert.return_value = mock_grayscale
        mock_grayscale.filter.return_value = mock_grayscale
        
        # Mock deskew detection to return significant angle (5 degrees)
        mock_determine_skew.return_value = 5.0
        
        # Mock rotation to return rotated array
        rotated_array = np.zeros((100, 100), dtype=np.uint8)
        mock_rotate.return_value = rotated_array
        
        # Mock Image.fromarray to return a new image
        mock_deskewed_image = MagicMock()
        mock_image_class.fromarray.return_value = mock_deskewed_image
        mock_deskewed_image.filter.return_value = mock_deskewed_image
        
        # Mock ImageEnhance.Contrast
        mock_enhancer = MagicMock()
        mock_enhancer.enhance.return_value = mock_deskewed_image
        mock_enhance.Contrast.return_value = mock_enhancer
        
        validator = QualityValidator(ocr_preprocessing_enabled=True)
        result = validator.preprocess_image_for_ocr(mock_image)
        
        # Verify deskew was called
        mock_determine_skew.assert_called_once()
        # Verify rotate was called with the detected angle
        mock_rotate.assert_called_once()
        assert mock_rotate.call_args[0][1] == 5.0  # Second arg is the angle
        # Verify Image.fromarray was called to convert rotated array back to PIL
        mock_image_class.fromarray.assert_called_once()

    @patch("src.data_extract.normalize.validation.TESSERACT_AVAILABLE", True)
    @patch("src.data_extract.normalize.validation.determine_skew")
    @patch("src.data_extract.normalize.validation.rotate")
    @patch("src.data_extract.normalize.validation.ImageEnhance", create=True)
    @patch("src.data_extract.normalize.validation.ImageFilter", create=True)
    @patch("src.data_extract.normalize.validation.Image", create=True)
    def test_preprocess_image_skips_deskew_for_small_angle(
        self, mock_image_class, mock_filter, mock_enhance, mock_rotate, mock_determine_skew
    ):
        """Test that deskew is skipped when angle is too small (<0.1 degrees)."""
        # Create mock image
        mock_image = MagicMock()
        mock_image.mode = "L"  # Already grayscale
        mock_image.filter.return_value = mock_image
        
        # Mock deskew detection to return negligible angle (0.05 degrees)
        mock_determine_skew.return_value = 0.05
        
        # Mock ImageEnhance.Contrast
        mock_enhancer = MagicMock()
        mock_enhancer.enhance.return_value = mock_image
        mock_enhance.Contrast.return_value = mock_enhancer
        
        validator = QualityValidator(ocr_preprocessing_enabled=True)
        result = validator.preprocess_image_for_ocr(mock_image)
        
        # Verify deskew was called but rotation was NOT
        mock_determine_skew.assert_called_once()
        mock_rotate.assert_not_called()  # Should skip rotation for small angles

    @patch("src.data_extract.normalize.validation.TESSERACT_AVAILABLE", True)
    @patch("src.data_extract.normalize.validation.determine_skew")
    @patch("src.data_extract.normalize.validation.ImageEnhance", create=True)
    @patch("src.data_extract.normalize.validation.ImageFilter", create=True)
    @patch("src.data_extract.normalize.validation.Image", create=True)
    def test_preprocess_image_handles_deskew_failure_gracefully(
        self, mock_image_class, mock_filter, mock_enhance, mock_determine_skew
    ):
        """Test that preprocessing continues if deskew fails."""
        # Create mock image
        mock_image = MagicMock()
        mock_image.mode = "L"
        mock_image.filter.return_value = mock_image
        
        # Mock deskew to raise an exception
        mock_determine_skew.side_effect = Exception("Deskew library error")
        
        # Mock ImageEnhance.Contrast
        mock_enhancer = MagicMock()
        mock_enhancer.enhance.return_value = mock_image
        mock_enhance.Contrast.return_value = mock_enhancer
        
        validator = QualityValidator(ocr_preprocessing_enabled=True)
        
        # Should not raise exception - should handle gracefully
        result = validator.preprocess_image_for_ocr(mock_image)
        
        # Should still return a processed image (denoise + contrast applied)
        assert result is not None
        mock_image.filter.assert_called()  # Denoise was applied
        mock_enhancer.enhance.assert_called()  # Contrast was applied
