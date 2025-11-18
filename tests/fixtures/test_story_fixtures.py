"""
Test fixtures for Story test-story

Provides sample data and test configurations.
Generated at: 2025-11-18T04:30:58.107378
"""

import pytest
from pathlib import Path
from typing import Any, Dict, List


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """
    Provide sample test data for story acceptance criteria.
    
    Returns:
        Dictionary containing test inputs and expected outputs
    """
    return {
        # AC-1: T
        'ac_1_input': {
            # TODO: Add specific test input data
            'description': 'est AC:** Test this feature...',
            'data': None,
        },
        'ac_1_expected': {
            # TODO: Add expected output
            'result': None,
        },

    }


@pytest.fixture
def test_config() -> Dict[str, Any]:
    """
    Provide test configuration settings.
    
    Returns:
        Dictionary containing test configuration
    """
    return {
        'story_key': 'test-story',
        'epic_number': '',
        'test_timeout': 30,  # seconds
        'enable_debug': False,
        'test_data_dir': Path('tests/data'),
    }


@pytest.fixture
def mock_dependencies(monkeypatch):
    """
    Mock external dependencies for isolated testing.
    
    Args:
        monkeypatch: pytest monkeypatch fixture
    
    Returns:
        Dictionary of mocked dependencies
    """
    mocks = {}
    
    # TODO: Add specific mocks based on story requirements
    # Example:
    # from unittest.mock import Mock
    # mock_api = Mock()
    # monkeypatch.setattr('module.api_client', mock_api)
    # mocks['api'] = mock_api
    
    return mocks
