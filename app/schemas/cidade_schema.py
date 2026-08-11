from pydantic import BaseModel, field_validator, PositiveInt, ConfigDict
from pydantic_core import PydanticCustomError
import re

REGEX_NOME = re.compile(r"^[A-Za-zÀ-ÿ\s\-']+$")
REGEX_UF = re.compile(r"^[A-Za-z]{2}$")

class CidadeCreate(BaseModel):
    """
    Schema Pydantic para criação de uma cidade.
    Inclui nome e UF da cidade.
    """
    cid_nome: str
    cid_uf: str

    @field_validator("cid_nome")
    @classmethod
    def _cid_nome(cls, v: str) -> str:
        if not v.strip():
            raise PydanticCustomError("Nome obrigatório", "Cidade é obrigatório.")
        if len(v) > 100:
            raise PydanticCustomError("Máximo de caracteres", "Cidade deve ter no máximo 100 caracteres.")
        if not REGEX_NOME.match(v):
            raise PydanticCustomError("Formato inválido", "Cidade contém caracteres inválidos.")
        return v
    

    @field_validator("cid_uf")
    @classmethod
    def _cid_uf(cls, v: str) -> str:
        if not v.strip():
            raise PydanticCustomError("UF obrigatório", "UF é obrigatório.")
        if len(v) != 2:
            raise PydanticCustomError("Máximo de caracteres", "UF deve ter exatamente 2 caracteres.")
        if not REGEX_UF.match(v):
            raise PydanticCustomError("Formato inválido", "UF contém caracteres inválidos.")
        return v

    class Config:
        from_attributes = True

class CidadeUpdate(CidadeCreate):
    cid_id: PositiveInt

    class Config:
        from_attributes = True

class CidadeOut(BaseModel):
    cid_id: int
    cid_nome: str
    cid_uf: str

    model_config = ConfigDict(from_attributes=True)