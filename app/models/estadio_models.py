from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Estadio(Base):
    __tablename__ = "estadio"

    est_id = Column(Integer, primary_key=True, autoincrement=True)
    est_nome = Column(String(100), nullable=False)
    cidade_cid_id = Column(Integer, ForeignKey("cidade.cid_id"), nullable=False)

    # cidade_relacao = relationship("Cidade", backref="estadios")

    def __init__(self, est_nome, cidade_cid_id):
        self.est_nome = est_nome
        self.cidade_cid_id = cidade_cid_id