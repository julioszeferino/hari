from unittest.mock import MagicMock, patch

import pytest

from hari.cli import contrato_dados


class TestCriaEstruturaContrato:
    @pytest.fixture
    def mock_console(self):
        return MagicMock()

    def test_cria_estrutura_contrato_fluxo_basico(self, mock_console):
        respostas = iter(
            [
                '',  # descricao
                'tabela_saida',  # tabela_saida
                'parquet',  # tabela_saida_formato
                True,  # add_coluna
                'col1',  # nome coluna
                'string',  # tipo coluna
                True,  # eh_nulo
                False,  # eh_unico
                False,  # add_coluna (encerra)
                False,  # add_particao
                '',  # owner_email
                False,  # sla
            ]
        )
        with patch(
            'hari.cli.contrato_dados.prompt',
            side_effect=lambda *a, **k: next(respostas),
        ), patch(
            'hari.cli.contrato_dados.confirm',
            side_effect=lambda *a, **k: next(respostas),
        ), patch(
            'hari.cli.contrato_dados.Contrato'
        ) as MockContrato:
            mock_contrato = MockContrato.return_value
            contrato_dados.cria_estrutura_contrato(mock_console, 'projeto1')
            assert mock_contrato.cria_contrato.called
            assert mock_contrato.salvar_contrato.called

    def test_cria_estrutura_contrato_com_particao(self, mock_console):
        respostas = iter(
            [
                '',  # descricao
                'tabela_saida',
                'csv',
                True,  # add_coluna
                'col1',
                'int',
                True,
                False,
                True,  # add_coluna
                'col2',
                'string',
                True,
                False,
                False,  # add_coluna (encerra)
                True,  # add_particao
                'col1',  # Prompt.ask - partição 1
                False,  # continuar partição
                '',  # owner_email
                False,  # sla
            ]
        )
        with patch(
            'hari.cli.contrato_dados.prompt',
            side_effect=lambda *a, **k: next(respostas),
        ), patch(
            'hari.cli.contrato_dados.confirm',
            side_effect=lambda *a, **k: next(respostas),
        ), patch(
            'hari.cli.contrato_dados.Prompt.ask',
            side_effect=lambda *a, **k: next(respostas),
        ), patch(
            'hari.cli.contrato_dados.Contrato'
        ) as MockContrato:
            mock_contrato = MockContrato.return_value
            contrato_dados.cria_estrutura_contrato(mock_console, 'projeto2')
            assert hasattr(mock_contrato, 'colunas_particao')
            assert mock_contrato.cria_contrato.called
            assert mock_contrato.salvar_contrato.called

    def test_cria_estrutura_contrato_com_sla(self, mock_console):
        respostas = iter(
            [
                '',  # descricao
                'tabela_saida',
                'csv',
                True,  # add_coluna
                'col1',
                'int',
                True,
                False,
                False,  # add_coluna (encerra)
                False,  # add_particao
                '',  # owner_email
                True,  # sla
                'diaria',  # frequencia_atualizacao
                '1 hora',  # sla_tolerancia
            ]
        )
        with patch(
            'hari.cli.contrato_dados.prompt',
            side_effect=lambda *a, **k: next(respostas),
        ), patch(
            'hari.cli.contrato_dados.confirm',
            side_effect=lambda *a, **k: next(respostas),
        ), patch(
            'hari.cli.contrato_dados.Contrato'
        ) as MockContrato:
            mock_contrato = MockContrato.return_value
            contrato_dados.cria_estrutura_contrato(mock_console, 'projeto3')
            assert mock_contrato.cria_contrato.called
            assert mock_contrato.salvar_contrato.called
            assert mock_contrato.sla is True
            assert mock_contrato.frequencia_atualizacao == 'diaria'
            assert mock_contrato.sla_tolerancia == '1 hora'
