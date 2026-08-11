from pydantic import BaseModel, field_validator, PositiveInt
from pydantic_core import PydanticCustomError
import re


REGEX_NOME = re.compile(r"^[A-Za-zÀ-ÿ\s\-']+$")

class EstadioCreate(BaseModel):
    est_id: int
    est_nome: str
    cidade_cid_id: int

    @field_validator("est_nome")
    @classmethod
    def _est_nome(cls, v: str) -> str:
        if not v.strip():
            raise PydanticCustomError("Nome obrigatório", "Estádio é obrigatório.")
        if len(v) > 100:
            raise PydanticCustomError("Máximo de caracteres", "Estádio deve ter no máximo 100 caracteres.")
        if not REGEX_NOME.match(v):
            raise PydanticCustomError("Formato inválido", "Estádio contém caracteres inválidos.")
        return v

    class Config:
        from_attributes = True

class EstadioUpdate(EstadioCreate):
    est_id: PositiveInt

    class Config:
        from_attributes = True

class EstadioCidadeOut(BaseModel):
    est_id: int
    est_nome: str
    cidade_cid_id: int
    cidade_nome: str
    cidade_uf: str

    class Config:
        from_attributes = True