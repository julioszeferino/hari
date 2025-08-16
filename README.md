<img src="https://hari-data.readthedocs.io/en/latest/assets/logo.png" width="200">

# Hari

[![Documentation Status](https://app.readthedocs.org/projects/hari-data/badge/?version=latest)](https://hari-data.readthedocs.io/en/latest/?badge=latest) 
![CI](https://github.com/julioszeferino/hari/actions/workflows/pipeline.yml/badge.svg) 
[![codecov](https://codecov.io/gh/julioszeferino/hari/graph/badge.svg?token=W55X6CYP96)](https://codecov.io/gh/julioszeferino/hari)



Hari is a Python library designed to establish a standardized pattern for developing PySpark applications, leveraging the concept of "data contracts" to ensure consistency, reliability, and maintainability in data engineering workflows.

All application operations are based on the `hari` command. This command has a subcommand for each action the application can perform, such as `create` and `contract`.

## How to Install

To install the CLI, it is recommended to use `pipx`:

```bash
pipx install hari
```

Although this is just a recommendation! You can also install the project using your preferred package manager, such as pip:

```bash
pip install hari
```

## How to create a new Hari project?

You can create a new project via the command line. For example:

```bash
hari create project_name
```

This command create a directory `project_name` and print this message:

```bash
          Directories and Files Created          
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Type      ┃ Name                              ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Directory │ project_name/configs              │
│ Directory │ project_name/utils                │
│ File      │ project_name/configs/configs.yaml │
│ File      │ project_name/utils/helpers.py     │
│ File      │ project_name/utils/validators.py  │
│ File      │ project_name/job.py               │
│ File      │ project_name/README.md            │
└───────────┴───────────────────────────────────┘

Project project_name created successfully!
Happy coding! 🚀
```

## How to create a new Data Contract?

Data contracts are one of the main features of the Hari library. To create a new contract, you must be inside a Hari project directory.

Run the following command:

```bash
hari contract new contract_name
```

You will be prompted for the following information:

- **Description** (optional): A description for your contract.
- **Owner email** (optional): The email of the contract owner.
- **Output table name**: Name of the output table (e.g., table_name, file_name).
- **Output table format**: Format of the output table (e.g., parquet, csv).
- **Output table path**: Path or URI for the output table.
- **Columns**: You will be able to add one or more columns, specifying name, type, nullability, uniqueness, and optionally size/precision.
- **Partitions**: Optionally, select columns to use as partitions.
- **SLA**: Optionally, add SLA details such as update frequency and tolerance.

Example session:

```bash
$ hari contract new sales_contract
Description of the contract (optional): Sales data contract
Email of the contract owner (optional): user@email.com
Name of the output table (e.g., table_name, file_name): sales.daily
Format of the output table (e.g., parquet, csv): parquet
Path of the output table (e.g., uri_catalog, local_path): /data/sales
Do you want to add a column? [Y/n]: Y
Column name: sale_id
Column type (e.g., string, int, double): int
Can the column be null? [Y/n]: n
Are the column values unique? [y/N]: y
# ...repeat for more columns...
Do you want to add partition columns? [y/N]: y
Choose a column for partitioning (or press Enter to finish): sale_id
Do you want to add another partition column? [y/N]: n
Do you want to add SLA details? [y/N]: y
Frequency of updates (e.g., daily, weekly, monthly): daily
Tolerance for SLA (e.g., 1 hour, 30 minutes): 1 hour
Proceeding to create the contract...
Saving contract data to YAML file...
Contract sales_contract created successfully!
Happy coding! 🚀
```

Example session with interactive prompts:

```bash
$ hari contract new sales_contract
Description of the contract (optional): Sales data contract
Email of the contract owner (optional): user@email.com
Name of the output table (e.g., table_name, file_name): sales.daily
Format of the output table (e.g., parquet, csv): parquet
Path of the output table (e.g., uri_catalog, local_path): /data/sales

Do you want to add a column? [Y/n]: Y
Column name: sale_id
Column type (e.g., string, int, double): int
Can the column be null? [Y/n]: n
Are the column values unique? [y/N]: y

Do you want to add a column? [y/N]: y
Column name: sale_date
Column type (e.g., string, int, double): date
Can the column be null? [Y/n]: n
Are the column values unique? [y/N]: n

Do you want to add partition columns? [y/N]: y
Choose a column for partitioning (or press Enter to finish): sale_date
Do you want to add another partition column? [y/N]: n

Do you want to add SLA details? [y/N]: y
Frequency of updates (e.g., daily, weekly, monthly): daily
Tolerance for SLA (e.g., 1 hour, 30 minutes): 1 hour

Proceeding to create the contract...
Saving contract data to YAML file...
Contract sales_contract created successfully!
Happy coding! 🚀
```

You can also use command-line options to provide values directly, skipping the interactive prompts. For example:

```bash
hari contract new sales_contract \
  --description "Sales data contract" \
  --owner-email "user@email.com" \
  --output-table-name "sales.daily" \
  --output-table-format parquet \
  --output-table-path "/data/sales"
```

If you provide all required options, the command will not prompt for those values interactively. You will still be prompted for columns, partitions, and SLA unless you provide those through additional options (if supported).

The contract will be saved as a YAML file in the `contracts` directory of your project.

Example of a generated contract YAML file:

```yaml
version: 1.0.0
creation_date: '2025-08-03'
name: sales_contract
description: Sales data contract
owner_email: user@email.com
output_table:
  name: sales.daily
  format: parquet
  path: /data/sales
  partitioned_by:
    - sale_date
  columns:
    - name: sale_id
      type: int
      is_nullable: false
      is_unique: true
    - name: sale_date
      type: date
      is_nullable: false
      is_unique: false
sla:
  frequency: daily
  tolerance: 1 hour
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
hari --help
```
```bash
 Usage: hari [OPTIONS] COMMAND [ARGS]...         

╭─ Commands ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ create     Create a new project.                                                                                                                                                                                                                    │
│ contract   Manage data contracts.                                                                                                                                                                                                                   │
╰─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```
