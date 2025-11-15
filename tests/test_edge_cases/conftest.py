"""
Configuration for edge case tests.

Provides shared fixtures and markers for edge case testing.
"""


def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line("markers", "slow: marks tests as slow (run with -m slow)")
    config.addinivalue_line("markers", "encoding: marks encoding edge case tests")
    config.addinivalue_line("markers", "threading: marks threading edge case tests")
    config.addinivalue_line("markers", "filesystem: marks filesystem edge case tests")
    config.addinivalue_line("markers", "resource: marks resource edge case tests")
