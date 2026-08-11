from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Integer, ForeignKey, DateTime, text, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.clube_models import Clube


class ClassificacaoRodada(Base):
    __tablename__ = "classificacao_rodada"

    clr_id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True,
        autoincrement=True
    )  # ID da classificação
    
    clr_serie: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )  # Série do campeonato (A ou B)

    clr_ano: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Ano da competição

    clr_rodada: Mapped[Optional[str]] = mapped_column(
        String(45),
        nullable=True
    )  # Número ou descrição da rodada

    clr_pontos: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Pontos do clube

    clr_vitorias: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Número de vitórias

    clr_saldo_gols: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Saldo de gols

    clr_gols_pro: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Gols marcados ("gols pró")

    clr_confronto_direto: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Critério de confronto direto

    clube_clu_sigla: Mapped[str] = mapped_column(
        String(3),
        ForeignKey("clube.clu_sigla"),
        nullable=False
    )  # FK do clube

    clr_qtd_jogou: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Quantidade de jogos

    clr_qtd_empates: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Quantidade de empates

    clr_qtd_derrotas: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Quantidade de derrotas

    clr_gols_contra: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Gols sofridos ("gols contra")

    # Relacionamento com a tabela Clube
    clube: Mapped["Clube"] = relationship(
        "Clube",
        foreign_keys=[clube_clu_sigla]
    )

    def __init__(self, clr_serie, clr_ano, clr_rodada, clr_pontos, clr_vitorias, clr_saldo_gols,
                 clr_gols_pro, clr_confronto_direto, clube_clu_sigla, clr_qtd_jogou=None, clr_qtd_empates=None, 
                 clr_qtd_derrotas=None, clr_gols_contra=None):
        self.clr_serie = clr_serie
        self.clr_ano = clr_ano
        self.clr_rodada = clr_rodada
        self.clr_pontos = clr_pontos
        self.clr_vitorias = clr_vitorias
        self.clr_saldo_gols = clr_saldo_gols
        self.clr_gols_pro = clr_gols_pro
        self.clr_confronto_direto = clr_confronto_direto
        self.clube_clu_sigla = clube_clu_sigla
        self.clr_qtd_jogou = clr_qtd_jogou
        self.clr_qtd_empates = clr_qtd_empates
        self.clr_qtd_derrotas = clr_qtd_derrotas
        self.clr_gols_contra = clr_gols_contra

    def as_dict(self):
        return {
            "clr_id": self.clr_id,
            "clr_serie": self.clr_serie,
            "clr_ano": self.clr_ano,
            "clr_rodada": self.clr_rodada,
            "clr_pontos": self.clr_pontos,
            "clr_vitorias": self.clr_vitorias,
            "clr_saldo_gols": self.clr_saldo_gols,
            "clr_gols_pro": self.clr_gols_pro,
            "clr_confronto_direto": self.clr_confronto_direto,
            "clube_clu_sigla": self.clube_clu_sigla,
            "clr_qtd_jogou": self.clr_qtd_jogou,
            "clr_qtd_empates": self.clr_qtd_empates,
            "clr_qtd_derrotas": self.clr_qtd_derrotas,
            "clr_gols_contra": self.clr_gols_contra
        }