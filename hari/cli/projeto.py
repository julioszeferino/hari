import os
from typing import List, Tuple


def cria_estrutura_projeto(nome_projeto: str) -> Tuple[List[str], List[str]]:
    """
    Cria a estrutura de diretórios para um novo projeto
    Hari.

    Args:
        nome_projeto (str): Nome do projeto para o qual a
        estrutura será criada.

    Returns:
        Tuple[List[str], List[str]]: Retorna uma tupla contendo duas listas:
        - A lista de diretórios criados.
        - A lista de arquivos criados.
    """
    __DIRETORIOS = [
        'configs',
        'utils',
    ]

    __ARQUIVOS = [
        {
            'nome_dir_arquivo': 'configs/configs.json',
            'conteudo': (
                '# Este e um exemplo do arquivo configs.json.\n'
                '{{\n'
                '    "nome_projeto": "{}",\n'
                '    "versao": "1.0.0",\n'
                '    "log_level": "INFO",\n'
                '    "num_tentativas": 3,\n'
                '    "tabelas_entrada": [\n'
                '        {{\n'
                '            "path": "",  # ex: catalog uri, bucket path.\n'
                '            "formato": ""  # ex: parquet, csv, table, etc.\n'
                '        }}\n'
                '    ],\n'
                '    "tabelas_saida": [\n'
                '        {{\n'
                '            "path": "",  # ex: catalog uri, bucket path.\n'
                '            "formato": ""  # ex: parquet, csv, table, etc.\n'
                '        }}\n'
                '    ]\n'
                '}}\n'
            ).format(nome_projeto),
        },
        {
            'nome_dir_arquivo': 'utils/helpers.py',
            'conteudo': '# Este e um exemplo do arquivo utils/helpers.py\n',
        },
        {
            'nome_dir_arquivo': 'utils/validators.py',
            'conteudo': '# Este e um exemplo do arquivo \
                        utils/validators.py\n',
        },
        {
            'nome_dir_arquivo': 'job.py',
            'conteudo': '# Este e um exemplo do arquivo job.py\n',
        },
        {
            'nome_dir_arquivo': 'README.md',
            'conteudo': f'# {nome_projeto}\n',
        },
    ]

    diretorios_criados = []
    arquivos_criados = []

    for dir in __DIRETORIOS:
        dir_path = os.path.join(nome_projeto, dir)
        os.makedirs(dir_path, exist_ok=True)
        diretorios_criados.append(dir_path)

    for arquivo in __ARQUIVOS:
        path_arquivo = os.path.join(nome_projeto, arquivo['nome_dir_arquivo'])
        if not os.path.exists(path_arquivo):
            os.makedirs(os.path.dirname(path_arquivo), exist_ok=True)
            with open(path_arquivo, 'w') as f:
                f.write(arquivo['conteudo'])
        arquivos_criados.append(path_arquivo)

    return diretorios_criados, arquivos_criados
