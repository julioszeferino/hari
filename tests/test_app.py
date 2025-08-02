import os
import re
import shutil
import tempfile
from unittest.mock import Mock, patch

import pytest
from typer.testing import CliRunner

from hari.cli.app import app


def remove_ansi_codes(text: str) -> str:
    """Remove códigos de escape ANSI do texto."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class TestApp:
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

    @pytest.fixture
    def executor(self):
        """Cria um executor de comandos da app."""
        return CliRunner()

    def test_comando_novo_projeto_sucesso(self, temp_dir, executor):
        nome_projeto = 'teste_projeto'
        # executa o comando para criar um novo projeto
        # projeto novo teste_projeto
        resultado = executor.invoke(app, ['projeto', 'novo', nome_projeto])
        resultado_limpo = remove_ansi_codes(resultado.stdout)

        # Verifica se o comando foi executado com sucesso
        assert resultado.exit_code == 0

        # Verifica se a mensagem de sucesso aparece
        assert (
            f'Projeto "{nome_projeto}" criado com sucesso!' in resultado_limpo
        )
        assert 'Bons Codigos!' in resultado_limpo

        # Verifica se a tabela foi criada
        assert 'Diretorios e Arquivos Criados' in resultado_limpo
        assert 'Tipo' in resultado_limpo
        assert 'Nome' in resultado_limpo
        assert 'Diretorio' in resultado_limpo
        assert 'Arquivo' in resultado_limpo

    @patch('hari.cli.app.cria_estrutura_projeto')
    def test_comando_novo_projeto_erro(
        self, mock_cria_estrutura, temp_dir, executor
    ):
        nome_projeto = 'teste_projeto_erro'
        erro_simulado = Exception('Erro simulado para teste')

        # Configura o mock para levantar uma exceção
        mock_cria_estrutura.side_effect = erro_simulado

        # Executa o comando para criar um novo projeto
        resultado = executor.invoke(app, ['projeto', 'novo', nome_projeto])
        resultado_limpo = remove_ansi_codes(resultado.stdout)

        # Verifica se o comando falhou
        assert (
            resultado.exit_code == 0
        )  # Typer não altera exit_code por exceção capturada

        # Verifica se a mensagem de erro aparece
        assert (
            'Erro ao criar estrutura do projeto: Erro simulado para teste'
            in resultado_limpo
        )

        # Verifica que as mensagens de sucesso NÃO aparecem
        assert (
            f'Projeto "{nome_projeto}" criado com sucesso!'
            not in resultado_limpo
        )
        assert 'Bons Codigos!' not in resultado_limpo
        assert 'Diretorios e Arquivos Criados' not in resultado_limpo
