# from sqlalchemy.orm import Session
# from fastapi import HTTPException
# from app.models.rodada_models import Rodada
# from app.models.clube_models import Clube
# from app.models.estadio_models import Estadio
# from app.services.clube_service import buscar_clube_sigla, consiste_serie, consiste_sigla
# from typing import List, Optional
# import re
# from app.schemas.rodada_schema import (
#     RodadaBaseSchema,
#     CriarRodadaSchema,
#     AtualizarRodadaPlacarSchema,
#     ResponseRodadaSchema,
#     ResponseRodadasSchema,
# )


# def carga_tabela(
#     rod_serie: str,
#     rod_ano: int,
#     session: Session
# ) -> ResponseRodadasSchema:
#     """

#     """
#     # 1. Validar os parâmetros principais
#     if not consiste_serie(rod_serie):
#         raise HTTPException(
#             status_code=400,
#             detail=f"Série '{rod_serie}' inválida. Use 'A' ou 'B'."
#         )

#     if len(jogos_data) != 10:
#         raise HTTPException(
#             status_code=400,
#             detail=f"A rodada deve conter exatamente 10 jogos. Recebido: {len(jogos_data)}."
#         )

#     # Validar unicidade das sequências dentro da lista fornecida
#     seq_set = set(j.rod_sequencia for j in jogos_data)
#     if len(seq_set) != 10:
#         raise HTTPException(
#             status_code=400,
#             detail="A lista de jogos contém sequências duplicadas."
#         )

#     # 2. Validar os jogos na rodada
#     for jogo in jogos_data:
#         if jogo.rod_serie != rod_serie or jogo.rod_ano != rod_ano:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Jogo com sequência {jogo.rod_sequencia} não possui série ou ano correspondentes: "
#                        f"Série: {jogo.rod_serie}, Ano: {jogo.rod_ano}."
#             )

#         # Validar clubes
#         if not consiste_sigla(jogo.clube_clu_sigla_mandante) or not consiste_sigla(jogo.clube_clu_sigla_visitante):
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Siglas de clubes inválidas no jogo {jogo.rod_sequencia}."
#             )

#         if jogo.clube_clu_sigla_mandante == jogo.clube_clu_sigla_visitante:
#             raise HTTPException(
#                 status_code=400,
#                 detail=f"Clube mandante e visitante são iguais no jogo {jogo.rod_sequencia}."
#             )

#         # Validar se os clubes existem
#         mandante = buscar_clube_sigla(True, jogo.clube_clu_sigla_mandante, session)
#         # retorna_exception: bool, clube_sigla: str, session: Session
#         if not mandante:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Clube mandante com sigla '{jogo.clube_clu_sigla_mandante}' não encontrado."
#             )

#         visitante = buscar_clube_sigla(True, jogo.clube_clu_sigla_visitante, session)
#         if not visitante:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Clube visitante com sigla '{jogo.clube_clu_sigla_visitante}' não encontrado."
#             )

#         # Validar estádio
#         estadio = db.query(Estadio).filter(Estadio.est_id == jogo.estadio_est_id).first()
#         if not estadio:
#             raise HTTPException(
#                 status_code=404,
#                 detail=f"Estádio com ID '{jogo.estadio_est_id}' não encontrado para o jogo {jogo.rod_sequencia}."
#             )

#         # Verificar se o jogo já existe no banco
#         jogo_existente = db.query(Rodada).filter(
#             Rodada.__table__.c.rod_serie == rod_serie,
#             Rodada.__table__.c.rod_ano == rod_ano,
#             Rodada.__table__.c.rod_rodada == jogo.rod_rodada,
#             Rodada.__table__.c.rod_sequencia == jogo.rod_sequencia
#         ).first()

#         if jogo_existente:
#             raise HTTPException(
#                 status_code=409,
#                 detail=f"Jogo com sequência '{jogo.rod_sequencia}', série '{rod_serie}', rodada '{jogo.rod_rodada}', "
#                        f"ano '{rod_ano}' já existe."
#             )

#     # 3. Adicionar os jogos no banco
#     rodadas = []
#     try:
#         for jogo in jogos_data:
#             nova_rodada = Rodada(
#                 rod_serie=rod_serie,
#                 rod_ano=rod_ano,
#                 rod_rodada=jogo.rod_rodada,
#                 rod_sequencia=jogo.rod_sequencia,
#                 rod_data=jogo.rod_data,
#                 clube_clu_sigla_mandante=jogo.clube_clu_sigla_mandante,
#                 clube_clu_sigla_visitante=jogo.clube_clu_sigla_visitante,
#                 rod_calculou_classificacao=jogo.rod_calculou_classificacao,
#                 rod_partida_finalidaza=jogo.rod_partida_finalidaza,
#                 estadio_est_id=jogo.estadio_est_id,
#             )
#             db.add(nova_rodada)
#             rodadas.append(nova_rodada)

#         # Commitar todas as alterações no banco
#         db.commit()

#         # Garantir que os objetos estão atualizados com a sessão
#         for rodada in rodadas:
#             db.refresh(rodada)

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=500,
#             detail=f"Ocorreu um erro ao salvar a rodada: {str(e)}"
#         )

#     # 4. Retornar os objetos criados no formato esperado
#     return ResponseRodadasSchema(rodadas=[ResponseRodadaSchema.from_orm(jogo) for jogo in rodadas])