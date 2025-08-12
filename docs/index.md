![project_logo](assets/logo.png){ width="300" .center }
# Hari
Hari is a Python library that helps automate several common data engineering tasks in PySpark environments. The library provides functions related to ingestion, loading, management, and data quality in data lakehouse environments with PySpark, and proposes a development model based on coding standards and data contracts.

It has two basic commands: `project` and `contract`

## How to create a new Hari project?
You can create a new project via the command line. For example:
```bash
poetry run hari project new project_name
```
Returning a list with the directories and files that were created.

```
           Created Directories and Files            
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Type      ┃ Name                                 ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Directory │ project_name/configs                 │
│ Directory │ project_name/utils                   │
│ File      │ project_name/configs/configs.json    │
│ File      │ project_name/utils/helpers.py        │
│ File      │ project_name/utils/validators.py     │
│ File      │ project_name/job.py                  │
│ File      │ project_name/README.md               │
└───────────┴──────────────────────────────────────┘
Project "project_name" created successfully!
Happy Coding!
```
## How to create a new Data Contract?
Data contracts are one of the main features of the Hari library. You can create a new contract via the command line. For example:
```bash
poetry run hari contract new project_name
```
Returning a series of questions about the data contract to be created.
```bash
Enter contract data:
Contract description (press enter to skip) []: My Example Contract
Output table name (e.g.: uri_catalog, file_name): catalog.schema.output_table_name
Output table format (e.g.: parquet, csv): delta
Do you want to add a column to table catalog.schema.output_table_name? [Y/n]: Y
Column name: column1
Column type (e.g.: string, int, double): string
Can the column be null? [Y/n]: n
Are the column values unique? [y/N]: y
Do you want to add a column to table catalog.schema.output_table_name? [y/N]: y
Column name: column2
Column type (e.g.: string, int, double): int
Can the column be null? [Y/n]: n
Are the column values unique? [y/N]: n
Do you want to add a column to table catalog.schema.output_table_name? [y/N]: y
Column name: column3
Column type (e.g.: string, int, double): double
Column size (e.g.: 10, 20) or press enter to skip: 10, 15
Can the column be null? [Y/n]: y
Are the column values unique? [y/N]: n
Do you want to add a column to table catalog.schema.output_table_name? [y/N]: y
Column name: column 3
Column type (e.g.: string, int, double): date
Can the column be null? [Y/n]: n
Are the column values unique? [y/N]: n
Do you want to add a column to table catalog.schema.output_table_name? [y/N]: n
Do you want to add partition columns? [y/N]: y
Choose a column for partitioning (or press Enter to finish) [column1/column2/column3/column 3] (): column2
Column 'column2' added as partition.
Do you want to add another partition column? [y/N]: n
Selected columns: column2
Contract owner email (press enter to skip) []: my@email.com
Do you want to add SLA to the contract? [y/N]: y
Update frequency (e.g.: daily, weekly, monthly): daily
SLA tolerance (e.g.: 1 hour, 30 minutes): 1 hour
Processing contract:
Saving contract:
```
Finally, a file will be created with the following model:
```yaml
version: 1.0.0
creation_date: '2025-08-03 14:42:40'
name: project_name
description: My Example Contract
owner_email: my@email.com
output_table:
  name: catalog.schema.output_table_name
  format: delta
  partition: null
  path: null
  columns:
  - name: column1
    type: string
    is_nullable: false
    is_unique: true
  - name: column2
    type: int
    is_nullable: false
    is_unique: false
  - name: column3
    type: double
    precision: 10, 15
    is_nullable: true
    is_unique: false
  - name: column 3
    type: date
    is_nullable: false
    is_unique: false
```
### Is it possible to have more than one data contract per project?
Yes. The idea is that you create one data contract for each output your project will generate.

### Is it possible to have data contracts for inputs?
Yes. However, I recommend evaluating whether it is really worth creating contracts for inputs. Prefer to create them in situations of great complexity where an unexpected change in the inputs would be detrimental to the process.

### Can I add more parameters to the contract after it is created?
Yes. Unfortunately, this has not yet been implemented via CLI. But you can edit the file content manually. To avoid incompatibility with new features that will be released, I recommend keeping at least the standard parameters, but feel free to add whatever you find necessary.

## More information about Hari
To discover other options, you can use the `--help` flag
```bash
poetry run hari --help
```
```bash
 Usage: hari [OPTIONS] COMMAND [ARGS]...                                                                                                                                                                                                                                                                     
                                                                                                                                                                                                                                                                                                             
╭─ Options ─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                                                                                                   │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                                                                                            │
│ --help                        Show this message and exit.                                                                                                                                                                                                                                                 │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ project    Manage Hari projects                                                                                                                                                                                                                                                                           │
│ contract   Manage Hari contracts                                                                                                                                                                                                                                                                          │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
