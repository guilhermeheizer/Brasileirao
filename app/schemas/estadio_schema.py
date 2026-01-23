from pydantic import BaseModel
from typing import List


class EstadioSchema(BaseModel):
    est_id: int
    est_nome: str
    cidade_cid_id: int

    class Config:
        from_attributes = True
   
class ResponseEstadioSchema(BaseModel):
    estadios: List[EstadioSchema]

    class Config:
        from_attributes = True

class EstadioCidadeSchema(BaseModel):
    est_id: int
    est_nome: str
    cidade_cid_id: int
    cidade_nome: str
    cidade_uf: str

    class Config:
        from_attributes = True


class ResponseEstadioCidadeSchema(BaseModel):
    estadios: List[EstadioCidadeSchema]

    class Config:
        from_attributes = True