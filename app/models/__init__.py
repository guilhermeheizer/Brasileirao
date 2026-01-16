# Importando todos os modelos para registro
from app.models.cidade_models import Cidade
from app.models.estadio_models import Estadio
from app.models.usuario_models import Usuario
# from app.models.clube import Clube
# from app.models.rodada import Rodada
# from app.models.classificacao import Classificacao

# CODIGO ANTIGO RETIRAR
# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base
# from sqlalchemy.ext.declarative import declarative_base
# from app.core.config import settings

# # Criando a conexão com o banco de dados SQLite
# print("models/__init__.DATABASE_URL:", settings.DATABASE_URL)
# database = str(settings.DATABASE_URL)
# db = create_engine(database, connect_args={"check_same_thread": False})

# #  cria a base do banco de dados
# Base = declarative_base()