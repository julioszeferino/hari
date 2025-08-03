import os
from datetime import datetime
from typing import Dict, List, Optional

import yaml


class Contrato:
    def __init__(
        self,
        nome_projeto: str,
        tabela_saida: str,
        tabela_saida_formato: str,
        sla: bool = False,
        tabela_saida_particao: Optional[List[str]] = None,
        tabela_saida_path: Optional[str] = None,
        descricao: Optional[str] = None,
        owner_email: Optional[str] = None,
        frequencia_atualizacao: Optional[str] = None,
        sla_tolerancia: Optional[str] = None,
    ):
        self.__versao = '1.0.0'
        self.__data_criacao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.__nome_projeto = nome_projeto
        self.__descricao = descricao
        self.__owner_email = owner_email
        self.__tabela_saida = tabela_saida
        self.__tabela_saida_formato = tabela_saida_formato
        self.__tabela_saida_particao = tabela_saida_particao
        self.__tabela_saida_path = tabela_saida_path
        self.__tabela_saida_colunas = List[Dict[str, str]]
        self.__sla = sla
        self.__contrato = None

        if self.__sla:
            if not frequencia_atualizacao:
                raise ValueError('SLA deve ser definido se sla for True.')
            if not sla_tolerancia:
                raise ValueError(
                    'SLA tolerancia deve ser definido se sla for True.'
                )

            self.__frequencia_atualizacao = frequencia_atualizacao
            self.__sla_tolerancia = sla_tolerancia

    @property
    def tabela_saida_particao(self) -> Optional[List[str]]:
        return self.__tabela_saida_particao

    @tabela_saida_particao.setter
    def tabela_saida_particao(self, valor: str):
        self.__tabela_saida_particao = valor

    @property
    def tabela_saida_path(self) -> Optional[str]:
        return self.__tabela_saida_path

    @tabela_saida_path.setter
    def tabela_saida_path(self, valor: str):
        self.__tabela_saida_path = valor

    @property
    def descricao(self) -> Optional[str]:
        return self.__descricao

    @descricao.setter
    def descricao(self, valor: str):
        self.__descricao = valor

    @property
    def owner_email(self) -> Optional[str]:
        return self.__owner_email

    @owner_email.setter
    def owner_email(self, valor: str):
        self.__owner_email = valor

    @property
    def frequencia_atualizacao(self) -> Optional[str]:
        return self.__frequencia_atualizacao

    @frequencia_atualizacao.setter
    def frequencia_atualizacao(self, valor: str):
        self.__frequencia_atualizacao = valor

    @property
    def sla_tolerancia(self) -> Optional[str]:
        return self.__sla_tolerancia

    @sla_tolerancia.setter
    def sla_tolerancia(self, valor: str):
        self.__sla_tolerancia = valor

    @property
    def tabela_saida_colunas(self) -> List[Dict[str, str]]:
        return self.__tabela_saida_colunas

    @tabela_saida_colunas.setter
    def tabela_saida_colunas(self, colunas: List[Dict[str, str]]):
        self.__tabela_saida_colunas = colunas

    def cria_contrato(self) -> Dict[str, str]:
        __contrato = {
            'versao': self.__versao,
            'data_criacao': self.__data_criacao,
            'nome': self.__nome_projeto,
            'descricao': self.__descricao,
            'owner_email': self.__owner_email,
            'tabela_saida': {
                'nome': self.__tabela_saida,
                'formato': self.__tabela_saida_formato,
                'particao': self.__tabela_saida_particao,
                'path': self.__tabela_saida_path,
                'colunas': self.__tabela_saida_colunas,
            },
        }

        if self.__sla:
            __contrato['sla'] = {
                'frequencia_atualizacao': self.__frequencia_atualizacao,
                'sla_tolerancia': self.__sla_tolerancia,
            }

        self.__contrato = __contrato

    def salvar_contrato(self) -> None:
        try:
            if not self.__contrato:
                raise ValueError('Contrato nao foi criado.')
            # cria o diretorio
            dir_contrato = os.path.join(self.__nome_projeto, 'contratos')
            os.makedirs(dir_contrato, exist_ok=True)
            # salva yaml
            arquivo = os.path.join(dir_contrato, f'{self.__nome_projeto}.yaml')
            with open(arquivo, 'w') as f:
                yaml.dump(
                    self.__contrato, f, sort_keys=False, allow_unicode=True
                )
        except ValueError as e:
            raise ValueError(f'Erro ao salvar contrato: {e}')
        except Exception as e:
            raise Exception(f'Erro ao salvar contrato: {e}')
