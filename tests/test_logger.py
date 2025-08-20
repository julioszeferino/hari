import logging

import pytest

from hari_data.utils.logger import Logger


@pytest.fixture
def reset_logger():
    """Reset the Logger singleton between tests"""
    Logger._instance = None
    Logger._logger = None
    yield
    # Clean up after test
    Logger._instance = None
    Logger._logger = None


def test_already_configured_logger(reset_logger, monkeypatch):
    """Test that a warning is issued when configuring an already configured logger."""
    # First configuration
    logger = Logger()
    logger.configure(app_name='TestApp')

    # Keep track of warning calls
    warning_calls = []

    # Mock the warning method
    def mock_warning(message):
        warning_calls.append(message)

    # Apply the monkeypatch
    monkeypatch.setattr(logger._logger, 'warning', mock_warning)

    # Second configuration attempt
    logger.configure(app_name='AnotherApp')

    # Verify warning was called with expected message
    assert len(warning_calls) == 1
    assert (
        warning_calls[0]
        == 'Logger is already configured. Ignoring the new configuration.'
    )


def test_configure_with_configs_path(reset_logger, monkeypatch):
    """Test configuring the logger with a config path."""
    # Mock config data
    mock_config = {'app_name': 'ConfigApp', 'log_level': 'ERROR'}

    # Mock the read_yaml_to_dict function
    def mock_read_yaml(path):
        assert path == '/fake/path'  # Verify the path was passed correctly
        return mock_config

    monkeypatch.setattr(
        'hari_data.utils.logger.read_yaml_to_dict', mock_read_yaml
    )

    # Keep track of print calls
    print_calls = []

    # Mock the print function
    def mock_print(*args):
        print_calls.append(' '.join(str(arg) for arg in args))

    monkeypatch.setattr('builtins.print', mock_print)

    # Configure the logger
    logger = Logger()
    logger.configure(configs_path='/fake/path')

    # Verify the config values were used
    assert logger._logger.name == 'ConfigApp'
    assert logger._logger.level == logging.ERROR

    # Verify the print message
    assert len(print_calls) == 1
    assert (
        print_calls[0]
        == 'Logger configured with app name "ConfigApp" and log level "ERROR".'
    )
