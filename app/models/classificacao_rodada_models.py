from sqlalchemy import Column, CHAR, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class ClassificacaoRodada(Base):
    __tablename__ = "classificacao_rodada"

    clr_id = Column(Integer, primary_key=True, autoincrement=True)  # ID da classificação
    clr_serie = Column(CHAR(1), nullable=False)  # Série do campeonato (A ou B)
    clr_ano = Column(Integer, nullable=False)  # Ano da competição
    clr_rodada = Column(String(45), nullable=True)  # Número ou descrição da rodada
    clr_pontos = Column(Integer, nullable=False)  # Pontos do clube
    clr_vitorias = Column(Integer, nullable=False)  # Número de vitórias
    clr_saldo_gols = Column(Integer, nullable=False)  # Saldo de gols
    clr_gols_pro = Column(Integer, nullable=False)  # Gols marcados ("gols pró")
    clr_confronto_direto = Column(Integer, nullable=False)  # Critério de confronto direto
    clr_vermelho_clube_clu_sigla = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  # Sigla do club no FK cartão vermelho
    clr_amarelo_clube_clu_sigla = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  # Sigla do clube no FK cartão amarelo
    clube_clu_sigla = Column(CHAR(3), ForeignKey("clube.clu_sigla"), nullable=False)  # FK do clube
    clr_qtd_jogou = Column(Integer, nullable=True)  # Quantidade de jogos
    clr_qtd_empates = Column(Integer, nullable=True)  # Quantidade de empates
    clr_qtd_derrotas = Column(Integer, nullable=True)  # Quantidade de derrotas
    clr_gols_contra = Column(Integer, nullable=True)  # Gols sofridos ("gols contra")

    # Relacionamento com a tabela Clube
    clube = relationship("Clube", foreign_keys=[clube_clu_sigla])
    clube_vermelho = relationship("Clube", foreign_keys=[clr_vermelho_clube_clu_sigla])
    clube_amarelo = relationship("Clube", foreign_keys=[clr_amarelo_clube_clu_sigla])

    def __init__(self, clr_serie, clr_ano, clr_rodada, clr_pontos, clr_vitorias, clr_saldo_gols,
                 clr_gols_pro, clr_confronto_direto, clr_vermelho_clube_clu_sigla, clr_amarelo_clube_clu_sigla,
                 clube_clu_sigla, clr_qtd_jogou=None, clr_qtd_empates=None, clr_qtd_derrotas=None,
                 clr_gols_contra=None):
        self.clr_serie = clr_serie
        self.clr_ano = clr_ano
        self.clr_rodada = clr_rodada
        self.clr_pontos = clr_pontos
        self.clr_vitorias = clr_vitorias
        self.clr_saldo_gols = clr_saldo_gols
        self.clr_gols_pro = clr_gols_pro
        self.clr_confronto_direto = clr_confronto_direto
        self.clr_vermelho_clube_clu_sigla = clr_vermelho_clube_clu_sigla
        self.clr_amarelo_clube_clu_sigla = clr_amarelo_clube_clu_sigla
        self.clube_clu_sigla = clube_clu_sigla
        self.clr_qtd_jogou = clr_qtd_jogou
        self.clr_qtd_empates = clr_qtd_empates
        self.clr_qtd_derrotas = clr_qtd_derrotas
        self.clr_gols_contra = clr_gols_contra

    def as_dict(self):
        return {
            "clr_id": self.clr_id,
            "clr_serie": self.clr_serie,
            "clr_ano": self.clr_ano,
            "clr_rodada": self.clr_rodada,
            "clr_pontos": self.clr_pontos,
            "clr_vitorias": self.clr_vitorias,
            "clr_saldo_gols": self.clr_saldo_gols,
            "clr_gols_pro": self.clr_gols_pro,
            "clr_confronto_direto": self.clr_confronto_direto,
            "clr_vermelho_clube_clu_sigla": self.clr_vermelho_clube_clu_sigla,
            "clr_amarelo_clube_clu_sigla": self.clr_amarelo_clube_clu_sigla,
            "clube_clu_sigla": self.clube_clu_sigla,
            "clr_qtd_jogou": self.clr_qtd_jogou,
            "clr_qtd_empates": self.clr_qtd_empates,
            "clr_qtd_derrotas": self.clr_qtd_derrotas,
            "clr_gols_contra": self.clr_gols_contra
        }