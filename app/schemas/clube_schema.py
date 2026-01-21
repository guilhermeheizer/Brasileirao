from pydantic import BaseModel
from typing import List


class ClubeSchema(BaseModel):
    clu_sigla: str
    clu_nome: str
    clu_serie: str
    clu_link_escudo: str
    cidade_cid_id: int

    class Config:
        from_attributes = True


class ResponseClubeSchema(BaseModel):
    clubes: List[ClubeSchema]

    class Config:
        from_attributes = True

class ClubeCidadeSchema(BaseModel):
    clu_sigla: str
    clu_nome: str
    clu_serie: str
    clu_link_escudo: str
    cidade_cid_id: int
    cidade_nome: str
    cidade_uf: str

    class Config:
        from_attributes = True


class ResponseClubeCidadeSchema(BaseModel):
    clubes: List[ClubeCidadeSchema]

    class Config:
        from_attributes = True