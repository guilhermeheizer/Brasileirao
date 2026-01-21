from sqlalchemy import Column, String, CHAR, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Clube(Base):
    __tablename__ = "clube"

    clu_sigla = Column(CHAR(3), primary_key=True, nullable=False)
    clu_nome = Column(String(60), nullable=False)
    clu_serie = Column(CHAR(1), nullable=False)
    clu_link_escudo = Column(String(100), nullable=False)
    cidade_cid_id = Column(Integer, ForeignKey("cidade.cid_id", ondelete="CASCADE"), primary_key=True)

    # Relacionamento com Cidade
    cidade = relationship("Cidade", back_populates="clubes")

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