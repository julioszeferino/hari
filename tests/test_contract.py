from hari.cli.commands.contract import contract


def test_contract_basic_params():
    # Arrange
    version = '0.1.0'
    created_at = '2025-07-01'
    name = 'contract_example'
    output_table = {
        'name': 'table_name',
        'path': 'catalog.schema.table_name',
        'format': 'delta',
        'partitioned_by': ['col1', 'col2'],
    }
    columns = [
        {'name': 'col1', 'type': 'string'},
        {'name': 'col2', 'type': 'integer'},
    ]
    expected_result = {
        'hari_version': '0.1.0',
        'created_at': '2025-07-01',
        'name': 'contract_example',
        'output_table': {
            'name': 'table_name',
            'path': 'catalog.schema.table_name',
            'format': 'delta',
            'partitioned_by': ['col1', 'col2'],
            'columns': [
                {'name': 'col1', 'type': 'string'},
                {'name': 'col2', 'type': 'integer'},
            ],
        },
    }

    # Act
    result = contract(
        version=version,
        created_at=created_at,
        name=name,
        output_table=output_table,
        columns=columns,
    )

    # Assert
    assert result == expected_result


def test_contract_full_params():
    # Arrange
    version = '0.1.0'
    created_at = '2025-07-01'
    name = 'contract_example'
    output_table = {
        'name': 'table_name',
        'path': 'catalog.schema.table_name',
        'format': 'delta',
        'partitioned_by': ['col1', 'col2'],
    }
    columns = [
        {'name': 'col1', 'type': 'string'},
        {'name': 'col2', 'type': 'integer'},
    ]
    description = 'This is an example contract.'
    owner_email = 'user@mail.com'
    sla = {'frequency': 'daily', 'tolerance': '22:00:00'}
    expected_result = {
        'hari_version': '0.1.0',
        'created_at': '2025-07-01',
        'name': 'contract_example',
        'description': 'This is an example contract.',
        'owner_email': 'user@mail.com',
        'output_table': {
            'name': 'table_name',
            'path': 'catalog.schema.table_name',
            'format': 'delta',
            'partitioned_by': ['col1', 'col2'],
            'columns': [
                {'name': 'col1', 'type': 'string'},
                {'name': 'col2', 'type': 'integer'},
            ],
        },
        'sla': {'frequency': 'daily', 'tolerance': '22:00:00'},
    }

    # Act
    result = contract(
        version=version,
        created_at=created_at,
        name=name,
        output_table=output_table,
        columns=columns,
        description=description,
        owner_email=owner_email,
        sla=sla,
    )

    # Assert
    assert result == expected_result


def test_contract_no_columns():
    pass


def test_contract_with_output_table_missing_fields():
    pass


def test_contract_with_sla_incomplete():
    pass


def test_contract_with_empty_column():
    pass
