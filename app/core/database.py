# Configuração e inicialização do banco de dados
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


print("DATABASE_URL:", settings.DATABASE_URL)
database_url = settings.DATABASE_URL
if settings.DATABASE_URL is None:
    raise HTTPException(status_code=500, detail="DATABASE_URL is not set in environment variables")

engine = create_engine(str(settings.DATABASE_URL), connect_args={"check_same_thread": False} if "sqlite" in str(settings.DATABASE_URL) else {})

# Cria sessão local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

# Instância do Base para criação automática de tabelas
Base = declarative_base()

# Dependência para conexão com o banco de dados.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cria as tabelas no banco de dados
def criar_tabelas(): 
    from app.models import cidade_models, estadio_models, usuario_models, clube_models, cartao_models, classificacao_rodada_models, classificacao_geral_models  # Importa os modelos para registrar as tabelas
    Base.metadata.create_all(bind=engine)