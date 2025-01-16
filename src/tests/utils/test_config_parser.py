from pathlib import Path
from unittest.mock import patch

import pytest

from pdoc_ai.utils.config_parser import Config


@pytest.fixture
def sample_toml_content():
    return """
    [server]
    host = "localhost"
    port = 8000
    
    [database]
    url = "postgresql://localhost:5432"
    username = "admin"
    """


class TestConfig:
    def test_init_default(self):
        """Test initialization with default parameters"""
        config = Config()
        assert config._Config__filename == "config.toml"
        assert config._Config__filepath is None

    def test_init_with_filepath_directory(self, tmp_path):
        """Test initialization with directory path"""
        config = Config(filepath=tmp_path)
        assert config._Config__filename == "config.toml"
        assert config._Config__filepath == tmp_path / "config.toml"

    def test_init_with_filepath_file(self, tmp_path):
        """Test initialization with file path"""
        filepath = tmp_path / "custom_config.toml"
        config = Config(filepath=filepath)
        assert config._Config__filename == "custom_config.toml"
        assert config._Config__filepath is None

    def test_str_representation(self):
        """Test string representation of Config"""
        config = Config()
        expected = "Config(filename=config.toml, filepath=None)"
        assert str(config) == expected

    @patch("pathlib.Path.exists")
    def test_filepath_with_direct_file(self, mock_exists):
        """Test filepath resolution with direct file"""
        mock_exists.return_value = True
        config = Config("test_config.toml")
        assert config.filepath == Path("test_config.toml")

    @patch("pathlib.Path.exists")
    @patch.object(Config, "_Config__find_src_folder")
    def test_filepath_with_src_folder(self, mock_find_src, mock_exists):
        """Test filepath resolution with src folder"""
        mock_exists.return_value = False
        mock_find_src.return_value = Path("/path/to/src")
        config = Config()
        assert config.filepath == Path("/path/to/src/config.toml")

    def test_value_with_nonexistent_file(self):
        """Test value property with non-existent file"""
        config = Config("nonexistent.toml")
        assert config.value == {}

    def test_exists_with_nonexistent_file(self):
        """Test exists method with non-existent file"""
        config = Config("nonexistent.toml")
        assert config.exists() is False


if __name__ == "__main__":
    pytest.main(["-v"])
