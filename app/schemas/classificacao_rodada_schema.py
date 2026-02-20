"""
classificacao_rodada_schema.py

Este módulo define os schemas Pydantic para operações relacionadas à classificação por rodada do Campeonato Brasileiro.
Os schemas são utilizados para validação, serialização e documentação automática das rotas FastAPI.

Principais schemas:
- ClassificacaoRodadaBaseSchema: Base para classificação por rodada
- CriarClassificacaoRodadaSchema: Para criação de classificação por rodada
- AtualizarClassificacaoRodadaSchema: Para atualização de classificação por rodada
- ResponseClassificacaoRodadaSchema: Resposta detalhada de classificação por rodada
- ResponseClassificacoesRodadaSchema: Lista de classificações por rodada
"""
from pydantic import BaseModel
from typing import Optional, List


class ClassificacaoRodadaBaseSchema(BaseModel):
    """
    Schema base para classificação por rodada.
    Inclui informações essenciais como série, ano, rodada, pontos, vitórias, saldo de gols, gols pró, confronto direto e sigla do clube.
    """
    clr_id: int
    clr_serie: str
    clr_ano: int
    clr_rodada: Optional[str] = None
    clr_pontos: int
    clr_vitorias: int
    clr_saldo_gols: int
    clr_gols_pro: int
    clr_confronto_direto: int
    clube_clu_sigla: str


class CriarClassificacaoRodadaSchema(BaseModel):
    """
    Schema para criação de classificação por rodada.
    Utilizado para inserir novos registros de classificação por rodada.
    """
    clr_serie: str
    clr_ano: int
    clr_rodada: Optional[str] = None
    clr_pontos: int
    clr_vitorias: int
    clr_saldo_gols: int
    clr_gols_pro: int
    clr_confronto_direto: int
    clube_clu_sigla: str
    clr_qtd_jogou: Optional[int] = None
    clr_qtd_empates: Optional[int] = None
    clr_qtd_derrotas: Optional[int] = None
    clr_gols_contra: Optional[int] = None


class AtualizarClassificacaoRodadaSchema(BaseModel):
    """
    Schema para atualização de classificação por rodada.
    Utilizado para atualizar campos específicos de um registro de classificação por rodada.
    """
    clr_pontos: Optional[int] = None
    clr_vitorias: Optional[int] = None
    clr_saldo_gols: Optional[int] = None
    clr_gols_pro: Optional[int] = None
    clr_confronto_direto: Optional[int] = None
    clr_qtd_jogou: Optional[int] = None
    clr_qtd_empates: Optional[int] = None
    clr_qtd_derrotas: Optional[int] = None
    clr_gols_contra: Optional[int] = None


class ResponseClassificacaoRodadaSchema(ClassificacaoRodadaBaseSchema):
    """
    Schema de resposta detalhada de classificação por rodada.
    Inclui campos adicionais como quantidade de jogos, empates, derrotas e gols contra.
    """
    clr_qtd_jogou: Optional[int] = None
    clr_qtd_empates: Optional[int] = None
    clr_qtd_derrotas: Optional[int] = None
    clr_gols_contra: Optional[int] = None

    class Config:
        from_attributes = True


class ResponseClassificacoesRodadaSchema(BaseModel):
    """
    Schema de resposta contendo uma lista de classificações por rodada.
    Utilizado para retornar múltiplas classificações em respostas de API.
    """
    classificacoes: List[ResponseClassificacaoRodadaSchema]

    class Config:
        from_attributes = True