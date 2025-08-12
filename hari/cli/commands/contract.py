from typing import (
    Dict,
    List,
    Optional,
)


def contract(
    version: str,
    created_at: str,
    name: str,
    output_table: Dict[str, str],
    columns: List[Dict[str, str]],
    description: Optional[str] = None,
    owner_email: Optional[str] = None,
    sla: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """
    Examples:
        >>> contract( # doctest: +SKIP
            version='0.1.0',
            name='example',
            description='This is an example contract.',
            owner_email='user@mail.com',
            output_table={
                'name': 'table_name',
                'path': 'catalog.schema.table_name',
                'format': 'delta',
                'partitioned_by': ['col1', 'col2'],
            },
            columns=[
                {'name': 'col1', 'type': 'string'},
                {'name': 'col2', 'type': 'integer'},
            ],
            sla={
                'frequency': 'daily',
                'tolerance': '22:00:00'
            }
        )
        {
            'hari_version': '0.1.0',
            'created_at': '2025-07-01',
            'name': 'example',
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
            'sla': {
                'frequency': 'daily',
                'tolerance': '22:00:00',
            },
        }
    """
    contract = {}
    contract['hari_version'] = version
    contract['created_at'] = created_at
    contract['name'] = name

    if description:
        contract['description'] = description

    if owner_email:
        contract['owner_email'] = owner_email

    contract['output_table'] = {
        'name': output_table.get('name', ''),
        'path': output_table.get('path', ''),
        'format': output_table.get('format', 'delta'),
        'partitioned_by': output_table.get('partitioned_by', []),
        'columns': columns,
    }

    if sla:
        contract['sla'] = {
            'frequency': sla.get('frequency', ''),
            'tolerance': sla.get('tolerance', ''),
        }

    return contract
