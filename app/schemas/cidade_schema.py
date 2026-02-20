"""
cidade_schema.py

Este módulo define os schemas Pydantic para operações relacionadas às cidades no contexto do Campeonato Brasileiro.
Os schemas são utilizados para validação, serialização e documentação automática das rotas FastAPI.

Principais schemas:
- CidadesSchema: Representa uma cidade individual
- ResponseCidadesSchema: Representa uma resposta com lista de cidades
"""
from pydantic import BaseModel
from typing import Optional
from typing import List

class CidadesSchema(BaseModel):
    """
    Schema Pydantic que representa uma cidade.
    Inclui id, nome e UF da cidade.
    """
    cid_id: int
    cid_nome: str
    cid_uf: str

    class Config:
        from_attributes = True

class ResponseCidadesSchema(BaseModel):
    """
    Schema de resposta contendo uma lista de cidades.
    Utilizado para retornar múltiplas cidades em respostas de API.
    """
    cidades: List[CidadesSchema]

    class Config:
        from_attributes = True