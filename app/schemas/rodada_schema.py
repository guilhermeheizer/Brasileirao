from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RodadaBaseSchema(BaseModel):
    rod_serie: str
    rod_ano: int
    rod_rodada: int
    rod_sequencia: int
    rod_data: datetime
    clube_clu_sigla_mandante: str
    clube_clu_sigla_visitante: str
    estadio_est_id: int


class CriarRodadaSchema(RodadaBaseSchema):
    rod_calculou_classificacao: Optional[str] = "N"
    rod_partida_finalidaza: Optional[str] = "N"


class AtualizarRodadaPlacarSchema(BaseModel):
    clube_clu_sigla_mandante: str
    rod_gols_mandante: int
    clube_clu_sigla_visitante: str
    rod_gols_visitante: int


class ResponseRodadaSchema(RodadaBaseSchema):
    rod_gols_mandante: Optional[int] = None
    rod_gols_visitante: Optional[int] = None
    rod_calculou_classificacao: Optional[str] = None
    rod_partida_finalidaza: Optional[str] = None

    class Config:
        from_attributes = True


class ResponseRodadasSchema(BaseModel):
    rodadas: List[ResponseRodadaSchema]

    class Config:
        from_attributes = True