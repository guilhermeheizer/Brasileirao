# To activate the virtual environment, use the following command into terminal
# venv\Scripts\activate 
# To run the FastAPI app, use the following command into terminal
#  uvicorn main:app --reload
#
# Quando incluir uma nova tabela, ir em:
# - app\models\__init__.py: acresentar o novo import do modelo da tabela
# - app\core\database.py: acrescentar em criar_tabelas() o novo model

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
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
    # print("main - Inicializando a aplicação...")
    criar_tabelas()  # Cria as tabelas no banco de dados caso necessário.

@app.get("/")
def root():
    return {"message": "Bem-vindo ao sistema Brasileirão!"}

# print("Aplicação configurada com sucesso.")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/login-form")

from app.routes.form.form_login import login_router
from app.routes.crud.usuario_routers import usuario_router
from app.routes.crud.cidade_routes import cidade_router
from app.routes.crud.clube_routers import clube_router
from app.routes.crud.estadio_routers import estadio_router
from app.routes.crud.cartao_routers import cartao_router
app.router.include_router(usuario_router, prefix="/usuario")
app.router.include_router(login_router, prefix="/login")
app.router.include_router(cidade_router, prefix="/cidade")
app.router.include_router(clube_router, prefix="/clube")
app.router.include_router(estadio_router, prefix="/estadio")
app.router.include_router(cartao_router, prefix="/cartao")
# print("Rotas incluídas com sucesso.")

