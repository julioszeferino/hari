import os
from io import StringIO

import pytest
import yaml

from hari_data.utils.helpers import (
    create_yaml_from_dict,
    is_hari_project,
    read_yaml_to_dict,
)


def test_is_hari_project_true(tmp_path, monkeypatch):
    # Arrange: create a dummy 'hari.lock' file in the temp directory
    monkeypatch.chdir(tmp_path)
    (tmp_path / 'hari.lock').touch()
    # Act & Assert
    assert is_hari_project() is True


def test_is_hari_project_false(tmp_path, monkeypatch):
    # Arrange: ensure 'hari.lock' does not exist
    monkeypatch.chdir(tmp_path)
    # Act & Assert
    assert is_hari_project() is False


def test_create_yaml_from_dict_creates_file(tmp_path):
    # Arrange
    data = {'a': 1, 'b': [2, 3]}
    dir_name = tmp_path / 'mydir'
    file_name = 'myfile'
    # Act
    create_yaml_from_dict(data, str(dir_name), file_name)
    # Assert
    yaml_path = dir_name / f'{file_name}.yaml'
    assert yaml_path.exists()
    with open(yaml_path, 'r') as f:
        loaded = yaml.safe_load(f)
    assert loaded == data


def test_create_yaml_from_dict_creates_dir(tmp_path):
    # Arrange
    data = {'foo': 'bar'}
    dir_name = tmp_path / 'newdir'
    file_name = 'testfile'
    # Act
    create_yaml_from_dict(data, str(dir_name), file_name)
    # Assert
    assert os.path.isdir(dir_name)
    assert os.path.isfile(dir_name / f'{file_name}.yaml')


def test_create_yaml_from_dict_raises_oserror(monkeypatch):
    # Simulate OSError when creating directory
    def raise_oserror(*args, **kwargs):
        raise OSError('Cannot create directory')

    monkeypatch.setattr(os, 'makedirs', raise_oserror)
    with pytest.raises(
        OSError, match='Error creating YAML file: Cannot create directory'
    ):
        from hari_data.utils.helpers import create_yaml_from_dict

        create_yaml_from_dict({}, '/nonexistent_dir', 'file')


def test_create_yaml_from_dict_raises_yamlerror(monkeypatch, tmp_path):
    # Simula erro do yaml.dump para garantir cobertura do except yaml.YAMLError
    dir_name = tmp_path / 'errordir'
    dir_name.mkdir()
    # Patch yaml.dump no namespace correto
    import hari_data.utils.helpers as helpers

    monkeypatch.setattr(
        helpers.yaml,
        'dump',
        lambda *a, **kw: (_ for _ in ()).throw(
            yaml.YAMLError('YAML dump error')
        ),
    )
    with pytest.raises(
        yaml.YAMLError, match='Error writing YAML file: YAML dump error'
    ):
        helpers.create_yaml_from_dict({}, str(dir_name), 'file')


def test_read_yaml_to_dict_success(monkeypatch):
    """Test successful reading of YAML file and conversion to dictionary."""
    # Mock file content
    yaml_content = 'key1: value1\nkey2: value2'
    expected_data = {'key1': 'value1', 'key2': 'value2'}

    # Mock open function to return StringIO with our content
    def mock_open(file_path, mode):
        assert file_path == '/test/path.yaml'
        assert mode == 'r'
        return StringIO(yaml_content)

    monkeypatch.setattr('builtins.open', mock_open)

    # Call the function and check result
    result = read_yaml_to_dict('/test/path.yaml')
    assert result == expected_data


def test_read_yaml_to_dict_empty_file(monkeypatch):
    """Test reading an empty YAML file returns empty dictionary."""
    # Mock open to return empty StringIO
    monkeypatch.setattr('builtins.open', lambda *args, **kwargs: StringIO(''))

    # Call function and check it returns empty dict
    result = read_yaml_to_dict('/test/empty.yaml')
    assert result == {}


def test_read_yaml_to_dict_null_content(monkeypatch):
    """Test reading a YAML file with null content returns empty dictionary."""
    # Mock open to return StringIO with 'null'
    monkeypatch.setattr(
        'builtins.open', lambda *args, **kwargs: StringIO('null')
    )

    # Call function and check it returns empty dict
    result = read_yaml_to_dict('/test/null.yaml')
    assert result == {}


def test_read_yaml_to_dict_file_not_found(monkeypatch):
    """Test FileNotFoundError is raised and properly formatted."""
    # Mock open to raise FileNotFoundError
    def mock_open_error(*args, **kwargs):
        raise FileNotFoundError(
            "No such file or directory: '/test/missing.yaml'"
        )

    monkeypatch.setattr('builtins.open', mock_open_error)

    # Check that FileNotFoundError is raised with proper message
    with pytest.raises(FileNotFoundError, match='YAML file not found:.*'):
        read_yaml_to_dict('/test/missing.yaml')


def test_read_yaml_to_dict_yaml_error(monkeypatch):
    """Test YAMLError is raised and properly formatted for invalid YAML."""
    # Mock open to return StringIO with invalid YAML
    monkeypatch.setattr(
        'builtins.open', lambda *args, **kwargs: StringIO('key: : value')
    )

    # Mock yaml.safe_load to raise YAMLError
    def mock_yaml_error(*args, **kwargs):
        raise yaml.YAMLError('mapping values are not allowed here')

    monkeypatch.setattr(yaml, 'safe_load', mock_yaml_error)

    # Check that YAMLError is raised with proper message
    with pytest.raises(yaml.YAMLError, match='Error reading YAML file:.*'):
        read_yaml_to_dict('/test/invalid.yaml')
