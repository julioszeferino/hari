from datetime import datetime
from typing import Dict, List, Optional

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from typer import Argument, Context, Exit, Option, Typer, confirm, prompt

from hari import __version__
from hari.cli.commands.contract import contract
from hari.cli.commands.project import project
from hari.utils.helpers import create_yaml_from_dict, is_hari_project

console = Console()
app = Typer()
app_contract = Typer()

app.add_typer(app_contract, name='contract', help='Manage data contracts.')

spark_type_options = [
    'string',
    'boolean',
    'byte',
    'short',
    'int',
    'bigint',
    'float',
    'double',
    'decimal',
    'date',
    'timestamp',
    'binary',
    'json',
    'time',
]


def version_callback(flag: bool):
    if flag:
        print(f'Hari CLI version: {__version__}')
        raise Exit(code=0)


@app.callback(invoke_without_command=True)
def main(
    ctx: Context,
    version: Optional[bool] = Option(
        None,
        '--version',
        '-v',
        help='Show the version of Hari CLI.',
        callback=version_callback,
        is_eager=True,
    ),
):
    message = """How to use: [b]hari [COMMAND] [ARGS][/]

    Available commands:

    - [b]create[/]: Create a new project.
    - [b]version[/]: Show the version of Hari CLI.
    - [b]help[/]: Show this message.

    [b]Examples[/]:
    hari create my_project

    hari --version

    For short descriptions, use [red]hari --help[/].
    For detailed help, read the docs!
    [blue][link=http://notas-musicais.readthedocs.io][/]
    """
    if ctx.invoked_subcommand:
        return
    console.print(message)


@app.command('create', help='Create a new project.')
def app_create_project(
    project_name: str = Argument(..., help='Name of the project to create.')
) -> None:

    dirs_files_created: Dict[str, List[str]] = project(project_name)

    table = Table(title='Directories and Files Created')
    table.add_column('Type', justify='left', style='cyan', no_wrap=True)
    table.add_column('Name', justify='left', style='magenta')

    for dir in dirs_files_created['dirs_created']:
        table.add_row('Directory', dir)

    for file in dirs_files_created['files_created']:
        table.add_row('File', file)

    console.print(table)
    console.print(f'\nProject [bold]{project_name}[/] created successfully!')
    console.print('Happy coding! :rocket:')


def add_columns() -> List[Dict[str, str]]:
    columns = []
    while True:
        add_column = confirm(
            'Do you want to add a column?', default=bool(not columns)
        )
        if not add_column:
            break
        column = {}
        column['name'] = prompt('Column name')
        column['type'] = prompt('Column type (e.g., string, int, double)')
        if column['type'] not in spark_type_options:
            console.print(f"[red]Invalid type '{column['type']}'.")
            console.print(
                f"Please choose from: {', '.join(spark_type_options)}[/red]"
            )
            continue
        column['is_nullable'] = confirm(
            'Can the column be null?', default=True
        )
        column['is_unique'] = confirm(
            'Is the data in the column unique?', default=False
        )
        columns.append(column)

    if len(columns) == 0:
        console.print(
            '[yellow]No columns added. Please add at least one column.[/yellow]'
        )
        columns = add_columns()
    return columns


@app_contract.command('new')
def app_contract_new(
    contract_name: str = Argument(..., help='Name of the contract.'),
    description: Optional[str] = Option(
        '',
        prompt='Description of the contract (optional)',
        help='Description of the contract.',
    ),
    owner_email: Optional[str] = Option(
        '',
        prompt='Email of the contract owner (optional)',
        help='Email of the contract owner.',
    ),
    output_table_name: Optional[str] = Option(
        ...,
        prompt='Name of the output table (e.g., table_name, file_name)',
        help='Name of the output table (e.g., table_name, file_name).',
    ),
    output_table_format: Optional[str] = Option(
        ...,
        prompt='Format of the output table (e.g., parquet, csv)',
        help='Format of the output table (e.g., parquet, csv).',
    ),
    output_table_path: Optional[str] = Option(
        ...,
        prompt='Path of the output table (e.g., uri_catalog, local_path)',
        help='Path of the output table (e.g., uri_catalog, local_path).',
    ),
    sla: Optional[str] = Option(
        'N',
        prompt='Do you want to add SLA details? [y/N]',
        help='Whether to add SLA details to the contract.',
    ),
) -> None:

    if not is_hari_project():
        console.print(
            '[red]This command must be run inside a Hari project.[/red]'
        )
        raise Exit(code=1)

    output_table_info = {}

    output_table_info['name'] = output_table_name
    output_table_info['path'] = output_table_path
    output_table_info['format'] = output_table_format
    output_table_columns = add_columns()

    if output_table_columns:
        add_partitions = confirm(
            'Do you want to add partition columns?', default=False
        )
        # TODO: Add validation for choice column not existing in output_table_columns
        if add_partitions:
            partition_columns = []
            available_columns = [col['name'] for col in output_table_columns]
            while available_columns:
                partition_column = Prompt.ask(
                    'Choose a column for partitioning (or press Enter to finish)',
                    choices=available_columns,
                    default='',
                )
                if not partition_column:
                    break
                if partition_column in partition_columns:
                    console.print(
                        f"[yellow]Column '{partition_column}' already selected.[/yellow]"
                    )
                else:
                    partition_columns.append(partition_column)
                    available_columns.remove(partition_column)

                    console.print(
                        f"[green]Column '{partition_column}' added as a partition.[/green]"
                    )
            output_table_info['partitioned_by'] = partition_columns

    if sla.lower() == 'y':
        sla_info = {}
        sla_info['frequency'] = prompt(
            'Frequency of updates (e.g., daily, weekly, monthly)'
        )
        sla_info['tolerance'] = prompt(
            'Tolerance for SLA (e.g., 1 hour, 30 minutes)'
        )
    else:
        sla_info = None

    console.print('Proceeding to create the contract...')
    contract_data = contract(
        version=__version__,
        created_at=datetime.now().strftime('%Y-%m-%d'),
        name=contract_name,
        description=description,
        owner_email=owner_email,
        output_table=output_table_info,
        columns=output_table_columns,
        sla=sla_info,
    )

    console.print('Saving contract data to YAML file...')
    create_yaml_from_dict(
        data=contract_data, dir='contracts', file_name=contract_name
    )
    console.print(f'Contract [bold]{contract_name}[/] created successfully!')
    console.print('Happy coding! :rocket:')
