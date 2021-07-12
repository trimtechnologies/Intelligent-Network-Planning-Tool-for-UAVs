
import datetime

from models.base_model import BaseModel
from peewee import *


class BaseStation(BaseModel):
    """
    This class is the base station model for storage data in database
    """
    status: str = CharField()
    entidade: str = CharField()
    num_fistel: str = CharField()
    num_servico: str = CharField()
    num_ato_de_rf: str = CharField()
    num_estacao: str = CharField()
    endereco: str = CharField()
    uf: str = CharField()
    municipio: str = CharField()
    emissao: str = CharField()
    tecnologia: str = CharField()
    meio_acesso: str = CharField()
    frequencia_inicial: str = CharField()
    frequencia_final: str = CharField()
    azimute: str = CharField()
    tipo_estacao: str = CharField()
    classificacao_infra_fisica: str = CharField()
    compartilhamento_infra_fisica: str = CharField()
    disp_compartilhamento_infra: str = CharField()
    tipo_antena: str = CharField()
    homologacao_antena: str = CharField()
    ganho_antena: str = CharField()
    ganho_frente_costa: str = CharField()
    angulo_meia_potencia: str = CharField()
    elevacao: str = CharField()
    polarizacao: str = CharField()
    altura: str = CharField()
    homologacao_transmissao: str = CharField()
    potencia_transmissao: str = CharField()
    latitude: float = FloatField()
    longitude: float = FloatField()
    latitude_dms: str = CharField()
    longitude_dms: str = CharField()
    cod_debito_tfi: str = CharField()
    data_primeiro_licenciamento: str = CharField()
    color: str = CharField(default='blue')

    created_at: datetime = DateTimeField(default=datetime.datetime.now)


