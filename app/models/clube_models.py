from typing import TYPE_CHECKING
from sqlalchemy import String, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

if TYPE_CHECKING:
    from app.models.cidade_models import Cidade


class Clube(Base):
    __tablename__ = "clube"

    __table_args__ = (
        Index("idx_clube_cidade_cid_id", "cidade_cid_id"),
    )

    clu_sigla: Mapped[str] = mapped_column(
        String(3),
        primary_key=True,
        nullable=False
    )
    
    clu_nome: Mapped[str] = mapped_column(
        String(60),
        nullable=False
    )

    clu_serie: Mapped[str] = mapped_column(
        String(1),
        nullable=False
    )

    clu_link_escudo: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    cidade_cid_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("cidade.cid_id"),
        nullable=False
    )

    # Relacionamento com Cidade
    cidade: Mapped["Cidade"] = relationship("Cidade", back_populates="clubes")

    def __init__(self, clu_sigla, clu_nome, clu_serie, clu_link_escudo, cidade_cid_id):
        self.clu_sigla = clu_sigla
        self.clu_nome = clu_nome
        self.clu_serie = clu_serie
        self.clu_link_escudo = clu_link_escudo
        self.cidade_cid_id = cidade_cid_id

    def as_dict(self):
        return {
            "clu_sigla": self.clu_sigla,
            "clu_nome": self.clu_nome,
            "clu_serie": self.clu_serie,
            "clu_link_escudo": self.clu_link_escudo,
            "cidade_cid_id": self.cidade_cid_id
        }


# Atualize a classe Cidade no arquivo cidade_models.py para incluir o relacionamento com Clube:
# Adicione:
# clubes = relationship("Clube", cascade="all, delete", back_populates="cidade")