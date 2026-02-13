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
    clube_clu_sigla: str


class CriarClassificacaoGeralSchema(BaseModel):
    clg_serie: str
    clg_ano: int
    clg_pontos: int
    clg_vitorias: int
    clg_saldo_gols: int
    clg_gols_pro: int
    clg_confronto_direto: int
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


class ResponseClassificacaoGeralListaSchema(BaseModel):
    ordem_classificacao: int
    clube_clu_sigla: str
    clu_nome: str
    clu_link_escudo: str
    clg_pontos: int
    clg_qtd_jogou: int
    clg_vitorias: int
    clg_qtd_empates: int
    clg_qtd_derrotas: int
    clg_gols_pro: int
    clg_gols_contra: int
    clg_saldo_gols: int
    car_qtd_amarelo: int
    car_qtd_vermelho: int

    class Config:
        from_attributes = True