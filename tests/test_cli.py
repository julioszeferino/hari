import re

from typer.testing import CliRunner

from hari.cli.commands.cli import add_columns, app

runner = CliRunner()


def result_cleaned_norm(result):
    result_cleaned = re.sub(r'\x1b\[[0-9;]*m', '', result)
    result_normalized = ' '.join(result_cleaned.split())
    return result_normalized


def test_version_callback(monkeypatch):
    """
    Test hari --version
    """
    # ---- Arrange / Act ----
    monkeypatch.setattr('hari.cli.commands.cli.__version__', '1.0.0')
    result = runner.invoke(app, ['--version'], env={'NO_COLOR': '1'})

    # ---- Assert ----
    # Check success
    assert result.exit_code == 0
    # Check Output
    assert 'Hari CLI version: 1.0.0' in result.output


def test_callback_no_flag(mocker):
    """
    Test hari without --version flag
    """
    # ---- Arrange / Act ----
    mocker.patch('hari.cli.commands.cli.version_callback', return_value=None)
    result = runner.invoke(app, [], env={'NO_COLOR': '1'})

    # ---- Assert ----
    # Check success
    assert result.exit_code == 0
    # Check Output
    assert 'How to use:' in result.output


def test_create_project_success(mocker):
    """
    Test hari create project_name
    """
    # ---- Arrange ----
    # change the return value of the function project
    mock_func_project = mocker.patch('hari.cli.commands.cli.project')
    mock_func_project.return_value = {
        'dirs_created': ['configs', 'utils'],
        'files_created': ['job.py', 'README.md'],
    }
    project_name = 'project_test'
    expected_outputs = [
        'Directories and Files Created',
        'Project project_test created successfully!',
        'Happy coding! 🚀',
        'Directory │ configs',
        'Directory │ utils',
        'File │ job.py',
        'File │ README.md',
    ]

    # ---- Act ----
    result = runner.invoke(
        app, ['create', project_name], env={'NO_COLOR': '1', 'COLUMNS': '120'}
    )
    result_cleaned = result_cleaned_norm(result.output)

    # ---- Assert ----
    # Check success
    assert result.exit_code == 0
    # Check Output
    for check in expected_outputs:
        assert check in result_cleaned


def test_add_columns_no_columns(mocker):
    # ---- Arrange ----
    # simulate the user not wanting to add
    # in first prompt, but wanting to add in second
    # question and the next questions recursively
    mocker.patch(
        'hari.cli.commands.cli.confirm',
        side_effect=[
            False,  # No to add columns
            True,  # Yes to add columns
            True,  # is_nullable
            False,  # is_not unique
            False,  # No to add more columns
        ],
    )
    # simulate the user adding a column
    mocker.patch(
        'hari.cli.commands.cli.prompt',
        side_effect=[
            'col1',  # Column name
            'string',  # Column type
        ],
    )
    # desactivate the console print
    mocker.patch('hari.cli.commands.cli.console.print')

    columns_expected = [
        {
            'name': 'col1',
            'type': 'string',
            'is_nullable': True,
            'is_unique': False,
        }
    ]

    # ---- Act ----
    columns = add_columns()

    # ---- Assert ----
    assert columns == columns_expected


def test_add_columns_type_invalid(mocker):
    # ---- Arrange ----
    # simulate the user wanting to add a column
    mocker.patch(
        'hari.cli.commands.cli.confirm',
        side_effect=[
            True,  # Yes to add columns
            True,  # Yes to add columns sec try
            True,  # is_nullable
            False,  # is_not unique
            False,  # No to add more columns
        ],
    )
    # simulate to add a column with float type
    # simulate the user adding a column
    mocker.patch(
        'hari.cli.commands.cli.prompt',
        side_effect=[
            'col1',  # Column name
            'invalid_type',  # Column type
            'col2',  # Column name for next column
            'string',  # Column type for next column
        ],
    )
    # desactivate the console print
    mocker.patch('hari.cli.commands.cli.console.print')

    columns_expected = [
        {
            'name': 'col2',
            'type': 'string',
            'is_nullable': True,
            'is_unique': False,
        }
    ]

    # ---- Act ----
    columns = add_columns()

    # ---- Assert ----
    assert columns == columns_expected


def test_add_contract_outside_hari_project(mocker):
    # ---- Arrange ----
    # define line args
    args = [
        'contract',
        'new',
        'test_contract',
        '--output-table-name',
        'test',
        '--output-table-format',
        'csv',
        '--output-table-path',
        '/tmp',
        '--sla',
        'n',
        '--description',
        '',
        '--owner-email',
        '',
    ]
    # change the return value of the function is_hari_project
    mocker.patch('hari.cli.commands.cli.is_hari_project', return_value=False)

    # ---- Act ----
    result = runner.invoke(app, args, env={'NO_COLOR': '1'})

    assert result.exit_code == 1
    assert 'This command must be run inside a Hari project' in result.output


