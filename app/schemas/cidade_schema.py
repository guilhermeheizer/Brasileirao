from pydantic import BaseModel
from typing import Optional
from typing import List

class CidadesSchema(BaseModel):
    cid_id: int
    cid_nome: str
    cid_uf: str

    class Config:
        from_attributes = True

class ResponseCidadesSchema(BaseModel):
    cidades: List[CidadesSchema]

    class Config:
        from_attributes = True