from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.clube_models import Clube


class Cartao(Base):
    __tablename__ = "cartao"

    car_serie: Mapped[str] = mapped_column(
        String(1),
        primary_key=True,
        nullable=False
    )  # Série (A ou B)

    car_ano: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False
    )  # Ano da competição

    clube_clu_sigla: Mapped[str] = mapped_column(
        String(3),
        ForeignKey("clube.clu_sigla"),
        primary_key=True,
        nullable=False
    )  # FK para clube

    car_qtd_vermelho: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )  # Cartões vermelhos

    car_qtd_amarelo: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )  # Cartões amarelos

    # Relacionamento com a tabela Clube
    clube: Mapped["Clube"] = relationship(
    "Clube",
    foreign_keys=[clube_clu_sigla]
    )

    def __init__(self, car_serie, car_ano, clube_clu_sigla, car_qtd_vermelho=0, car_qtd_amarelo=0):
        self.car_serie = car_serie
        self.car_ano = car_ano
        self.clube_clu_sigla = clube_clu_sigla
        self.car_qtd_vermelho = car_qtd_vermelho
        self.car_qtd_amarelo = car_qtd_amarelo

    def as_dict(self):
        return {
            "car_serie": self.car_serie,
            "car_ano": self.car_ano,
            "clube_clu_sigla": self.clube_clu_sigla,
            "car_qtd_vermelho": self.car_qtd_vermelho,
            "car_qtd_amarelo": self.car_qtd_amarelo
        }