def test_contract_new_happy_path_with_partitions(mocker):
    # ---- Arrange ----
    args = [
        'contract',
        'new',
        'test_contract',
        '--output-table-name',
        'test',
        '--output-table-format',
        'csv',
        '--output-table-path',
        '/tmp',
        '--sla',
        'n',
        '--description',
        '',
        '--owner-email',
        '',
    ]
    # simulate a happy path
    mocker.patch('hari.cli.commands.cli.is_hari_project', return_value=True)
    # simulate columns addition
    mocker.patch(
        'hari.cli.commands.cli.add_columns',
        return_value=[
            {
                'name': 'col1',
                'type': 'string',
                'is_nullable': True,
                'is_unique': False,
            },
            {
                'name': 'col2',
                'type': 'integer',
                'is_nullable': True,
                'is_unique': False,
            },
        ],
    )
    # simulate add partition
    mocker.patch(
        'hari.cli.commands.cli.confirm',
        side_effect=[
            True,  # Add partition columns
        ],
    )
    # simulate a choice for partition column
    mocker.patch(
        'hari.cli.commands.cli.Prompt.ask',
        side_effect=[
            'col1',  # Selected col1 for partition
            'col1',  # Try to add col1 again, should be ignored
            '',  # No more partition columns
        ],
    )
    # simulate the contract creation
    mock_contract = mocker.patch('hari.cli.commands.cli.contract')
    # simulate version
    mocker.patch('hari.cli.commands.cli.__version__', return_value='0.1.1')
    # desactivate the console print
    mock_create_yaml = mocker.patch(
        'hari.cli.commands.cli.create_yaml_from_dict'
    )

    # ---- Act ----
    result = runner.invoke(app, args, env={'NO_COLOR': '1'})

    # ---- Assert ----
    # Check success
    assert result.exit_code == 0
    # Check Output
    assert (
        'Contract test_contract created successfully!'
        in result_cleaned_norm(result.output)
    )
    # Check Partitioned By
    assert "Column 'col1' already selected." in result_cleaned_norm(
        result.output
    )
    # Check that the YAML file was created
    mock_create_yaml.assert_called_once()
    # Check parameters passed to the contract function
    mock_contract.assert_called_once_with(
        version=mocker.ANY,
        created_at=mocker.ANY,
        name='test_contract',
        description='',
        owner_email='',
        output_table={
            'name': 'test',
            'path': '/tmp',
            'format': 'csv',
            'partitioned_by': ['col1'],
        },
        columns=[
            {
                'name': 'col1',
                'type': 'string',
                'is_nullable': True,
                'is_unique': False,
            },
            {
                'name': 'col2',
                'type': 'integer',
                'is_nullable': True,
                'is_unique': False,
            },
        ],
        sla=None,
    )


def test_contract_with_sla(mocker):
    """
    Test contract creation with SLA prompts
    """
    # ---- Arrange ----
    args = [
        'contract',
        'new',
        'test_contract',
        '--output-table-name',
        'test',
        '--output-table-format',
        'csv',
        '--output-table-path',
        '/tmp',
        '--sla',
        'y',
        '--description',
        '',
        '--owner-email',
        '',
    ]
    # Simulate being inside a Hari project
    mocker.patch('hari.cli.commands.cli.is_hari_project', return_value=True)
    # Simulate columns addition
    mocker.patch(
        'hari.cli.commands.cli.add_columns',
        return_value=[
            {
                'name': 'col1',
                'type': 'string',
                'is_nullable': True,
                'is_unique': False,
            },
        ],
    )
    # Simulate not adding partition columns
    mocker.patch(
        'hari.cli.commands.cli.confirm',
        side_effect=[
            False,  # No to add partition columns
        ],
    )
    # Simulate SLA prompts
    mocker.patch(
        'hari.cli.commands.cli.prompt',
        side_effect=[
            'daily',  # Frequency
            '1 hour',  # Tolerance
        ],
    )
    # Simulate contract creation
    mock_contract = mocker.patch('hari.cli.commands.cli.contract')
    # Simulate version
    mocker.patch('hari.cli.commands.cli.__version__', return_value='0.1.1')
    # Disable console print
    mock_create_yaml = mocker.patch(
        'hari.cli.commands.cli.create_yaml_from_dict'
    )

    # ---- Act ----
    result = runner.invoke(app, args, env={'NO_COLOR': '1'})

    # ---- Assert ----
    # Check success
    assert result.exit_code == 0
    # Check Output
    assert (
        'Contract test_contract created successfully!'
        in result_cleaned_norm(result.output)
    )
    # Check that the YAML file was created
    mock_create_yaml.assert_called_once()
    # Check parameters passed to the contract function
    mock_contract.assert_called_once_with(
        version=mocker.ANY,
        created_at=mocker.ANY,
        name='test_contract',
        description='',
        owner_email='',
        output_table={
            'name': 'test',
            'path': '/tmp',
            'format': 'csv',
        },
        columns=[
            {
                'name': 'col1',
                'type': 'string',
                'is_nullable': True,
                'is_unique': False,
            },
        ],
        sla={'frequency': 'daily', 'tolerance': '1 hour'},
    )
