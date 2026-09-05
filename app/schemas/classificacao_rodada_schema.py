"""
classificacao_rodada_schema.py

Este módulo define os schemas Pydantic para operações relacionadas à classificação por rodada do Campeonato Brasileiro.
Os schemas são utilizados para validação, serialização e documentação automática das rotas FastAPI.
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
    clr_qtd_jogou: Optional[int] = None
    clr_qtd_empates: Optional[int] = None
    clr_qtd_derrotas: Optional[int] = None
    clr_gols_contra: Optional[int] = None