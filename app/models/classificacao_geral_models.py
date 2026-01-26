from sqlalchemy import Column, CHAR, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ClassificacaoGeral(Base):
    __tablename__ = "classificacao_geral"

    clg_id = Column(Integer, primary_key=True, autoincrement=True)  # ID da classificação geral
    clg_serie = Column(CHAR(1), nullable=False)  # Série do campeonato (A ou B)
    clg_ano = Column(Integer, nullable=False)  # Ano da competição
    clg_pontos = Column(Integer, nullable=False)  # Pontuação total do clube
    clg_vitorias = Column(Integer, nullable=False)  # Número total de vitórias
    clg_saldo_gols = Column(Integer, nullable=False)  # Saldo total de gols
    clg_gols_pro = Column(Integer, nullable=False)  # Total de gols marcados ("gols pró")
    clg_confronto_direto = Column(Integer, nullable=False)  # Critério de confronto direto
    clg_vermelho_clube_clu_sigla = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  # FK Cartões vermelhos
    clg_amarelo_clube_clu_sigla = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  # FK Cartões amarelos
    clube_clu_sigla = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  # FK Clube
    clg_qtd_jogou = Column(Integer, nullable=True)  # Total de jogos disputados
    clg_qtd_empates = Column(Integer, nullable=True)  # Total de empates
    clg_qtd_derrotas = Column(Integer, nullable=True)  # Total de derrotas
    clg_gols_contra = Column(Integer, nullable=True)  # Total de gols sofridos

    # Relacionamento com a tabela Clube
    clube = relationship("Clube", foreign_keys=[clube_clu_sigla])
    clube_vermelho = relationship("Clube", foreign_keys=[clg_vermelho_clube_clu_sigla])
    clube_amarelo = relationship("Clube", foreign_keys=[clg_amarelo_clube_clu_sigla])

    def __init__(self, clg_serie, clg_ano, clg_pontos, clg_vitorias, clg_saldo_gols, clg_gols_pro, 
                 clg_confronto_direto, clg_vermelho_clube_clu_sigla, clg_amarelo_clube_clu_sigla, 
                 clube_clu_sigla, clg_qtd_jogou=None, clg_qtd_empates=None, clg_qtd_derrotas=None, 
                 clg_gols_contra=None):
        self.clg_serie = clg_serie
        self.clg_ano = clg_ano
        self.clg_pontos = clg_pontos
        self.clg_vitorias = clg_vitorias
        self.clg_saldo_gols = clg_saldo_gols
        self.clg_gols_pro = clg_gols_pro
        self.clg_confronto_direto = clg_confronto_direto
        self.clg_vermelho_clube_clu_sigla = clg_vermelho_clube_clu_sigla
        self.clg_amarelo_clube_clu_sigla = clg_amarelo_clube_clu_sigla
        self.clube_clu_sigla = clube_clu_sigla
        self.clg_qtd_jogou = clg_qtd_jogou
        self.clg_qtd_empates = clg_qtd_empates
        self.clg_qtd_derrotas = clg_qtd_derrotas
        self.clg_gols_contra = clg_gols_contra

    def as_dict(self):
        return {
            "clg_id": self.clg_id,
            "clg_serie": self.clg_serie,
            "clg_ano": self.clg_ano,
            "clg_pontos": self.clg_pontos,
            "clg_vitorias": self.clg_vitorias,
            "clg_saldo_gols": self.clg_saldo_gols,
            "clg_gols_pro": self.clg_gols_pro,
            "clg_confronto_direto": self.clg_confronto_direto,
            "clg_vermelho_clube_clu_sigla": self.clg_vermelho_clube_clu_sigla,
            "clg_amarelo_clube_clu_sigla": self.clg_amarelo_clube_clu_sigla,
            "clube_clu_sigla": self.clube_clu_sigla,
            "clg_qtd_jogou": self.clg_qtd_jogou,
            "clg_qtd_empates": self.clg_qtd_empates,
            "clg_qtd_derrotas": self.clg_qtd_derrotas,
            "clg_gols_contra": self.clg_gols_contra
        }