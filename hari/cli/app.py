from rich.console import Console
from rich.table import Table
from typer import Argument, Typer

from hari.cli.projeto import cria_estrutura_projeto

console = Console()
app = Typer()
__app_projeto = Typer()

app.add_typer(__app_projeto, name='projeto', help='Gerencia projetos Hari')


@__app_projeto.command('novo')
def app_cria_estrutura_projeto(
    nome_projeto: str = Argument(
        ..., help='Nome do projeto para o qual a estrutura será criada.'
    )
):
    """

    Cria a estrutura de diretórios para um novo projeto Hari.
    ex: hari projeto novo nome_projeto

    Args:
        nome_projeto (str): Nome do projeto para o qual a estrutura
        será criada.
    """
    try:
        diretorios_criados, arquivos_criados = cria_estrutura_projeto(
            nome_projeto
        )

        # Cria tabela para exibir os diretórios e arquivos criados
        __tabela = Table(title='Diretorios e Arquivos Criados')
        __tabela.add_column('Tipo', justify='left', style='cyan', no_wrap=True)
        __tabela.add_column('Nome', justify='left', style='magenta')

        # Adiciona diretórios à tabela
        for diretorio in diretorios_criados:
            __tabela.add_row('Diretorio', diretorio)

        # Adiciona arquivos à tabela
        for arquivo in arquivos_criados:
            __tabela.add_row('Arquivo', arquivo)

        # Exibe a tabela no console
        console.print(__tabela)
        console.print(
            f'[green]Projeto "{nome_projeto}" criado com sucesso![/green]'
        )
        console.print('[green]Bons Codigos![/green]')

    except Exception as e:
        console.print(f'[red]Erro ao criar estrutura do projeto: {e}[/red]')


if __name__ == '__main__':  # pragma: no cover
    app()  # pragma: no cover
