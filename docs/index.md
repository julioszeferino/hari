![logo_do_projeto](assets/logo.png){ width="300" .center }
# Hari
Hari é uma biblioteca Python que auxilia na automação de diversas tarefas comuns de engenharia de dados em ambientes PySpark. A biblioteca possui funções relacionadas à ingestão, carga, gerenciamento e qualidade de dados em ambientes de data lakehouse com PySpark, e propõe um modelo de desenvolvimento baseado em padrões de codificação e contratos de dados.

## Como criar um novo projeto Hari?
Você pode criar um novo projeto via linha de comando. Por exemplo: 
```bash
poetry run hari projeto novo nome_do_projeto
```
Retornando uma lista com os diretórios e arquivos que foram criados.

```
           Diretorios e Arquivos Criados            
┏━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Tipo      ┃ Nome                                 ┃
┡━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Diretorio │ nome_do_projeto/configs              │
│ Diretorio │ nome_do_projeto/utils                │
│ Arquivo   │ nome_do_projeto/configs/configs.json │
│ Arquivo   │ nome_do_projeto/utils/helpers.py     │
│ Arquivo   │ nome_do_projeto/utils/validators.py  │
│ Arquivo   │ nome_do_projeto/job.py               │
│ Arquivo   │ nome_do_projeto/README.md            │
└───────────┴──────────────────────────────────────┘
Projeto "nome_do_projeto" criado com sucesso!
Bons Codigos!
```
## Como criar um novo Contrato de Dados?
Os contratos de dados são uma das principais funcionalidades da biblioteca Hari. Você pode criar um novo contrato via linha de comando. Por exemplo:
```bash
poetry run hari contrato novo nome_do_projeto
```
Retornando uma série de questionamentos sobre o contrato de dados que será criado.
```bash
Informe os dados do contrato:
Descricao do contrato (digite enter para pular) []: Meu Contrato Exemplo
Nome da tabela de saida (ex: uri_catalogo, nome_arquivo): catalogo.schema.nome_tabela_saida
Formato da tabela de saida (ex: parquet, csv): delta
Deseja adicionar uma coluna a tabela catalogo.schema.nome_tabela_saida? [Y/n]: Y
Nome da coluna: coluna1
Tipo da coluna (ex: string, int, double): string
A coluna pode ser nula? [Y/n]: n
Os dados da coluna sao unicos? [y/N]: y
Deseja adicionar uma coluna a tabela catalogo.schema.nome_tabela_saida? [y/N]: y
Nome da coluna: coluna2
Tipo da coluna (ex: string, int, double): int
A coluna pode ser nula? [Y/n]: n
Os dados da coluna sao unicos? [y/N]: n
Deseja adicionar uma coluna a tabela catalogo.schema.nome_tabela_saida? [y/N]: y
Nome da coluna: coluna3
Tipo da coluna (ex: string, int, double): double
Tamanho da coluna (ex: 10, 20) ou digite enter para pular: 10, 15
A coluna pode ser nula? [Y/n]: y
Os dados da coluna sao unicos? [y/N]: n
Deseja adicionar uma coluna a tabela catalogo.schema.nome_tabela_saida? [y/N]: y
Nome da coluna: coluna 3
Tipo da coluna (ex: string, int, double): date
A coluna pode ser nula? [Y/n]: n
Os dados da coluna sao unicos? [y/N]: n
Deseja adicionar uma coluna a tabela catalogo.schema.nome_tabela_saida? [y/N]: n
Deseja adicionar colunas de particao? [y/N]: y
Escolha uma coluna para particao (ou pressione Enter para finalizar) [coluna1/coluna2/coluna3/coluna 3] (): coluna2
Coluna 'coluna2' add como particao.
Deseja adicionar outra coluna de particao? [y/N]: n
Colunas selecionadas: coluna2
Email do owner do contrato (digite enter para pular) []: meu@email.com.br
Deseja adicionar SLA ao contrato? [y/N]: y
Frequencia de atualizacao (ex: diaria, semanal, mensal): diaria
Tolerancia do SLA (ex: 1 hora, 30 minutos): 1 hora
Processando contrato:
Salvando contrato:
```
Por fim, será criado um arquivo com o modelo abaixo:
```yaml
versao: 1.0.0
data_criacao: '2025-08-03 14:42:40'
nome: nome_do_projeto
descricao: Meu Contrato Exemplo
owner_email: meu@email.com.br
tabela_saida:
  nome: catalogo.schema.nome_tabela_saida
  formato: delta
  particao: null
  path: null
  colunas:
  - nome: coluna1
    tipo: string
    eh_nulo: false
    eh_unico: true
  - nome: coluna2
    tipo: int
    eh_nulo: false
    eh_unico: false
  - nome: coluna3
    tipo: double
    precisao: 10, 15
    eh_nulo: true
    eh_unico: false
  - nome: coluna 3
    tipo: date
    eh_nulo: false
    eh_unico: false
```
### É possível ter mais de um contrato de dados por projeto?
Sim. A ideia é que você crie 1 contrato de dados para cada saída que o seu projeto vá gerar.

### É possível ter contratos de dados para as entradas?
Sim. Contudo, recomendo que avalie se vale realmente a pena criar contratos para as entradas. Prefira criá-los em situações de grande complexidade onde uma alteração inesperada nas entradas seria prejudicial para o processo.

### Eu posso adicionar mais parâmetros ao contrato após ser criado?
Sim. Infelizmente isso ainda não foi implementado via CLI. Mas você pode editar o conteúdo do arquivo manualmente. Para que não haja incompatibilidade com as novas funcionalidades que serão lançadas recomendo que mantenha ao menos os parâmetros padrão, mas fique livre para adicionar o que achar necessário.

## Mais informações sobre o Hari
Para descobrir outras opções, você pode utilizar a flag `--help`
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
│ projeto    Gerencia projetos Hari                                                                                                                                                                                                                                                                         │
│ contrato   Gerencia contratos Hari                                                                                                                                                                                                                                                                        │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```
