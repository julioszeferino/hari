from rich.console import Console
from rich.prompt import Prompt
from typer import confirm, prompt

from hari.models.contrato import Contrato


def cria_estrutura_contrato(
    console: Console,
    nome_projeto: str,
) -> None:
    console.print('[bold green]Informe os dados do contrato:[/bold green]')
    descricao = prompt(
        'Descricao do contrato (digite enter para pular)', default=''
    )
    tabela_saida = prompt(
        'Nome da tabela de saida (ex: uri_catalogo, nome_arquivo)'
    )
    tabela_saida_formato = prompt(
        'Formato da tabela de saida (ex: parquet, csv)'
    )

    contrato_hari = Contrato(
        nome_projeto=nome_projeto,
        tabela_saida=tabela_saida,
        tabela_saida_formato=tabela_saida_formato,
    )

    if descricao:
        contrato_hari.descricao = descricao

    # adicao de colunas
    colunas = []
    while True:
        add_coluna = confirm(
            f'Deseja adicionar uma coluna a tabela {tabela_saida}?',
            default=bool(not colunas),
        )
        if not add_coluna:
            break
        coluna = {}
        coluna['nome'] = prompt('Nome da coluna')
        coluna['tipo'] = prompt('Tipo da coluna (ex: string, int, double)')
        if coluna['tipo'] in ['float', 'decimal', 'double']:
            coluna['precisao'] = prompt(
                'Tamanho da coluna (ex: 10, 20) ou digite enter para pular'
            )
        coluna['eh_nulo'] = confirm('A coluna pode ser nula?', default=True)
        coluna['eh_unico'] = confirm(
            'Os dados da coluna sao unicos?', default=False
        )
        colunas.append(coluna)
    contrato_hari.tabela_saida_colunas = colunas

    # deseja adicionar colunas de particao? Permitir selecionar entre cols
    if colunas:
        add_particao = confirm(
            'Deseja adicionar colunas de particao?', default=False
        )
        if add_particao:
            opcoes_colunas = [col['nome'] for col in colunas]
            colunas_particao = []
            colunas_disponiveis = opcoes_colunas.copy()
            while colunas_disponiveis:
                coluna_particao = Prompt.ask(
                    'Escolha uma coluna para particao (ou pressione Enter para finalizar)',
                    choices=colunas_disponiveis,
                    console=console,
                    default='',
                )
                if not coluna_particao:
                    break
                if coluna_particao in colunas_particao:
                    console.print(
                        f"[yellow]Coluna '{coluna_particao}' já selecionada.[/yellow]"
                    )
                else:
                    colunas_particao.append(coluna_particao)
                    colunas_disponiveis.remove(coluna_particao)
                    console.print(
                        f"[green]Coluna '{coluna_particao}' add como particao.[/green]"
                    )
                if not colunas_disponiveis:
                    console.print(
                        '[yellow]Todas as colunas já foram selecionadas.[/yellow]'
                    )
                    break
                continuar = confirm(
                    'Deseja adicionar outra coluna de particao?', default=False
                )
                if not continuar:
                    break
            if colunas_particao:
                contrato_hari.colunas_particao = colunas_particao
                console.print(
                    f"[green]Colunas selecionadas: {', '.join(colunas_particao)}[/green]"
                )
            else:
                console.print(
                    '[yellow]Nenhuma coluna de particao selecionada.[/yellow]'
                )

    owner_email = prompt(
        'Email do owner do contrato (digite enter para pular)', default=''
    )
    if owner_email:
        contrato_hari.owner_email = owner_email

    sla = confirm('Deseja adicionar SLA ao contrato?', default=False)
    if sla:
        frequencia_atualizacao = prompt(
            'Frequencia de atualizacao (ex: diaria, semanal, mensal)'
        )
        sla_tolerancia = prompt('Tolerancia do SLA (ex: 1 hora, 30 minutos)')
        contrato_hari.frequencia_atualizacao = frequencia_atualizacao
        contrato_hari.sla_tolerancia = sla_tolerancia
        contrato_hari.sla = True

    console.print('[bold green]Processando contrato:[/bold green]')
    contrato_hari.cria_contrato()

    console.print('[bold green]Salvando contrato:[/bold green]')
    contrato_hari.salvar_contrato()
