from sqlalchemy import and_, text
from sqlalchemy.orm import Session, aliased
from fastapi import HTTPException
from app.models.rodada_models import Rodada
from app.models.clube_models import Clube
from app.models.estadio_models import Estadio
from app.models.cartao_models import Cartao
from app.schemas.rodada_schema import ListaJogosRodadaFormPlacarResponse, JogoFormPlacarSchema


def rodada_lista(
    db: Session,
    serie: str,
    ano: int,
    rodada: int,
    carrega_nao_realizados: bool = False
) -> ListaJogosRodadaFormPlacarResponse:
    """
    Carrega a lista de jogos da rodada no formato necessário para o front-end.
    Se carrega_nao_realizados=True, inclui jogos de rodadas anteriores não finalizados.

    Args:
        db (Session): Sessão ativa do banco de dados.
        serie (str): Série do campeonato (ex: 'A', 'B').
        ano (int): Ano da competição.
        rodada (int): Número da rodada.
        carrega_nao_realizados (bool): Se True, inclui jogos não finalizados das rodadas anteriores.

    Returns:
        ListaJogosRodadaFormPlacarResponse: JSON contendo detalhes da rodada e jogos.
    """
    # Garantir que a série está em maiúsculo
    serie_upper = serie.upper()

    # Validar a série
    if serie_upper not in ["A", "B"]:
        raise HTTPException(
            status_code=400,
            detail=f"Série '{serie_upper}' inválida. Use 'A' ou 'B'."
        )

    # Aliases para diferenciar os clubes e cartao mandante e visitante
    ClubeMandante = aliased(Clube, name="clube_mandante")
    ClubeVisitante = aliased(Clube, name="clube_visitante")
    CartaoMandante = aliased(Cartao, name="cartao_mandante")
    CartaoVisitante = aliased(Cartao, name="cartao_visitante")

    # Query inicial
    # query = db.query(
    #     Rodada,
    #     Estadio.__table__.c.est_nome.label("est_nome"),
    #     ClubeMandante.__table__.c.clu_nome.label("clu_nome_mandante"),
    #     ClubeMandante.__table__.c.clu_link_escudo.label("clu_link_escudo_mandante"),
    #     ClubeVisitante.__table__.c.clu_nome.label("clu_nome_visitante"),
    #     ClubeVisitante.__table__.c.clu_link_escudo.label("clu_link_escudo_visitante"),
    #     CartaoMandante.__table__.c.car_qtd_vermelho.label("cartoes_vermelhos_mandante"),
    #     CartaoMandante.__table__.c.car_qtd_amarelo.label("cartoes_amarelos_mandante"),
    #     CartaoVisitante.__table__.c.car_qtd_vermelho.label("cartoes_vermelhos_visitante"),
    #     CartaoVisitante.__table__.c.car_qtd_amarelo.label("cartoes_amarelos_visitante")
    # ).join(
    #     Estadio, Rodada.__table__.c.estadio_est_id == Estadio.est_id
    # ).join(
    #     #ClubeMandante, Rodada.__table__.c.clube_clu_sigla_mandante == ClubeMandante.__table__.c.clu_sigla
    #      ClubeMandante, Rodada.clube_clu_sigla_mandante == ClubeMandante.clu_sigla
    # ).join(
    #     ClubeVisitante, Rodada.__table__.c.clube_clu_sigla_visitante == ClubeVisitante.__table__.c.clu_sigla
    # ).outerjoin(
    #     CartaoMandante, and_(
    #         Rodada.__table__.c.rod_serie == CartaoMandante.__table__.c.car_serie,
    #         Rodada.__table__.c.rod_ano == CartaoMandante.__table__.c.car_ano,
    #         Rodada.__table__.c.clube_clu_sigla_mandante == CartaoMandante.__table__.c.clube_clu_sigla
    # )
    # ).outerjoin(
    #     CartaoVisitante, and_(
    #         Rodada.__table__.c.rod_serie == CartaoVisitante.__table__.c.car_serie,
    #         Rodada.__table__.c.rod_ano == CartaoVisitante.__table__.c.car_ano,
    #         Rodada.__table__.c.clube_clu_sigla_visitante == CartaoVisitante.__table__.c.clube_clu_sigla
    # )
    # ).filter(
    #     Rodada.__table__.c.rod_serie == serie_upper,
    #     Rodada.__table__.c.rod_ano == ano
    # )

    # # Filtrar jogos conforme o parâmetro "carrega_nao_realizados"
    # if carrega_nao_realizados:
    #     query = query.filter(
    #         Rodada.__table__.c.rod_rodada <= rodada,
    #         Rodada.__table__.c.rod_partida_finalidaza == "N"
    #     )
    # else:
    #     query = query.filter(Rodada.__table__.c.rod_rodada == rodada)

    # # Ordenar os dados de maneira consistente
    # query = query.order_by(
    #     Rodada.__table__.c.rod_rodada, Rodada.__table__.c.rod_data, Rodada.__table__.c.rod_sequencia
    # )
    # print(query)

    # Obter os resultados
    #resultados = query.all()
        # Definir a query SQL diretamente
    sql_query = text("""
        SELECT
            rodada.rod_serie AS rodada_rod_serie,
            rodada.rod_ano AS rodada_rod_ano,
            rodada.rod_rodada AS rodada_rod_rodada,
            rodada.rod_sequencia AS rodada_rod_sequencia,
            rodada.rod_data AS rodada_rod_data,
            rodada.clube_clu_sigla_mandante AS rodada_clube_clu_sigla_mandante,
            rodada.rod_gols_mandante AS rodada_rod_gols_mandante,
            rodada.clube_clu_sigla_visitante AS rodada_clube_clu_sigla_visitante,
            rodada.rod_gols_visitante AS rodada_rod_gols_visitante,
            rodada.rod_pontos_mandante AS rodada_rod_pontos_mandante,
            rodada.rod_pontos_visitante AS rodada_rod_pontos_visitante,
            rodada.rod_calculou_classificacao AS rodada_rod_calculou_classificacao,
            rodada.rod_partida_finalidaza AS rodada_rod_partida_finalidaza,
            rodada.estadio_est_id AS rodada_estadio_est_id,
            estadio.est_nome AS est_nome,
            clube_mandante.clu_nome AS clu_nome_mandante,
            clube_mandante.clu_link_escudo AS clu_link_escudo_mandante,
            clube_visitante.clu_nome AS clu_nome_visitante,
            clube_visitante.clu_link_escudo AS clu_link_escudo_visitante,
            cartao_mandante.car_qtd_vermelho AS cartoes_vermelhos_mandante,
            cartao_mandante.car_qtd_amarelo AS cartoes_amarelos_mandante,
            cartao_visitante.car_qtd_vermelho AS cartoes_vermelhos_visitante,
            cartao_visitante.car_qtd_amarelo AS cartoes_amarelos_visitante
        FROM
            rodada
        JOIN estadio ON
            rodada.estadio_est_id = estadio.est_id
        JOIN clube AS clube_mandante ON
            rodada.clube_clu_sigla_mandante = clube_mandante.clu_sigla
        JOIN clube AS clube_visitante ON
            rodada.clube_clu_sigla_visitante = clube_visitante.clu_sigla
        LEFT OUTER JOIN cartao AS cartao_mandante ON
            rodada.rod_serie = cartao_mandante.car_serie
            AND rodada.rod_ano = cartao_mandante.car_ano
            AND rodada.clube_clu_sigla_mandante = cartao_mandante.clube_clu_sigla
        LEFT OUTER JOIN cartao AS cartao_visitante ON
            rodada.rod_serie = cartao_visitante.car_serie
            AND rodada.rod_ano = cartao_visitante.car_ano
            AND rodada.clube_clu_sigla_visitante = cartao_visitante.clube_clu_sigla
        WHERE
            rodada.rod_serie = :serie
            AND rodada.rod_ano = :ano
            AND rodada.rod_rodada = :rodada
        ORDER BY
            rodada.rod_rodada,
            rodada.rod_data,
            rodada.rod_sequencia
    """)

    # Executar a query diretamente no banco de dados
    resultados = db.execute(sql_query, {"serie": serie_upper, "ano": ano, "rodada": rodada}).fetchall()

    # Validar se há jogos correspondentes
    if not resultados:
        raise HTTPException(
            status_code=404,
            detail="Nenhum jogo encontrado para os parâmetros fornecidos."
        )

    # Construir o JSON da resposta
    jogos_da_rodada = []
    for jogo in resultados:
        jogos_da_rodada.append(
            JogoFormPlacarSchema(
                rod_serie=jogo.rodada_rod_serie,
                rod_ano=jogo.rodada_rod_ano,
                rod_rodada=jogo.rodada_rod_rodada,
                rod_sequencia=jogo.rodada_rod_sequencia,
                est_id=jogo.rodada_estadio_est_id,
                est_nome=jogo.est_nome,
                rod_data=jogo.rodada_rod_data,
                clube_clu_sigla_mandante=jogo.rodada_clube_clu_sigla_mandante,
                clu_nome_mandante=jogo.clu_nome_mandante,
                clu_link_escudo_mandante=jogo.clu_link_escudo_mandante,
                rod_gols_mandante=jogo.rodada_rod_gols_mandante,
                clube_clu_sigla_visitante=jogo.rodada_clube_clu_sigla_visitante,
                clu_nome_visitante=jogo.clu_nome_visitante,
                clu_link_escudo_visitante=jogo.clu_link_escudo_visitante,
                rod_gols_visitante=jogo.rodada_rod_gols_visitante,
                car_qtd_vermelho_mandante=jogo.cartoes_vermelhos_mandante,
                car_qtd_amarelo_mandante=jogo.cartoes_amarelos_mandante,
                car_qtd_vermelho_visitante=jogo.cartoes_vermelhos_visitante,
                car_qtd_amarelo_visitante=jogo.cartoes_amarelos_visitante,
                rod_partida_finalidaza=jogo.rodada_rod_partida_finalidaza,
                rod_calculou_classificacao=jogo.rodada_rod_calculou_classificacao,
            )
        )

    # Retornar o JSON completo
    return ListaJogosRodadaFormPlacarResponse(
        serie=serie_upper,
        ano=ano,
        rodada=rodada,
        jogos_da_rodada=jogos_da_rodada
    )
    # for (
    #     rodada_obj, est_nome, clu_nome_mandante, clu_link_escudo_mandante,
    #     clu_nome_visitante, clu_link_escudo_visitante,
    #     cartoes_vermelhos_mandante, cartoes_amarelos_mandante,
    #     cartoes_vermelhos_visitante, cartoes_amarelos_visitante
    # ) in resultados:
    #     jogos_da_rodada.append(
    #         JogoFormPlacarSchema(
    #             rod_serie=rodada_obj.rod_serie,
    #             rod_ano=rodada_obj.rod_ano,
    #             rod_rodada=rodada_obj.rod_rodada,
    #             rod_sequencia=rodada_obj.rod_sequencia,
    #             est_id=rodada_obj.estadio_est_id,
    #             est_nome=est_nome,
    #             rod_data=rodada_obj.rod_data,
    #             clube_clu_sigla_mandante=rodada_obj.clube_clu_sigla_mandante,
    #             clu_nome_mandante=clu_nome_mandante,
    #             clu_link_escudo_mandante=clu_link_escudo_mandante,
    #             rod_gols_mandante=rodada_obj.rod_gols_mandante,
    #             clube_clu_sigla_visitante=rodada_obj.clube_clu_sigla_visitante,
    #             clu_nome_visitante=clu_nome_visitante,
    #             clu_link_escudo_visitante=clu_link_escudo_visitante,
    #             rod_gols_visitante=rodada_obj.rod_gols_visitante,
    #             car_qtd_vermelho_mandante=cartoes_vermelhos_mandante,
    #             car_qtd_amarelo_mandante=cartoes_amarelos_mandante,
    #             car_qtd_vermelho_visitante=cartoes_vermelhos_visitante,
    #             car_qtd_amarelo_visitante=cartoes_amarelos_visitante,
    #             rod_partida_finalidaza=rodada_obj.rod_partida_finalidaza,
    #             rod_calculou_classificacao=rodada_obj.rod_calculou_classificacao,
    #         )
    #     )

    # # Retornar o JSON completo
    # return ListaJogosRodadaFormPlacarResponse(
    #     serie=serie_upper,
    #     ano=ano,
    #     rodada=rodada,
    #     jogos_da_rodada=jogos_da_rodada
    # )