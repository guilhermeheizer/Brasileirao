from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, Integer, ForeignKey, DateTime, text, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.clube_models import Clube


class ClassificacaoGeral(Base):
    __tablename__ = "classificacao_geral"

    clg_id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True,
        autoincrement=True
    )  # ID da classificação geral

    clg_serie: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )  # Série do campeonato (A ou B)

    clg_ano: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Ano da competição

    clg_pontos: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Pontuação total do clube

    clg_vitorias: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Número total de vitórias

    clg_saldo_gols: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Saldo total de gols

    clg_gols_pro: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Total de gols marcados ("gols pró")

    clg_confronto_direto: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )  # Critério de confronto direto

    clube_clu_sigla: Mapped[str] = mapped_column(
        String(3),
        ForeignKey("clube.clu_sigla"),
        nullable=False
    )  # FK Clube

    clg_qtd_jogou: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Total de jogos disputados

    clg_qtd_empates: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Total de empates

    clg_qtd_derrotas: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Total de derrotas
    
    clg_gols_contra: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Total de gols sofridos

    clg_posicao: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Posição na classificacao

    car_qtd_vermelho: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Cartões vermelhos

    car_qtd_amarelo: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True
    )  # Cartões amarelos

    # Relacionamento com a tabela Clube
    clube: Mapped["Clube"] = relationship(
        "Clube",
        foreign_keys=[clube_clu_sigla]
    )

    def __init__(self, clg_serie, clg_ano, clg_pontos, clg_vitorias, clg_saldo_gols, clg_gols_pro, 
                 clg_confronto_direto, clube_clu_sigla, clg_qtd_jogou=None, clg_qtd_empates=None, 
                 clg_qtd_derrotas=None, clg_gols_contra=None, clg_posicao=None, car_qtd_vermelho=None, 
                 car_qtd_amarelo=None):
        self.clg_serie = clg_serie
        self.clg_ano = clg_ano
        self.clg_pontos = clg_pontos
        self.clg_vitorias = clg_vitorias
        self.clg_saldo_gols = clg_saldo_gols
        self.clg_gols_pro = clg_gols_pro
        self.clg_confronto_direto = clg_confronto_direto
        self.clube_clu_sigla = clube_clu_sigla
        self.clg_qtd_jogou = clg_qtd_jogou
        self.clg_qtd_empates = clg_qtd_empates
        self.clg_qtd_derrotas = clg_qtd_derrotas
        self.clg_gols_contra = clg_gols_contra
        self.clg_posicao = clg_posicao
        self.car_qtd_vermelho = car_qtd_vermelho
        self.car_qtd_amarelo = car_qtd_amarelo

    def as_dict(self):
        return {
            "clg_id": self.clg_id,
            "clg_serie": self.clg_serie,
            "clg_ano": self.clg_ano,
            "clg_pontos": self.clg_pontos,
            "clg_vitorias": self.clg_vitorias,
            "clg_saldo_gols": self.clg_saldo_gols,
            "clg_gols_pro": self.clg_gols_pro,
            "clg_confronto_direto": self.clg_confronto_direto,
            "clube_clu_sigla": self.clube_clu_sigla,
            "clg_qtd_jogou": self.clg_qtd_jogou,
            "clg_qtd_empates": self.clg_qtd_empates,
            "clg_qtd_derrotas": self.clg_qtd_derrotas,
            "clg_gols_contra": self.clg_gols_contra,
            "clg_posicao": self.clg_posicao,
            "car_qtd_vermelho": self.car_qtd_vermelho,
            "car_qtd_amarelo": self.car_qtd_amarelo
        }