from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


"""
rodada_schema.py

Este módulo define os schemas Pydantic para operações relacionadas às rodadas do Campeonato Brasileiro.

Os schemas representam as estruturas de dados utilizadas para:
- Cadastro de rodadas
- Atualização de placar
- Respostas de API para rodadas e jogos
- Formulários de placar

Cada schema é utilizado para validação, serialização e documentação automática das rotas FastAPI.

Classes principais:
- RodadaSchema: Base para dados de uma rodada
- CriarRodadaSchema: Para criação de rodada
- AtualizarRodadaPlacarSchema: Para atualização de placar
- ResponseRodadaSchema: Resposta detalhada de uma rodada
- ResponseRodadasSchema: Lista de rodadas
- JogoFormPlacarSchema: Detalhes de um jogo
- ListaJogosRodadaFormPlacarResponse: Lista de jogos de uma rodada
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
class RodadaSchema(BaseModel):
    """
    Schema base para dados de uma rodada do campeonato.
    Inclui informações como série, ano, rodada, clubes e estádio.
    """
    rod_serie: str
    rod_ano: int
    rod_rodada: int
    rod_sequencia: int
    rod_data: datetime
    clube_clu_sigla_mandante: str
    clube_clu_sigla_visitante: str
    estadio_est_id: int
    
    class Config:
        from_attributes = True


class CriarRodadaSchema(RodadaSchema):
    """
    Schema para criação de uma rodada.
    Adiciona campos para controle de classificação e finalização da partida.
    """
    rod_calculou_classificacao: Optional[str] = "N"
    rod_partida_finalizada: Optional[str] = "N"

    class Config:
        from_attributes = True

class ResponseCriarRodadaSchema(CriarRodadaSchema):

    """
    Schema de resposta para criação de rodada.
    Herda todos os campos de CriarRodadaSchema.
    """
    class Config:
        from_attributes = True

class AtualizarRodadaPlacarSchema(BaseModel):
    """
    Schema para atualização do placar de uma rodada.
    Inclui gols, finalização e identificação da rodada.
    """
    rod_serie: str
    rod_ano: int
    rod_rodada: int
    rod_sequencia: int
    rod_gols_mandante: int
    rod_gols_visitante: int
    rod_partida_finalizada: str
    
    class Config:
        from_attributes = True


class ResponseRodadaSchema(AtualizarRodadaPlacarSchema):
    """
    Schema de resposta detalhada de uma rodada.
    Inclui links de escudo e informações do estádio.
    """
    clu_link_escudo_mandante: Optional[str]
    clu_link_escudo_visitante: Optional[str]
    est_id: int
    est_nome: str

    class Config:
        from_attributes = True


class ResponseRodadasSchema(BaseModel):
    """
    Schema de resposta para lista de rodadas.
    Contém uma lista de ResponseRodadaSchema.
    """
    rodadas: List[ResponseRodadaSchema]

    class Config:
        from_attributes = True


# Schema para representar os detalhes de um único jogo
class JogoFormPlacarSchema(BaseModel):
    """
    Schema para representar os detalhes de um único jogo.
    Utilizado em formulários de placar.
    """
    rod_serie: str  # Série do campeonato (A ou B)
    rod_ano: int  # Ano do campeonato
    rod_rodada: int  # Número da rodada
    rod_sequencia: int  # Sequência do jogo dentro da rodada
    est_id: int  # ID do estádio
    est_nome: str  # Nome do estádio
    rod_data: datetime  # Data e hora do jogo
    clube_clu_sigla_mandante: str  # Sigla do clube mandante
    clu_nome_mandante: str  # Nome completo do clube mandante
    clu_link_escudo_mandante: str  # URL do escudo do clube mandante
    rod_gols_mandante: Optional[int]  # Gols do mandante (pode ser nulo)
    rod_pontos_mandante: Optional[int]  # Pontos do mandante (pode ser nulo)
    clube_clu_sigla_visitante: str  # Sigla do clube visitante
    clu_nome_visitante: str  # Nome completo do clube visitante
    clu_link_escudo_visitante: str  # URL do escudo do clube visitante
    rod_gols_visitante: Optional[int] # Gols do visitante (pode ser nulo)
    rod_pontos_visitante: Optional[int]  # Pontos do visitante (pode ser nulo)
    car_qtd_vermelho_mandante: Optional[int] = 0 # Cartões vermelhos do mandante (pode ser nulo)
    car_qtd_amarelo_mandante: Optional[int] = 0 # Cartões amarelos do mandante (pode ser nulo)
    car_qtd_vermelho_visitante: Optional[int] = 0 # Cartões vermelhos do visitante (pode ser nulo)
    car_qtd_amarelo_visitante: Optional[int] = 0 # Cartões amarelos do visitante (pode ser nulo)
    rod_partida_finalizada: str  # Indica se a partida foi finalizada ("S" ou "N")
    rod_calculou_classificacao: str  # Indica se a classificação foi calculada ("S" ou "N")


# Schema para a resposta que contém a lista de jogos de uma rodada
class ListaJogosRodadaFormPlacarResponse(BaseModel):
    """
    Schema para resposta contendo a lista de jogos de uma rodada.
    Utilizado para exibir todos os jogos de uma rodada específica.
    """
    serie: str  # Série do campeonato (A ou B)
    ano: int  # Ano da competição
    rodada: int  # Número da rodada
    jogos_da_rodada: List[JogoFormPlacarSchema]  # Lista de jogos da rodada

    class Config:
        # Configuração para uso direto com objetos SQLAlchemy (opcional)
        from_attributes = True