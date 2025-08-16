import os

import yaml

from hari_data.utils.helpers import create_yaml_from_dict, is_hari_project


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
