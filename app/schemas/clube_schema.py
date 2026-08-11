from pydantic import BaseModel, field_validator
from pydantic_core import PydanticCustomError
import re


REGEX_NOME = re.compile(r"^[A-Za-zÀ-ÿ\s\-']+$")


class ClubeSchema(BaseModel):
    clu_sigla: str
    clu_nome: str
    clu_serie: str
    clu_link_escudo: str
    cidade_cid_id: int
    
    @field_validator("clu_nome")
    @classmethod
    def _clu_nome(cls, v: str) -> str:
        if not v.strip():
            raise PydanticCustomError("Nome obrigatório", "Clube é obrigatório.")
        if len(v) > 100:
            raise PydanticCustomError("Máximo de caracteres", "Clube deve ter no máximo 100 caracteres.")
        if not REGEX_NOME.match(v):
            raise PydanticCustomError("Formato inválido", "Clube contém caracteres inválidos.")
        return v
    
    class Config:
        from_attributes = True

class ClubeUpdate(ClubeSchema):
    clu_sigla: str

class ResponseClubeSchema(ClubeSchema):
    class Config:
        from_attributes = True

class ClubeCidadeOut(BaseModel):
    clu_sigla: str
    clu_nome: str
    clu_serie: str
    clu_link_escudo: str
    cidade_cid_id: int
    cidade_nome: str
    cidade_uf: str

    class Config:
        from_attributes = True