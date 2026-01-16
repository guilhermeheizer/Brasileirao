# To activate the virtual environment, use the following command into terminal
# venv\Scripts\activate 
# To run the FastAPI app, use the following command into terminal
#  uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
# from app.routes import api_router  # Importando o agrupador de rotas
# from app.core.config import settings  # Configurações do projeto (se aplicável)
# from app.core.database import get_db  # Função opcional para inicializar o banco de dados
from app.core.database import criar_tabelas


# Criação da aplicação FastAPI
app = FastAPI(
    title="Brasileirão API",
    description="API para gerenciar informações do Campeonato Brasileiro",
    version="1.0.0"
)

@app.on_event("startup")
def startup_event():
    """
    Evento de startup: executa configurações necessárias ao iniciar o aplicativo.
    """
    print("main - Inicializando a aplicação...")
    criar_tabelas()  # Cria as tabelas no banco de dados caso necessário.

# REMOVER ESTE CÓDIGO SE NÃO FOR MAIS NECESSÁRIO
# Função para configurar inicializações necessárias
# def setup():
#     # Inicialização de banco de dados, verificações ou outras configurações
#     get_db()

# Executar a criação de tabelas
# criar_tabelas()

@app.get("/")
def root():
    return {"message": "Bem-vindo ao sistema Brasileirão!"}

print("Aplicação configurada com sucesso.")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/login-form")

from app.routes.crud.cidade_routes import cidade_router
from app.routes.crud.usuario_routers import usuario_router
from app.routes.form.form_login import login_router
app.router.include_router(cidade_router, prefix="/cidade", tags=["Cidade"])
app.router.include_router(usuario_router, prefix="/usuario", tags=["Usuario"])
app.router.include_router(login_router, prefix="/login", tags=["Login"])
print("Rotas incluídas com sucesso.")

