
insert into cidade values (1, "Curitiba", "PR");
insert into cidade values (2, "Bragança Paulista", "SP");
insert into cidade values (3, "Salvador", "BA");
insert into cidade values (4, "Belém", "PA");
insert into cidade values (5, "Rio de Janeiro", "RJ");
insert into cidade values (6, "Porto Alegre", "RS");
insert into cidade values (7, "São Paulo", "SP");
insert into cidade values (8, "Santos", "SP");
insert into cidade values (9, "Chapecó", "SC");
insert into cidade values (10, "São Paulo", "SP");
insert into cidade values (11, "Rio de Janeiro", "RJ");
insert into cidade values (12, "Mirassol", "SP");
insert into cidade values (13, "Belo Horizonte", "MG");
insert into cidade values (14, "Baruei", "SP");

insert into clube values ("CAM", "Atlético-MG", "A", "", 13);
insert into clube values ("PAL", "Palmeiras", "A", "", 10);
insert into clube values ("INT", "Internacional", "A", "", 6);
insert into clube values ("CAP", "Athletico-PR", "A", "", 1);
insert into clube values ("CFC", "Coritiba", "A", "", 1);
insert into clube values ("RBB", "Bragantino", "A", "", 2);
insert into clube values ("VIT", "Vitória", "A", "", 3);
insert into clube values ("REM", "Remo", "A", "", 4);
insert into clube values ("FLU", "Fluminense", "A", "", 11);
insert into clube values ("GRE", "Grêmio", "A", "", 6);
insert into clube values ("COR", "Corinthians", "A", "", 7);
insert into clube values ("BAH", "Bahia", "A", "", 3);
insert into clube values ("SAN", "Santos", "A", "", 8);
insert into clube values ("CHA", "Chapecoense", "A", "", 9);
insert into clube values ("SAO", "São Paulo", "A", "", 10);
insert into clube values ("FLA", "Flamengo", "A", "", 11);
insert into clube values ("MIR", "Mirassol", "A", "", 12);
insert into clube values ("VAS", "Vasco", "A", "", 5);
insert into clube values ("BOT", "Botafogo", "A", "", 5);
insert into clube values ("CRU", "Cruzeiro", "A", "", 13);


update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2018/03/10/atletico-mg.svg"
where clu_sigla = "CAM";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2019/07/06/Palmeiras.svg"
where clu_sigla = "PAL";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2018/03/11/internacional.svg"
where clu_sigla =  "INT";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2026/01/07/Athletico-PR.svg"
where clu_sigla = "CAP";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2018/03/11/coritiba.svg"
where clu_sigla = "CFC";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2021/06/28/bragantino.svg"
where clu_sigla = "RBB";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2025/12/18/Vitoria_2025.svg"
where clu_sigla = "VIT";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2021/02/25/Remo-PA.svg"
where clu_sigla = "REM";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2018/03/11/fluminense.svg"
where clu_sigla = "FLU";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2018/03/12/gremio.svg"
where clu_sigla = "GRE";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2024/10/09/Corinthians_2024_Q4ahot4.svg"
where clu_sigla = "COR";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2018/03/11/bahia.svg"
where clu_sigla = "BAH";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2021/06/21/CHAPECOENSE-2018.svg"
where clu_sigla = "CHA";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2018/03/12/santos.svg"
where clu_sigla = "SAN";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2018/03/11/sao-paulo.svg"
where clu_sigla = "SAO";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2018/04/10/Flamengo-2018.svg"
where clu_sigla = "FLA";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2024/08/20/mirassol-novo-svg-71690.svg"
where clu_sigla = "MIR";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2021/09/04/vasco_SVG.svg"
where clu_sigla = "VAS";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2019/02/04/botafogo-svg.svg"
where clu_sigla = "BOT";
update clube set clu_link_escudo = "https://s.sde.globo.com/media/organizations/2021/02/13/cruzeiro_2021.svg"
where clu_sigla = "CRU";


insert into cartao values ("A", 2026, "CAM", 0, 0);
insert into cartao values ("A", 2026, "PAL", 0, 0);
insert into cartao values ("A", 2026, "INT", 0, 0);
insert into cartao values ("A", 2026, "CAP", 0, 0);
insert into cartao values ("A", 2026, "CFC", 0, 0);
insert into cartao values ("A", 2026, "RBB", 0, 0);
insert into cartao values ("A", 2026, "VIT", 0, 0);
insert into cartao values ("A", 2026, "REM", 0, 0);
insert into cartao values ("A", 2026, "FLU", 0, 0);
insert into cartao values ("A", 2026, "GRE", 0, 0);
insert into cartao values ("A", 2026, "COR", 0, 0);
insert into cartao values ("A", 2026, "BAH", 0, 0);
insert into cartao values ("A", 2026, "SAN", 0, 0);
insert into cartao values ("A", 2026, "CHA", 0, 0);
insert into cartao values ("A", 2026, "SAO", 0, 0);
insert into cartao values ("A", 2026, "FLA", 0, 0);
insert into cartao values ("A", 2026, "MIR", 0, 0);
insert into cartao values ("A", 2026, "VAS", 0, 0);
insert into cartao values ("A", 2026, "BOT", 0, 0);
insert into cartao values ("A", 2026, "CRU", 0, 0);

insert into estadio values (1, "Arena MRV", 13);
insert into estadio values (2, "Beira-Rio", 6);
insert into estadio values (3, "Couto Pereira", 1);
insert into estadio values (4, "Barradão", 3);
insert into estadio values (5, "Maracanã", 11);
insert into estadio values (6, "Vila Belmiro", 8);
insert into estadio values (7, "Arena Condá", 9);
insert into estadio values (8, "Morumbis", 10);
insert into estadio values (9, "Maião", 12);
insert into estadio values (10, "Nilton Santos", 11);
insert into estadio values (11, "Cícero de Souza Marques", 2);
insert into estadio values (12, "Mangueirão", 4);
insert into estadio values (13, "Arena Barueri", 14);
insert into estadio values (14, "Arena do Grêmio", 6);
insert into estadio values (15, "Arena Fonte Nova", 3);
insert into estadio values (16, "São Januário", 11);
insert into estadio values (17, "Mineirão", 13);	
insert into estadio values (18, "Arena da Baixada", 1);

select * from cidade c 

select * from usuario u 
select * from clube

select * from cartao c 
select * from estadio
select c.clu_sigla, (c.clu_nome ), c.clu_serie, c.cidade_cid_id, c.clu_link_escudo  
from clube c 

SELECT * from rodada r 

update rodada
set rod_gols_visitante = null,
    rod_gols_mandante = null
where rod_serie = "A"
  and rod_ano = 2026
  and rod_rodada = 2
    
select * from cartao


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
	rodada.rod_serie = "A"
	AND rodada.rod_ano = 2026
	AND rodada.rod_rodada = 1
ORDER BY
	rodada.rod_rodada,
	rodada.rod_data,
	rodada.rod_sequencia
