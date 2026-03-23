"""
form_classificacao_rodada_service.py

Este módulo implementa a lógica de serviço para copiar a classificação geral para a tabela de classificação por rodada.
Fornece função para persistir o estado da classificação geral ao final de uma rodada específica.

Funcionalidade principal:
- Copiar e salvar a classificação geral de uma rodada, preservando o histórico da competição

Utiliza SQLAlchemy para execução de SQL direto e persistência dos dados.
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.services.form.form_placar_rodada_service import calcular_classificacao_brasileirao
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.services.clube_service import consiste_serie


def copia_classificacao_por_rodada(db: Session, rodada: str, ano: int, serie: str):
    """
    Função para copiar a classificação geral para classificação por rodada.
    
    :param db: Instância da sessão do banco de dados
    :param rodada: Número ou nome da rodada
    :param ano: Ano da competição
    :param serie: Série do campeonato (A ou B)
    """
    # SQL para copiar a classificação geral para a tabela de classificação por rodada
    sql = text("""
        INSERT INTO classificacao_rodada (
            clr_serie, clr_ano, clr_rodada, clr_pontos, clr_vitorias, 
            clr_saldo_gols, clr_gols_pro, clr_confronto_direto, clube_clu_sigla,
            clr_qtd_jogou, clr_qtd_empates, clr_qtd_derrotas, clr_gols_contra
        )
        SELECT 
            clg_serie, clg_ano, :rodada AS clr_rodada, clg_pontos, clg_vitorias,
            clg_saldo_gols, clg_gols_pro, clg_confronto_direto, clube_clu_sigla,
            clg_qtd_jogou, clg_qtd_empates, clg_qtd_derrotas, clg_gols_contra
        FROM classificacao_geral
        WHERE clg_ano = :ano AND clg_serie = :serie
    """)

    # Executa o SQL com os parâmetros
    db.execute(sql, {"rodada": rodada, "ano": ano, "serie": serie})
    db.commit()


def recalcular_classificacao(db: Session, serie: str, ano: int):
    """
    Recalcula a classificação do campeonato para a série e ano especificados.
    """
    # Garantir que a série está em maiúsculo
    serie_upper = serie.upper()
    consiste_serie(serie_upper)

    try:
        # Passo 1: Atualizar a coluna rod_calculou_classificacao para "N" nas rodadas finalizadas
        db.execute(text("""
            UPDATE rodada
            SET rod_calculou_classificacao = 'N'
            WHERE rod_partida_finalizada = 'S'
            AND rod_serie = :serie
            AND rod_ano = :ano
        """), {"serie": serie_upper, "ano": ano})
        db.commit()

        # Passo 2: Excluir os registros da tabela classificacao_geral para a série e ano do campeonato
        db.execute(text("""
            DELETE FROM classificacao_geral
            WHERE clg_serie = :serie
            AND clg_ano = :ano
        """), {"serie": serie_upper, "ano": ano})
        db.commit()

        # Passo 3: Achar o número da última rodada do campeonato
        result = db.execute(text("""
            SELECT MAX(rod_numero) AS ultimo_numero FROM rodada
            WHERE rod_serie = :serie
            AND rod_ano = :ano
        """), {"serie": serie_upper, "ano": ano}).fetchone()
        ultimo_numero = result[0] if result and result[0] is not None else 0

        # Passo 4: Chamar a função calcular_classificacao_brasileirao
        calcular_classificacao_brasileirao(db, serie_upper, ano, ultimo_numero, True)
    except Exception as e:
        print(f"Erro ao recalcular classificação: {e}")
    finally:
        db.close()