from sqlalchemy.orm import Session
from sqlalchemy import text


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