from app.services.estadio_service import listar_todos_estadios
from app.services.clube_service import listar_todos_clubes
from app.services.form.form_cadastra_rodada_service import criar_rodada
from app.core.database import get_db
from app.schemas.rodada_schema import CriarRodadaSchema

# ---------------------------------------------
# Função JS → Python: carregar estádios
# ---------------------------------------------
def js_listar_todos_estadios():
    session = next(get_db())
    dados = listar_todos_estadios(session)
    session.close()
    return [e.model_dump() for e in dados.estadios]


# ---------------------------------------------
# Função JS → Python: carregar clubes
# ---------------------------------------------
def js_listar_todos_clubes(serie: str = ""):
    session = next(get_db())
    resultado = listar_todos_clubes(serie if serie else None, None, session)
    session.close()
    return [c.model_dump() for c in resultado.clubes]


# ---------------------------------------------
# Função JS → Python: criar rodada
# ---------------------------------------------
def js_criar_rodada(lista_dicts):
    session = next(get_db())
    lista_obj = [CriarRodadaSchema(**item) for item in lista_dicts]
    resposta = criar_rodada(lista_obj, session)
    session.close()
    return [r.model_dump() for r in resposta]