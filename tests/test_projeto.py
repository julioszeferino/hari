import os
import shutil
import tempfile

import pytest

from hari.cli.projeto import cria_estrutura_projeto


class TestProjeto:
    @pytest.fixture
    def temp_dir(self):
        # Cria diretorio temporario
        path_tmp = tempfile.mkdtemp()
        path_original = os.getcwd()
        # Muda o diretorio de trabalho para o temporario
        os.chdir(path_tmp)
        yield path_tmp
        # Retorna ao diretorio original
        os.chdir(path_original)
        # Remove o diretorio temporario
        shutil.rmtree(path_tmp)

    def test_diretorios_criados(self, temp_dir):
        nome_projeto = 'teste_projeto'
        diretorios_esperados = ['teste_projeto/configs', 'teste_projeto/utils']

        diretorios_criados, arquivos_criados = cria_estrutura_projeto(
            nome_projeto
        )

        for diretorio in diretorios_esperados:
            # Verifica se o diretório foi criado
            assert diretorio in diretorios_criados
            # Verifica se o diretório existe
            assert os.path.exists(diretorio)
            # Verifica se é um diretório
            assert os.path.isdir(diretorio)

    def test_arquivos_criados(self, temp_dir):
        nome_projeto = 'teste_projeto'
        arquivos_esperados = [
            'teste_projeto/configs/configs.json',
            'teste_projeto/utils/helpers.py',
            'teste_projeto/utils/validators.py',
            'teste_projeto/job.py',
            'teste_projeto/README.md',
        ]

        diretorios_criados, arquivos_criados = cria_estrutura_projeto(
            nome_projeto
        )

        for arquivo in arquivos_esperados:
            # Verifica se o arquivo foi criado
            assert arquivo in arquivos_criados
            # Verifica se o arquivo existe
            assert os.path.exists(arquivo)
            # Verifica se é um arquivo
            assert os.path.isfile(arquivo)
