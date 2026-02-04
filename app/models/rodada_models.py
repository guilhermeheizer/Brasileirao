from sqlalchemy import Column, CHAR, Integer, ForeignKey, DATETIME
from sqlalchemy.orm import relationship
from app.core.database import Base


class Rodada(Base):
    __tablename__ = "rodada"

    rod_serie = Column(CHAR(1), primary_key=True, nullable=False)  # Série (A ou B)
    rod_ano = Column(Integer, primary_key=True, nullable=False)  # Ano do campeonato
    rod_rodada = Column(Integer, primary_key=True, nullable=False)  # Número da rodada
    rod_sequencia = Column(Integer, primary_key=True, nullable=False)  # Identifica sequência da partida específica
    rod_data = Column(DATETIME, nullable=False)  # Data da partida
    clube_clu_sigla_mandante = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  # Mandante
    rod_gols_mandante = Column(Integer, nullable=True)  # Gols do mandante
    clube_clu_sigla_visitante = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  # Visitante
    rod_gols_visitante = Column(Integer, nullable=True)  # Gols do visitante
    rod_pontos_mandante = Column(Integer, nullable=True)  # Pontos do mandante
    rod_pontos_visitante = Column(Integer, nullable=True)  # Pontos do visitante
    rod_calculou_classificacao = Column(CHAR(1), nullable=True, default="N")  # Se classificações foram calculadas
    rod_partida_finalidaza = Column(CHAR(1), nullable=True, default="N")  # Se a partida foi finalidaza
    estadio_est_id = Column(Integer, ForeignKey("estadio.est_id"), nullable=False)  # Estádio onde ocorreu a partida

    # Relacionamentos com Clube
    clube_mandante = relationship("Clube", foreign_keys=[clube_clu_sigla_mandante])
    clube_visitante = relationship("Clube", foreign_keys=[clube_clu_sigla_visitante])

    # Relacionamento com Estádio
    estadio = relationship("Estadio")

    def __init__(self, rod_serie, rod_ano, rod_rodada, rod_sequencia, rod_data, 
                 clube_clu_sigla_mandante, clube_clu_sigla_visitante, rod_calculou_classificacao, 
                 rod_partida_finalidaza, estadio_est_id):
        self.rod_serie = rod_serie
        self.rod_ano = rod_ano
        self.rod_rodada = rod_rodada
        self.rod_sequencia = rod_sequencia
        self.rod_data = rod_data
        self.clube_clu_sigla_mandante = clube_clu_sigla_mandante
        self.clube_clu_sigla_visitante = clube_clu_sigla_visitante
        self.rod_calculou_classificacao = rod_calculou_classificacao
        self.rod_partida_finalidaza = rod_partida_finalidaza
        self.estadio_est_id = estadio_est_id

    def as_dict(self):
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
            "rod_partida_finalidaza": self.rod_partida_finalidaza,
            "estadio_est_id": self.estadio_est_id
        }