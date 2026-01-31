from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.rodada_schema import ListaJogosRodadaFormPlacarResponse
from app.services.form.form_rodada import rodada_lista


router_placar_rodada = APIRouter(tags=["placar rodada"])

@router_placar_rodada.get(
    "/rodadas/{serie}/{ano}/{rodada}",
    response_model=ListaJogosRodadaFormPlacarResponse,
    summary="Listar jogos da rodada para preenchimento de placares",
    description="Retorna jogos de uma rodada específica ou jogos anteriores não realizados no formato esperado pelo front-end."
)
def get_rodada_lista(
    serie: str,
    ano: int,
    rodada: int,
    carrega_nao_realizados: bool = Query(
        default=False,
        alias="carrega_jogos_nao_realizados",
        description="Quando verdadeiro, inclui jogos não realizados de rodadas anteriores."
    ),
    db: Session = Depends(get_db)
):
    """
    Endpoint para buscar os jogos de uma rodada no formato desejado.
    """
    return rodada_lista(
        db=db,
        serie=serie,
        ano=ano,
        rodada=rodada,
        carrega_nao_realizados=carrega_nao_realizados
    )