from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.orm import relationship
from app.core.database import Base


class Cidade(Base):
    __tablename__ = "cidade"

    cid_id = Column(Integer, primary_key=True, autoincrement=True)
    cid_nome = Column(String(100), nullable=False)
    cid_uf = Column(CHAR(2), nullable=False)

    estadios = relationship("Estadio", cascade="all, delete")
    clubes = relationship("Clube", cascade="all, delete", back_populates="cidade")

    def __init__(self, cid_nome, cid_uf):
        self.cid_nome = cid_nome
        self.cid_uf = cid_uf

    def as_dict(self):
        return {
            "cid_id": self.cid_id,
            "cid_nome": self.cid_nome,
            "cid_uf": self.cid_uf
        }