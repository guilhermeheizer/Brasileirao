from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from app.core.dependencies import pegar_sessao, verificar_token
from app.models.usuario_models import Usuario
from app.schemas.cartao_schema import ResponseCartaoClubeSchema
from app.schemas.rodada_schema import ListaJogosRodadaFormPlacarResponse, AtualizarRodadaPlacarSchema
from app.services.form.form_placar_rodada import calcular_classificacao_brasileirao, rodada_lista, atualizar_placares_rodada
from app.services.cartao_service import listar_cartoes_paginados


router_placar_rodada = APIRouter(tags=["placar rodada"])

@router_placar_rodada.get(
    "/busca-placares/{serie}/{ano}/{rodada}",
    response_model=ListaJogosRodadaFormPlacarResponse,
    summary="Busca os jogos da rodada para preenchimento de placares",
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
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    """
    Endpoint para buscar os jogos de uma rodada no formato desejado.
    """
    try:
        return rodada_lista(
            db=session,
            serie=serie,
            ano=ano,
            rodada=rodada,
            carrega_nao_realizados=carrega_nao_realizados
            
    )
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar jogos da rodada: {str(ex)}")
    finally:
        session.close()

@router_placar_rodada.put("/atualiza-placares")
async def atualizar_placares(
    jogos: List[AtualizarRodadaPlacarSchema],
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    """
    Endpoint para atualizar placares e status de finalização de 10 jogos na tabela `rodada`.

    Args:
        jogos (List[AtualizarRodadaPlacarSchema]): Lista de objetos contendo as informações sobre os placares e status.
        db (Session): Sessão ativa do banco de dados.

    Returns:
        dict: Mensagem indicando o número de partidas atualizadas.
    """
    try:
        return atualizar_placares_rodada(session, jogos)
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar placares: {str(ex)}")
    finally:
        session.close()




@router_placar_rodada.get("/lista-paginado", response_model=ResponseCartaoClubeSchema)
async def listar_cartoes_paginacao(
    nome: Optional[str] = Query(None, description="Busca parcial pelo nome da clube"),
    pagina: int = Query(1, description="Número da página", ge=1),
    tamanho_pagina: int = Query(20, description="Tamanho da página", ge=1),
    session: Session = Depends(pegar_sessao)):
    """Lista os cartões com paginação e busca por nome.

    Args:
        nome (Optional[str], optional): Defaults to Query(None, description="Busca parcial pelo nome do clube").
        pagina (int, optional): Defaults to Query(1, description="Número da página", ge=1).
        tamanho_pagina (int, optional): Defaults to Query(10, description="Tamanho da página", ge=1).   
        session (Session, optional): Sessão do SQLAlchemy gerenciada pelo FastAPI   
                                     via dependência de injeção (Depends(pegar_sessao)).

    Raises:
        HTTPException: Lançada se ocorrer um erro durante a listagem dos cartões.

    Returns: ResponseCartaoClubeSchema: Uma resposta no formato do esquema Pydantic `ResponseCartaoClubeSchema`, 
             que contém uma lista de cartões no formato especificado por `CartaoSchema`.
    """
    try:
        return listar_cartoes_paginados(nome, pagina, tamanho_pagina, session)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)
    finally:
        session.close()


@router_placar_rodada.post(
    "/classificacao/{serie}/{ano}/{rodada}",
    summary="Calcula a classificação da série informada no campeonato",
    description="Calcula e atualiza a tabela classificacao_geral com base nas rodadas já finalizadas.",
    response_description="Confirmação do processamento."
)
async def calcular_classificacao(
    serie: str,
    ano: int,
    rodada: int,
    carrega_jogos_nao_realizados: bool = Query(
        default=False,
        alias="carrega_jogos_nao_realizados",
        description="Quando verdadeiro, inclui jogos não realizados de rodadas anteriores."),
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token)
):
    try:
        return calcular_classificacao_brasileirao(
            db=session,
            serie=serie,
            ano=ano,
            rodada=rodada,
            carrega_nao_realizados=carrega_jogos_nao_realizados)
    except HTTPException as ex:
        log_erro = (f"{ex.detail}")
        raise HTTPException(status_code=404, detail=log_erro)
    finally:
        session.close()