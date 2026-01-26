from pydantic import BaseModel
from typing import Optional, List


class ClassificacaoRodadaBaseSchema(BaseModel):
    clr_id: int
    clr_serie: str
    clr_ano: int
    clr_rodada: Optional[str] = None
    clr_pontos: int
    clr_vitorias: int
    clr_saldo_gols: int
    clr_gols_pro: int
    clr_confronto_direto: int
    clr_vermelho_clube_clu_sigla: str
    clr_amarelo_clube_clu_sigla: str
    clube_clu_sigla: str


class CriarClassificacaoRodadaSchema(BaseModel):
    clr_serie: str
    clr_ano: int
    clr_rodada: Optional[str] = None
    clr_pontos: int
    clr_vitorias: int
    clr_saldo_gols: int
    clr_gols_pro: int
    clr_confronto_direto: int
    clr_vermelho_clube_clu_sigla: str
    clr_amarelo_clube_clu_sigla: str
    clube_clu_sigla: str
    clr_qtd_jogou: Optional[int] = None
    clr_qtd_empates: Optional[int] = None
    clr_qtd_derrotas: Optional[int] = None
    clr_gols_contra: Optional[int] = None


class AtualizarClassificacaoRodadaSchema(BaseModel):
    clr_pontos: Optional[int] = None
    clr_vitorias: Optional[int] = None
    clr_saldo_gols: Optional[int] = None
    clr_gols_pro: Optional[int] = None
    clr_confronto_direto: Optional[int] = None
    clr_vermelho_clube_clu_sigla: Optional[str] = None
    clr_amarelo_clube_clu_sigla: Optional[str] = None
    clr_qtd_jogou: Optional[int] = None
    clr_qtd_empates: Optional[int] = None
    clr_qtd_derrotas: Optional[int] = None
    clr_gols_contra: Optional[int] = None


class ResponseClassificacaoRodadaSchema(ClassificacaoRodadaBaseSchema):
    clr_qtd_jogou: Optional[int] = None
    clr_qtd_empates: Optional[int] = None
    clr_qtd_derrotas: Optional[int] = None
    clr_gols_contra: Optional[int] = None

    class Config:
        from_attributes = True


class ResponseClassificacoesRodadaSchema(BaseModel):
    classificacoes: List[ResponseClassificacaoRodadaSchema]

    class Config:
        from_attributes = True