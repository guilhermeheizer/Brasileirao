from pydantic import BaseModel
from typing import Optional, List


class ClassificacaoGeralBaseSchema(BaseModel):
    clg_id: int
    clg_serie: str
    clg_ano: int
    clg_pontos: int
    clg_vitorias: int
    clg_saldo_gols: int
    clg_gols_pro: int
    clg_confronto_direto: int
    clg_vermelho_clube_clu_sigla: str
    clg_amarelo_clube_clu_sigla: str
    clube_clu_sigla: str


class CriarClassificacaoGeralSchema(BaseModel):
    clg_serie: str
    clg_ano: int
    clg_pontos: int
    clg_vitorias: int
    clg_saldo_gols: int
    clg_gols_pro: int
    clg_confronto_direto: int
    clg_vermelho_clube_clu_sigla: str
    clg_amarelo_clube_clu_sigla: str
    clube_clu_sigla: str
    clg_qtd_jogou: Optional[int] = None
    clg_qtd_empates: Optional[int] = None
    clg_qtd_derrotas: Optional[int] = None
    clg_gols_contra: Optional[int] = None


class AtualizarClassificacaoGeralSchema(BaseModel):
    clg_pontos: Optional[int] = None
    clg_vitorias: Optional[int] = None
    clg_saldo_gols: Optional[int] = None
    clg_gols_pro: Optional[int] = None
    clg_confronto_direto: Optional[int] = None
    clg_vermelho_clube_clu_sigla: Optional[str] = None
    clg_amarelo_clube_clu_sigla: Optional[str] = None
    clg_qtd_jogou: Optional[int] = None
    clg_qtd_empates: Optional[int] = None
    clg_qtd_derrotas: Optional[int] = None
    clg_gols_contra: Optional[int] = None


class ResponseClassificacaoGeralSchema(ClassificacaoGeralBaseSchema):
    clg_qtd_jogou: Optional[int] = None
    clg_qtd_empates: Optional[int] = None
    clg_qtd_derrotas: Optional[int] = None
    clg_gols_contra: Optional[int] = None

    class Config:
        from_attributes = True


class ResponseClassificacoesGeraisSchema(BaseModel):
    classificacoes: List[ResponseClassificacaoGeralSchema]

    class Config:
        from_attributes = True