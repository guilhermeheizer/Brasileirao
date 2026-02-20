"""
cidade_models.py

Este módulo define o modelo ORM da tabela 'cidade' do Campeonato Brasileiro.
Utiliza SQLAlchemy para mapear os campos da tabela e seus relacionamentos.

Principais funcionalidades:
- Representação de uma cidade
- Relacionamento com estádios e clubes
- Métodos utilitários para conversão em dicionário

Classe principal:
- Cidade: modelo ORM da tabela cidade
"""
from sqlalchemy import Column, Integer, String, CHAR
from sqlalchemy.orm import relationship
from app.core.database import Base


class Cidade(Base):
    """
    Modelo ORM da tabela 'cidade'.
    Representa uma cidade, incluindo nome, UF e seus relacionamentos com estádios e clubes.
    """
    __tablename__ = "cidade"

    cid_id = Column(Integer, primary_key=True, autoincrement=True)
    cid_nome = Column(String(100), nullable=False)
    cid_uf = Column(CHAR(2), nullable=False)

    estadios = relationship("Estadio", cascade="all, delete")
    clubes = relationship("Clube", cascade="all, delete", back_populates="cidade")

    def __init__(self, cid_nome, cid_uf):
        """
        Inicializa uma instância de Cidade.
        Args:
            cid_nome (str): Nome da cidade
            cid_uf (str): Unidade Federativa (UF)
        """
        self.cid_nome = cid_nome
        self.cid_uf = cid_uf

    def as_dict(self):
        """
        Retorna os dados da cidade como um dicionário.
        Útil para serialização e respostas de API.
        Returns:
            dict: Dados da cidade
        """
        return {
            "cid_id": self.cid_id,
            "cid_nome": self.cid_nome,
            "cid_uf": self.cid_uf
        }