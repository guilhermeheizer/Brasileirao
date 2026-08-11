from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Index, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.cidade_models import Cidade

class Estadio(Base):
    __tablename__ = "estadio"

    __table_args__ = (
        Index("idx_estadio_cidade_cid_id", "cidade_cid_id"),
    )

    est_id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        primary_key=True,
        autoincrement=True
    )
    est_nome: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    cidade_cid_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cidade.cid_id"),
        nullable=False
    )

    # Relacionamento com Cidade
    cidade: Mapped["Cidade"] = relationship("Cidade", back_populates="estadios")

    def __init__(self, est_nome, cidade_cid_id):
        self.est_nome = est_nome
        self.cidade_cid_id = cidade_cid_id

    def as_dict(self):
        return {
            "est_id": self.est_id,
            "est_nome": self.est_nome,
            "cidade_cid_id": self.cidade_cid_id
        }