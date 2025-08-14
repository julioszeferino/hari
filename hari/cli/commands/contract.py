"""
Module for creating data contracts in the Hari CLI.
"""

from typing import Any  # Adicionado
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
) -> Dict[str, Any]:
    """
    Create a data contract dictionary.

    Parameters:
        version (str): The version of the Hari library.
        created_at (str): The creation date of the contract.
        name (str): The name of the contract.
        output_table (Dict[str, str]): Information about the output table, including
                    name, path, format, and partition columns.
        columns (List[Dict[str, str]]): List of column definitions for the output table.
        description (Optional[str], optional): Description of the contract. Defaults to None.
        owner_email (Optional[str], optional): Email of the contract owner. Defaults to None.
        sla (Optional[Dict[str, str]], optional): SLA information,
                such as frequency and tolerance. Defaults to None.

    Returns:
        Dict[str, Any]: A dictionary representing the data contract.

    Examples:
        >>> contract( # doctest: +SKIP
        ...     version='0.1.0',
        ...     created_at='2025-07-01',
        ...     name='example',
        ...     description='This is an example contract.',
        ...     owner_email='user@mail.com',
        ...     output_table={
        ...         'name': 'table_name',
        ...         'path': 'catalog.schema.table_name',
        ...         'format': 'delta',
        ...         'partitioned_by': ['col1', 'col2'],
        ...     },
        ...     columns=[
        ...         {'name': 'col1', 'type': 'string'},
        ...         {'name': 'col2', 'type': 'integer'},
        ...     ],
        ...     sla={
        ...         'frequency': 'daily',
        ...         'tolerance': '22:00:00'
        ...     }
        ... )
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
