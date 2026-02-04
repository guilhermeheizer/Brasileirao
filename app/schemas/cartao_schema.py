from pydantic import BaseModel
from typing import Optional, List


class CartaoSchema(BaseModel):
    car_serie: str
    car_ano: int
    clube_clu_sigla: str
    car_qtd_vermelho: Optional[int] = 0
    car_qtd_amarelo: Optional[int] = 0

    class Config:
        from_attributes = True

class ResponseCartaoSchema(BaseModel):
    cartoes: List[CartaoSchema]

    class Config:
        from_attributes = True

class CartaoClubeSchema(BaseModel):
    car_serie: str
    car_ano: int
    clube_clu_sigla: str
    clube_link_escudo: str
    clube_nome: str
    car_qtd_vermelho: Optional[int] = 0
    car_qtd_amarelo: Optional[int] = 0

    class Config:
        from_attributes = True

class ResponseCartaoClubeSchema(BaseModel):
    cartoes: List[CartaoClubeSchema]

    class Config:
        from_attributes = True