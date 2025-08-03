import os
import shutil
import tempfile

import pytest
import yaml

from hari.models.contrato import Contrato


class TestContrato:
    @pytest.fixture
    def temp_project_dir(self):
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)

    def test_cria_contrato_basico(self, temp_project_dir):
        contrato = Contrato(
            nome_projeto=temp_project_dir,
            tabela_saida='tabela1',
            tabela_saida_formato='parquet',
        )
        contrato.tabela_saida_colunas = [{'nome': 'col1', 'tipo': 'string'}]
        contrato.cria_contrato()
        assert contrato._Contrato__contrato is not None
        assert contrato._Contrato__contrato['nome'] == temp_project_dir
        assert (
            contrato._Contrato__contrato['tabela_saida']['nome'] == 'tabela1'
        )
        assert (
            contrato._Contrato__contrato['tabela_saida']['colunas'][0]['nome']
            == 'col1'
        )

    def test_propriedades_setters_getters(self):
        contrato = Contrato('proj', 'tab', 'csv')
        contrato.descricao = 'desc'
        contrato.owner_email = 'mail@x.com'
        contrato.frequencia_atualizacao = 'diaria'
        contrato.sla_tolerancia = '1h'
        contrato.tabela_saida_particao = ['col1', 'col2']
        contrato.tabela_saida_path = '/tmp'
        contrato.tabela_saida_colunas = [{'nome': 'c', 'tipo': 'int'}]
        assert contrato.descricao == 'desc'
        assert contrato.owner_email == 'mail@x.com'
        assert contrato.frequencia_atualizacao == 'diaria'
        assert contrato.sla_tolerancia == '1h'
        assert contrato.tabela_saida_particao == ['col1', 'col2']
        assert contrato.tabela_saida_path == '/tmp'
        assert contrato.tabela_saida_colunas == [{'nome': 'c', 'tipo': 'int'}]

    def test_cria_contrato_com_sla(self):
        contrato = Contrato(
            nome_projeto='p',
            tabela_saida='t',
            tabela_saida_formato='csv',
            sla=True,
            frequencia_atualizacao='mensal',
            sla_tolerancia='2h',
        )
        contrato.tabela_saida_colunas = []
        contrato.cria_contrato()
        assert 'sla' in contrato._Contrato__contrato
        assert (
            contrato._Contrato__contrato['sla']['frequencia_atualizacao']
            == 'mensal'
        )

    def test_cria_contrato_sla_sem_parametros(self):
        with pytest.raises(ValueError):
            Contrato(
                nome_projeto='p',
                tabela_saida='t',
                tabela_saida_formato='csv',
                sla=True,
            )

    def test_salvar_contrato_cria_arquivo(self, temp_project_dir):
        contrato = Contrato(
            nome_projeto=temp_project_dir,
            tabela_saida='saida',
            tabela_saida_formato='csv',
        )
        contrato.tabela_saida_colunas = [{'nome': 'col', 'tipo': 'int'}]
        contrato.cria_contrato()
        contrato.salvar_contrato()
        contrato_path = os.path.join(
            temp_project_dir, 'contratos', f'{temp_project_dir}.yaml'
        )
        assert os.path.exists(contrato_path)
        with open(contrato_path) as f:
            data = yaml.safe_load(f)
            assert data['tabela_saida']['nome'] == 'saida'

    def test_salvar_contrato_sem_criar(self):
        contrato = Contrato(
            nome_projeto='p', tabela_saida='t', tabela_saida_formato='csv'
        )
        with pytest.raises(ValueError):
            contrato.salvar_contrato()

    def test_salvar_contrato_erro_geral(self, monkeypatch):
        contrato = Contrato(
            nome_projeto='p', tabela_saida='t', tabela_saida_formato='csv'
        )
        contrato.tabela_saida_colunas = []
        contrato.cria_contrato()
        # Simula erro ao criar diretório
        monkeypatch.setattr(
            os,
            'makedirs',
            lambda *a, **kw: (_ for _ in ()).throw(Exception('fail')),
        )
        with pytest.raises(Exception) as excinfo:
            contrato.salvar_contrato()
        assert 'Erro ao salvar contrato' in str(excinfo.value)
