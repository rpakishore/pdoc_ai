import logging
import time
from pathlib import Path
from unittest.mock import patch

import pytest

from template_python.utils.logger import Log


@pytest.fixture
def mock_paths():
    with patch("template_python.paths") as mock_paths:
        mock_paths.dir_src = Path("/mock/src")
        yield mock_paths


@pytest.fixture
def mock_getpass():
    with patch("getpass.getuser") as mock_user:
        mock_user.return_value = "testuser"
        yield mock_user


@pytest.fixture
def log_instance(tmp_path, mock_paths, mock_getpass):
    with patch("pathlib.Path.mkdir"):
        log = Log()
        # Replace the real log file with a temporary one
        log.logfile = tmp_path / f"testuser{time.strftime('-%Y-%b')}.log"
        return log


class TestLog:
    def test_initialization(self, log_instance):
        """Test if Log instance is properly initialized"""
        assert isinstance(log_instance.logger, logging.Logger)
        assert log_instance.logger.name == "testuser"

    def test_info_message(self, log_instance, caplog):
        """Test info level logging"""
        with caplog.at_level(logging.INFO):
            test_message = "Info test message"
            log_instance.info(test_message)
            assert test_message in caplog.text

    def test_log_level_message(self, log_instance, caplog):
        """Test custom level logging"""
        with caplog.at_level(logging.INFO):
            test_message = "Custom level test message"
            log_instance.log(logging.INFO, test_message)
            assert test_message in caplog.text

    def test_set_level(self, log_instance):
        """Test changing log level"""
        log_instance.setLevel(logging.DEBUG)
        assert log_instance.logger.level == logging.DEBUG

    def test_contents_reading(self, log_instance, tmp_path):
        """Test reading log file contents"""
        test_logs = ["Log line 1\n", "Log line 2\n", "Log line 3\n"]

        # Write some test content to the log file
        log_instance.logfile.write_text("".join(test_logs))

        # Test reading all lines
        assert log_instance.contents() == test_logs

        # Test reading limited lines
        assert log_instance.contents(2) == test_logs[-2:]

    def test_contents_with_empty_file(self, log_instance):
        """Test reading from empty log file"""
        # Ensure the log file exists but is empty
        log_instance.logfile.write_text("")
        assert log_instance.contents() == []


if __name__ == "__main__":
    pytest.main(["-v"])
