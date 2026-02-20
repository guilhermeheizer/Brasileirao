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
from sqlalchemy import Column, CHAR, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from app.core.database import Base


class Rodada(Base):
    """
    Modelo ORM da tabela 'rodada'.
    Representa uma partida do Campeonato Brasileiro, incluindo informações de clubes, estádio, placar e status.
    """
    __tablename__ = "rodada"

    rod_serie = Column(CHAR(1), primary_key=True, nullable=False)  #: Série (A ou B)
    rod_ano = Column(Integer, primary_key=True, nullable=False)  #: Ano do campeonato
    rod_rodada = Column(Integer, primary_key=True, nullable=False)  #: Número da rodada
    rod_sequencia = Column(Integer, primary_key=True, nullable=False)  #: Identifica sequência da partida específica
    rod_data = Column(DATETIME, nullable=False)  #: Data da partida
    clube_clu_sigla_mandante = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  #: Mandante
    rod_gols_mandante = Column(Integer, nullable=True)  #: Gols do mandante
    clube_clu_sigla_visitante = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  #: Visitante
    rod_gols_visitante = Column(Integer, nullable=True)  #: Gols do visitante
    rod_pontos_mandante = Column(Integer, nullable=True)  #: Pontos do mandante
    rod_pontos_visitante = Column(Integer, nullable=True)  #: Pontos do visitante
    rod_calculou_classificacao = Column(CHAR(1), nullable=True, default="N")  #: Se classificações foram calculadas
    rod_partida_finalizada = Column(CHAR(1), nullable=True, default="N")  #: Se a partida foi finalizada
    estadio_est_id = Column(Integer, ForeignKey("estadio.est_id"), nullable=False)  #: Estádio onde ocorreu a partida

    # Relacionamentos com Clube
    clube_mandante = relationship("Clube", foreign_keys=[clube_clu_sigla_mandante])
    clube_visitante = relationship("Clube", foreign_keys=[clube_clu_sigla_visitante])

    # Relacionamento com Estádio
    estadio = relationship("Estadio")

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
            rod_data (datetime): Data da partida
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