"""
rodada_models.py

Este módulo define o modelo ORM da tabela 'rodada' do Campeonato Brasileiro.
Utiliza SQLAlchemy para mapear os campos da tabela e seus relacionamentos.

Principais funcionalidades:
- Representação de uma partida (rodada) do campeonato
- Relacionamento com clubes (mandante e visitante) e estádio
- Métodos utilitários para conversão em dicionário

Classe principal:
- Rodada: modelo ORM da tabela rodada
"""
from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, DateTime, text, Identity, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.clube_models import Clube
    from app.models.estadio_models import Estadio


class Rodada(Base):
    """
    Modelo ORM da tabela 'rodada'.
    Representa uma partida do Campeonato Brasileiro, incluindo informações de clubes, estádio, placar e status.
    """
    __tablename__ = "rodada"

    rod_serie: Mapped[str] = mapped_column(
        String(1),
        primary_key=True,
        nullable=False
    )

    rod_ano: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    rod_rodada: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    rod_sequencia: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )

    rod_data: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False),
        nullable=False
    )

    clube_clu_sigla_mandante: Mapped[str] = mapped_column(
        String(3),
        ForeignKey("clube.clu_sigla"),
        nullable=False
    )

    rod_gols_mandante: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    clube_clu_sigla_visitante: Mapped[str] = mapped_column(
        String(3),
        ForeignKey("clube.clu_sigla"),
        nullable=False
    )

    rod_gols_visitante: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    rod_pontos_mandante: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    rod_pontos_visitante: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    rod_calculou_classificacao: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        server_default=text("'N'")
    )

    rod_partida_finalizada: Mapped[str] = mapped_column(
        String(1),
        nullable=False,
        default="N",
        server_default=text("'N'")
    )

    estadio_est_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("estadio.est_id"),
        nullable=False
    )

    clube_mandante: Mapped["Clube"] = relationship(
        "Clube",
        foreign_keys=[clube_clu_sigla_mandante]
    )

    clube_visitante: Mapped["Clube"] = relationship(
        "Clube",
        foreign_keys=[clube_clu_sigla_visitante]
    )

    estadio: Mapped["Estadio"] = relationship(
        "Estadio"
    )

    def __init__(self, rod_serie, rod_ano, rod_rodada, rod_sequencia, rod_data, 
                 clube_clu_sigla_mandante, clube_clu_sigla_visitante, rod_calculou_classificacao, 
                 rod_partida_finalizada, estadio_est_id):
        """
        Inicializa uma instância de Rodada.
        Args:
            rod_serie (str): Série do campeonato (A ou B)
            rod_ano (int): Ano do campeonato
            rod_rodada (int): Número da rodada
            rod_sequencia (int): Sequência da partida
            rod_data (DateTime): Data da partida
            clube_clu_sigla_mandante (str): Sigla do clube mandante
            clube_clu_sigla_visitante (str): Sigla do clube visitante
            rod_calculou_classificacao (str): Se classificações foram calculadas
            rod_partida_finalizada (str): Se a partida foi finalizada
            estadio_est_id (int): ID do estádio
        """
        self.rod_serie = rod_serie
        self.rod_ano = rod_ano
        self.rod_rodada = rod_rodada
        self.rod_sequencia = rod_sequencia
        self.rod_data = rod_data
        self.clube_clu_sigla_mandante = clube_clu_sigla_mandante
        self.clube_clu_sigla_visitante = clube_clu_sigla_visitante
        self.rod_calculou_classificacao = rod_calculou_classificacao
        self.rod_partida_finalizada = rod_partida_finalizada
        self.estadio_est_id = estadio_est_id

    def as_dict(self):
        """
        Retorna os dados da rodada como um dicionário.
        Útil para serialização e respostas de API.
        Returns:
            dict: Dados da rodada
        """
        return {
            "rod_serie": self.rod_serie,
            "rod_ano": self.rod_ano,
            "rod_rodada": self.rod_rodada,
            "rod_sequencia": self.rod_sequencia,
            "rod_data": self.rod_data,
            "clube_clu_sigla_mandante": self.clube_clu_sigla_mandante,
            "rod_gols_mandante": self.rod_gols_mandante,
            "clube_clu_sigla_visitante": self.clube_clu_sigla_visitante,
            "rod_gols_visitante": self.rod_gols_visitante,
            "rod_pontos_mandante": self.rod_pontos_mandante,
            "rod_pontos_visitante": self.rod_pontos_visitante,
            "rod_calculou_classificacao": self.rod_calculou_classificacao,
            "rod_partida_finalizada": self.rod_partida_finalizada,
            "estadio_est_id": self.estadio_est_id
        }