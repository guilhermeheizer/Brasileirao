select * from usuario;

SELECT usuario.id AS usuario_id, usuario.nome AS usuario_nome, usuario.email AS usuario_email, usuario.senha AS usuario_senha, usuario.ativo AS usuario_ativo, usuario.admin AS usuario_admin 
FROM usuario 
WHERE usuario.id = 1


SELECT cid_id, cid_nome, cid_uf
	FROM public.cidade;

SELECT est_id, est_nome, cidade_cid_id
	FROM public.estadio;

SELECT clu_sigla, clu_nome, clu_serie, clu_link_escudo, cidade_cid_id
	FROM public.clube;

SELECT car_serie, car_ano, clube_clu_sigla, car_qtd_vermelho, car_qtd_amarelo
FROM public.cartao
where car_serie = 'B'
and car_ano = 2027
and clube_clu_sigla = 'CRI';

select * from classificacao_rodada;




--delete from public.rodada

SELECT rod_rodada, rod_sequencia, rod_data, clube_clu_sigla_mandante, rod_gols_mandante, clube_clu_sigla_visitante, rod_gols_visitante, rod_pontos_mandante, rod_pontos_visitante, rod_calculou_classificacao, rod_partida_finalizada, estadio_est_id
	FROM public.rodada
where rod_serie = 'B' 
and rod_ano = 2026
and rod_rodada = 21;
	
select count(*) from rodada;
insert into rodada values ( 'A',2026,1,1,'2026-01-28 19:00:00','CAM',2,'PAL',2,1,1,'S','S',1);
insert into rodada values ( 'A',2026,1,2,'2026-01-28 19:00:00','INT',0,'CAP',1,0,3,'S','S',2);
insert into rodada values ( 'A',2026,1,3,'2026-01-28 19:00:00','CFC',0,'RBB',1,0,3,'S','S',3);
insert into rodada values ( 'A',2026,1,4,'2026-01-28 19:00:00','VIT',2,'REM',0,3,0,'S','S',4);
insert into rodada values ( 'A',2026,1,5,'2026-01-28 19:30:00','FLU',2,'GRE',1,3,0,'S','S',5);
insert into rodada values ( 'A',2026,1,6,'2026-01-28 20:00:00','COR',1,'BAH',2,0,3,'S','S',6);
insert into rodada values ( 'A',2026,1,7,'2026-01-28 20:00:00','CHA',4,'SAN',2,3,0,'S','S',7);
insert into rodada values ( 'A',2026,1,8,'2026-01-28 21:30:00','SAO',2,'FLA',1,3,0,'S','S',8);
insert into rodada values ( 'A',2026,1,9,'2026-01-29 20:00:00','MIR',2,'VAS',1,3,0,'S','S',9);
insert into rodada values ( 'A',2026,1,10,'2026-01-29 21:30:00','BOT',4,'CRU',0,3,0,'S','S',10);
insert into rodada values ( 'A',2026,2,1,'2026-02-04 19:00:00','FLA',1,'INT',1,1,1,'S','S',5);
insert into rodada values ( 'A',2026,2,2,'2026-02-04 19:00:00','RBB',1,'CAM',0,3,0,'S','S',11);
insert into rodada values ( 'A',2026,2,3,'2026-02-04 19:00:00','SAN',1,'SAO',1,1,1,'S','S',6);
insert into rodada values ( 'A',2026,2,4,'2026-02-04 20:00:00','REM',2,'MIR',2,1,1,'S','S',12);
insert into rodada values ( 'A',2026,2,5,'2026-02-04 21:30:00','PAL',5,'VIT',1,3,0,'S','S',13);
insert into rodada values ( 'A',2026,2,6,'2026-02-04 21:30:00','GRE',5,'BOT',3,3,0,'S','S',14);
insert into rodada values ( 'A',2026,2,7,'2026-02-05 19:00:00','BAH',1,'FLU',1,1,1,'S','S',15);
insert into rodada values ( 'A',2026,2,8,'2026-02-05 20:00:00','VAS',1,'CHA',1,1,1,'S','S',16);
insert into rodada values ( 'A',2026,2,9,'2026-02-05 21:30:00','CRU',1,'CFC',2,0,3,'S','S',17);
insert into rodada values ( 'A',2026,2,10,'2026-02-19 19:30:00','CAP',0,'COR',1,0,3,'S','S',18);
insert into rodada values ( 'A',2026,3,1,'2026-02-10 21:30:00','VIT',1,'FLA',2,0,3,'S','S',4);
insert into rodada values ( 'A',2026,3,2,'2026-02-11 19:00:00','MIR',2,'CRU',2,1,1,'S','S',9);
insert into rodada values ( 'A',2026,3,3,'2026-02-11 19:00:00','CHA',3,'CFC',3,1,1,'S','S',7);
insert into rodada values ( 'A',2026,3,4,'2026-02-11 20:00:00','CAM',3,'REM',3,1,1,'S','S',1);
insert into rodada values ( 'A',2026,3,5,'2026-02-11 21:30:00','VAS',0,'BAH',1,0,3,'S','S',16);
insert into rodada values ( 'A',2026,3,6,'2026-02-11 21:30:00','SAO',2,'GRE',0,3,0,'S','S',8);
insert into rodada values ( 'A',2026,3,7,'2026-02-12 19:00:00','CAP',2,'SAN',1,3,0,'S','S',18);
insert into rodada values ( 'A',2026,3,8,'2026-02-12 19:30:00','FLU',1,'BOT',0,3,0,'S','S',5);
insert into rodada values ( 'A',2026,3,9,'2026-02-12 20:00:00','COR',2,'RBB',0,3,0,'S','S',19);
insert into rodada values ( 'A',2026,3,10,'2026-02-12 21:00:00','INT',1,'PAL',3,0,3,'S','S',2);
insert into rodada values ( 'A',2026,4,5,'2026-02-25 19:00:00','RBB',1,'CAP',1,1,1,'S','S',11);
insert into rodada values ( 'A',2026,4,10,'2026-02-25 19:00:00','REM',1,'INT',1,1,1,'S','S',5);
insert into rodada values ( 'A',2026,4,15,'2026-02-25 19:30:00','CFC',0,'SAO',1,0,3,'S','S',3);
insert into rodada values ( 'A',2026,4,20,'2026-02-25 20:00:00','CRU',1,'COR',1,1,1,'S','S',17);
insert into rodada values ( 'A',2026,4,25,'2026-02-25 21:30:00','PAL',2,'FLU',1,3,0,'S','S',13);
insert into rodada values ( 'A',2026,4,30,'2026-02-25 21:30:00','GRE',2,'CAM',1,3,0,'S','S',14);
insert into rodada values ( 'A',2026,4,35,'2026-02-26 19:00:00','SAN',2,'VAS',1,3,0,'S','S',6);
insert into rodada values ( 'A',2026,4,40,'2026-02-26 19:00:00','FLA',null,'MIR',null,null,null,'N','N',5);
insert into rodada values ( 'A',2026,4,45,'2026-02-26 19:00:00','BOT',null,'VIT',null,null,null,'N','N',10);
insert into rodada values ( 'A',2026,4,50,'2026-02-26 19:00:00','BAH',null,'CHA',null,null,null,'N','N',15);
insert into rodada values ( 'A',2026,5,5,'2026-03-10 21:30:00','MIR',2,'SAN',2,1,1,'S','S',9);
insert into rodada values ( 'A',2026,5,10,'2026-03-11 19:00:00','CAM',1,'INT',0,3,0,'S','S',1);
insert into rodada values ( 'A',2026,5,15,'2026-03-11 20:00:00','BAH',1,'VIT',1,1,1,'S','S',15);
insert into rodada values ( 'A',2026,5,20,'2026-03-11 20:00:00','FLA',2,'CRU',0,3,0,'S','S',5);
insert into rodada values ( 'A',2026,5,25,'2026-03-11 21:30:00','COR',0,'CFC',2,0,3,'S','S',19);
insert into rodada values ( 'A',2026,5,30,'2026-03-12 19:00:00','REM',0,'FLU',2,0,3,'S','S',12);
insert into rodada values ( 'A',2026,5,35,'2026-03-12 19:30:00','VAS',2,'PAL',1,3,0,'S','S',16);
insert into rodada values ( 'A',2026,5,40,'2026-03-12 20:00:00','SAO',2,'CHA',0,3,0,'S','S',20);
insert into rodada values ( 'A',2026,5,45,'2026-03-26 21:30:00','GRE',1,'RBB',1,1,1,'S','S',14);
insert into rodada values ( 'A',2026,5,50,'2026-03-29 18:30:00','CAP',4,'BOT',1,3,0,'S','S',18);
insert into rodada values ( 'A',2026,6,5,'2026-03-14 18:30:00','VIT',2,'CAM',0,3,0,'S','S',4);
insert into rodada values ( 'A',2026,6,10,'2026-03-14 20:30:00','BOT',0,'FLA',3,0,3,'S','S',10);
insert into rodada values ( 'A',2026,6,15,'2026-03-15 14:16:00','FLU',3,'CAP',2,3,0,'S','S',5);
insert into rodada values ( 'A',2026,6,20,'2026-03-15 16:00:00','SAN',1,'COR',1,1,1,'S','S',6);
insert into rodada values ( 'A',2026,6,25,'2026-03-15 16:00:00','INT',0,'BAH',1,0,3,'S','S',2);
insert into rodada values ( 'A',2026,6,30,'2026-03-15 18:30:00','PAL',1,'MIR',0,3,0,'S','S',21);
insert into rodada values ( 'A',2026,6,35,'2026-03-15 18:30:00','CFC',1,'REM',0,3,0,'S','S',3);
insert into rodada values ( 'A',2026,6,40,'2026-03-15 20:30:00','RBB',1,'SAO',2,0,3,'S','S',11);
insert into rodada values ( 'A',2026,6,45,'2026-03-15 20:30:00','CRU',3,'VAS',3,1,1,'S','S',17);
insert into rodada values ( 'A',2026,6,50,'2026-03-16 20:30:00','CHA',1,'GRE',1,1,1,'S','S',7);
insert into rodada values ( 'A',2026,7,5,'2026-03-18 19:00:00','PAL',2,'BOT',1,3,0,'S','S',21);
insert into rodada values ( 'A',2026,7,10,'2026-03-18 19:00:00','BAH',2,'RBB',0,3,0,'S','S',15);
insert into rodada values ( 'A',2026,7,15,'2026-03-18 19:30:00','CAP',2,'CRU',1,3,0,'S','S',18);
insert into rodada values ( 'A',2026,7,20,'2026-03-18 20:00:00','MIR',0,'CFC',1,0,3,'S','S',9);
insert into rodada values ( 'A',2026,7,25,'2026-03-18 20:00:00','CAM',1,'SAO',0,3,0,'S','S',1);
insert into rodada values ( 'A',2026,7,30,'2026-03-18 21:30:00','VAS',3,'FLU',2,3,0,'S','S',5);
insert into rodada values ( 'A',2026,7,35,'2026-03-18 21:30:00','SAN',1,'INT',2,0,3,'S','S',6);
insert into rodada values ( 'A',2026,7,40,'2026-03-19 19:00:00','GRE',2,'VIT',0,3,0,'S','S',14);
insert into rodada values ( 'A',2026,7,45,'2026-03-19 20:00:00','FLA',3,'REM',0,3,0,'S','S',5);
insert into rodada values ( 'A',2026,7,50,'2026-03-19 21:30:00','CHA',0,'COR',0,1,1,'S','S',7);
insert into rodada values ( 'A',2026,8,5,'2026-03-21 16:00:00','RBB',1,'BOT',2,0,3,'S','S',11);
insert into rodada values ( 'A',2026,8,10,'2026-03-21 18:30:00','FLU',1,'CAM',0,3,0,'S','S',5);
insert into rodada values ( 'A',2026,8,15,'2026-03-21 21:00:00','SAO',0,'PAL',1,0,3,'S','S',8);
insert into rodada values ( 'A',2026,8,20,'2026-03-22 16:00:00','VAS',2,'GRE',1,3,0,'S','S',16);
insert into rodada values ( 'A',2026,8,25,'2026-03-22 16:00:00','CRU',0,'SAN',0,1,1,'S','S',17);
insert into rodada values ( 'A',2026,8,30,'2026-03-22 16:00:00','CAP',2,'CFC',0,3,0,'S','S',5);
insert into rodada values ( 'A',2026,8,35,'2026-03-22 16:00:00','REM',4,'BAH',1,3,0,'S','S',12);
insert into rodada values ( 'A',2026,8,40,'2026-03-22 18:30:00','INT',2,'CHA',0,3,0,'S','S',2);
insert into rodada values ( 'A',2026,8,45,'2026-03-22 18:30:00','VIT',1,'MIR',0,3,0,'S','S',4);
insert into rodada values ( 'A',2026,8,50,'2026-03-22 20:30:00','COR',1,'FLA',1,1,1,'S','S',19);
insert into rodada values ( 'B',2026,1,5,'2026-03-21 17:00:00','VNO',2,'CRB',2,1,1,'S','S',23);
insert into rodada values ( 'B',2026,1,10,'2026-03-21 18:15:00','CEA',1,'SBD',1,1,1,'S','S',22);
insert into rodada values ( 'B',2026,1,15,'2026-03-21 19:15:00','OPE',1,'ACG',0,3,0,'S','S',24);
insert into rodada values ( 'B',2026,1,20,'2026-03-21 19:15:00','BSP',4,'FOR',0,3,0,'S','S',25);
insert into rodada values ( 'B',2026,1,25,'2026-03-21 20:30:00','CUI',0,'SPT',0,1,1,'S','S',26);
insert into rodada values ( 'B',2026,1,30,'2026-03-22 16:00:00','AVA',2,'JUV',0,3,0,'S','S',27);
insert into rodada values ( 'B',2026,1,35,'2026-03-22 16:00:00','NAU',0,'CRI',1,0,3,'S','S',28);
insert into rodada values ( 'B',2026,1,40,'2026-03-22 18:00:00','ATH',2,'PON',1,3,0,'S','S',29);
insert into rodada values ( 'B',2026,1,45,'2026-03-22 18:00:00','GOI',3,'AME',1,3,0,'S','S',30);
insert into rodada values ( 'B',2026,1,50,'2026-03-22 20:00:00','NOV',1,'LEC',3,0,3,'S','S',31);
insert into rodada values ( 'B',2026,2,5,'2026-03-31 18:30:00','JUV',0,'NOV',0,1,1,'S','S',23);
insert into rodada values ( 'B',2026,2,10,'2026-03-31 19:00:00','FOR',0,'CUI',0,1,1,'S','S',22);
insert into rodada values ( 'B',2026,2,15,'2026-04-01 18:00:00','AME',1,'BSP',2,0,3,'S','S',1);
insert into rodada values ( 'B',2026,2,20,'2026-04-01 19:00:00','LEC',2,'GOI',2,1,1,'S','S',33);
insert into rodada values ( 'B',2026,2,25,'2026-04-01 19:00:00','ACG',1,'NAU',2,0,3,'S','S',34);
insert into rodada values ( 'B',2026,2,30,'2026-04-01 19:00:00','SPT',1,'VNO',1,1,1,'S','S',35);
insert into rodada values ( 'B',2026,2,35,'2026-04-01 19:00:00','PON',1,'CEA',1,1,1,'S','S',36);
insert into rodada values ( 'B',2026,2,40,'2026-04-01 21:00:00','CRI',1,'ATH',1,1,1,'S','S',37);
insert into rodada values ( 'B',2026,2,45,'2026-04-01 21:30:00','CRB',0,'AVA',1,0,3,'S','S',38);
insert into rodada values ( 'B',2026,2,50,'2026-04-02 17:30:00','SBD',1,'OPE',2,0,3,'S','S',39);
insert into rodada values ( 'B',2026,3,5,'2026-04-04 16:00:00','FOR',2,'JUV',1,3,0,'S','S',22);
insert into rodada values ( 'B',2026,3,10,'2026-04-04 18:00:00','NAU',1,'PON',0,3,0,'S','S',28);
insert into rodada values ( 'B',2026,3,15,'2026-04-04 18:00:00','CUI',0,'CEA',2,0,3,'S','S',26);
insert into rodada values ( 'B',2026,3,20,'2026-04-04 20:00:00','VNO',2,'ACG',1,3,0,'S','S',23);
insert into rodada values ( 'B',2026,3,25,'2026-04-04 20:30:00','LEC',1,'SPT',2,0,3,'S','S',33);
insert into rodada values ( 'B',2026,3,30,'2026-04-04 20:30:00','AVA',0,'OPE',0,1,1,'S','S',27);
insert into rodada values ( 'B',2026,3,35,'2026-04-05 16:00:00','NOV',1,'CRB',1,1,1,'S','S',31);
insert into rodada values ( 'B',2026,3,40,'2026-04-06 18:00:00','GOI',1,'CRI',0,3,0,'S','S',30);
insert into rodada values ( 'B',2026,3,45,'2026-04-05 20:00:00','ATH',1,'AME',1,1,1,'S','S',29);
insert into rodada values ( 'B',2026,3,50,'2026-04-05 20:30:00','BSP',1,'SBD',2,0,3,'S','S',25);
insert into rodada values ( 'A',2026,9,5,'2026-04-01 19:30:00','BOT',3,'MIR',2,3,0,'S','S',10);
insert into rodada values ( 'A',2026,9,10,'2026-04-01 19:30:00','INT',1,'SAO',1,1,1,'S','S',2);
insert into rodada values ( 'A',2026,9,15,'2026-04-01 20:00:00','CRU',3,'VIT',0,3,0,'S','S',17);
insert into rodada values ( 'A',2026,9,20,'2026-04-01 20:00:00','BAH',3,'CAP',0,3,0,'S','S',15);
insert into rodada values ( 'A',2026,9,25,'2026-04-01 20:30:00','CFC',1,'VAS',1,1,1,'S','S',3);
insert into rodada values ( 'A',2026,9,30,'2026-04-01 21:30:00','FLU',3,'COR',1,3,0,'S','S',5);
insert into rodada values ( 'A',2026,9,35,'2026-04-02 19:00:00','SAN',2,'REM',0,3,0,'S','S',6);
insert into rodada values ( 'A',2026,9,40,'2026-04-02 19:00:00','CHA',0,'CAM',4,0,3,'S','S',7);
insert into rodada values ( 'A',2026,9,45,'2026-04-02 21:30:00','PAL',2,'GRE',1,3,0,'S','S',13);
insert into rodada values ( 'A',2026,9,50,'2026-04-02 21:30:00','RBB',3,'FLA',0,3,0,'S','S',11);
insert into rodada values ( 'A',2026,10,5,'2026-04-04 18:30:00','SAO',4,'CRU',1,3,0,'S','S',8);
insert into rodada values ( 'A',2026,10,10,'2026-04-04 20:30:00','CFC',1,'FLU',1,1,1,'S','S',3);
insert into rodada values ( 'A',2026,10,15,'2026-04-04 21:00:00','VAS',1,'BOT',2,0,3,'S','S',16);
insert into rodada values ( 'A',2026,10,20,'2026-04-05 16:00:00','CHA',1,'VIT',1,1,1,'S','S',7);
insert into rodada values ( 'A',2026,10,25,'2026-04-05 17:30:00','FLA',3,'SAN',1,3,0,'S','S',5);
insert into rodada values ( 'A',2026,10,30,'2026-04-05 17:30:00','CAM',2,'CAP',1,3,0,'S','S',1);
insert into rodada values ( 'A',2026,10,35,'2026-04-05 19:30:00','COR',0,'INT',1,0,3,'S','S',19);
insert into rodada values ( 'A',2026,10,40,'2026-04-05 19:30:00','BAH',1,'PAL',2,0,3,'S','S',15);
insert into rodada values ( 'A',2026,10,45,'2026-04-05 20:00:00','MIR',0,'RBB',1,0,3,'S','S',9);
insert into rodada values ( 'A',2026,10,50,'2026-04-05 20:30:00','GRE',0,'REM',0,1,1,'S','S',14);
insert into rodada values ( 'A',2026,11,5,'2026-04-11 16:30:00','VIT',2,'SAO',0,3,0,'S','S',4);
insert into rodada values ( 'A',2026,11,10,'2026-04-11 16:30:00','REM',1,'VAS',1,1,1,'S','S',12);
insert into rodada values ( 'A',2026,11,15,'2026-04-12 18:30:00','FLU',1,'FLA',2,0,3,'S','S',5);
insert into rodada values ( 'A',2026,11,20,'2026-04-11 18:30:00','MIR',1,'BAH',2,0,3,'S','S',9);
insert into rodada values ( 'A',2026,11,25,'2026-04-11 20:00:00','SAN',1,'CAM',0,3,0,'S','S',6);
insert into rodada values ( 'A',2026,11,30,'2026-04-11 20:30:00','INT',0,'GRE',0,1,1,'S','S',2);
insert into rodada values ( 'A',2026,11,35,'2026-04-12 11:00:00','CAP',2,'CHA',0,3,0,'S','S',18);
insert into rodada values ( 'A',2026,11,40,'2026-04-12 16:00:00','BOT',2,'CFC',2,1,1,'S','S',10);
insert into rodada values ( 'A',2026,11,45,'2026-04-12 18:30:00','COR',0,'PAL',0,1,1,'S','S',19);
insert into rodada values ( 'A',2026,11,50,'2026-04-12 18:30:00','CRU',2,'RBB',1,3,0,'S','S',17);
insert into rodada values ( 'A',2026,12,5,'2026-04-18 18:30:00','VAS',2,'SAO',1,3,0,'S','S',16);
insert into rodada values ( 'A',2026,12,10,'2026-04-18 18:30:00','CHA',1,'BOT',4,0,3,'S','S',7);
insert into rodada values ( 'A',2026,12,15,'2026-04-18 20:00:00','VIT',0,'COR',0,1,1,'S','S',4);
insert into rodada values ( 'A',2026,12,20,'2026-04-18 20:30:00','CRU',2,'GRE',0,3,0,'S','S',17);
insert into rodada values ( 'A',2026,12,25,'2026-04-19 16:00:00','SAN',2,'FLU',3,0,3,'S','S',6);
insert into rodada values ( 'A',2026,12,30,'2026-04-19 11:00:00','INT',1,'MIR',2,0,3,'S','S',2);
insert into rodada values ( 'A',2026,12,35,'2026-04-19 16:00:00','CFC',2,'CAM',0,3,0,'S','S',3);
insert into rodada values ( 'A',2026,12,40,'2026-04-19 18:30:00','PAL',1,'CAP',0,3,0,'S','S',21);
insert into rodada values ( 'A',2026,12,45,'2026-04-19 18:30:00','RBB',4,'REM',2,3,0,'S','S',11);
insert into rodada values ( 'A',2026,12,50,'2026-04-19 19:30:00','FLA',2,'BAH',0,3,0,'S','S',5);
insert into rodada values ( 'B',2026,4,5,'2026-04-10 20:30:00','CRI',1,'BSP',0,3,0,'S','S',37);
insert into rodada values ( 'B',2026,4,10,'2026-04-11 16:00:00','JUV',2,'GOI',0,3,0,'S','S',32);
insert into rodada values ( 'B',2026,4,15,'2026-04-11 18:00:00','PON',0,'VNO',1,0,3,'S','S',36);
insert into rodada values ( 'B',2026,4,20,'2026-04-11 18:00:00','SPT',2,'AVA',2,1,1,'S','S',35);
insert into rodada values ( 'B',2026,4,25,'2026-04-11 20:30:00','CEA',1,'NAU',0,3,0,'S','S',22);
insert into rodada values ( 'B',2026,4,30,'2026-04-12 18:00:00','SBD',0,'FOR',1,0,3,'S','S',9);
insert into rodada values ( 'B',2026,4,35,'2026-04-12 18:00:00','AME',0,'NOV',3,0,3,'S','S',40);
insert into rodada values ( 'B',2026,4,40,'2026-04-12 18:00:00','OPE',0,'CUI',0,1,1,'S','S',24);
insert into rodada values ( 'B',2026,4,45,'2026-04-12 20:00:00','CRB',2,'ATH',3,0,3,'S','S',38);
insert into rodada values ( 'B',2026,4,50,'2026-04-12 20:30:00','ACG',2,'LEC',1,3,0,'S','S',34);
insert into rodada values ( 'B',2026,5,5,'2026-04-18 18:00:00','AME',0,'SPT',0,1,1,'S','S',40);
insert into rodada values ( 'B',2026,5,10,'2026-04-18 18:00:00','NAU',0,'SBD',3,0,3,'S','S',28);
insert into rodada values ( 'B',2026,5,15,'2026-04-18 18:30:00','VNO',2,'OPE',1,3,0,'S','S',23);
insert into rodada values ( 'B',2026,5,20,'2026-04-18 20:30:00','AVA',1,'PON',2,0,3,'S','S',27);
insert into rodada values ( 'B',2026,5,25,'2026-04-18 20:45:00','CRB',0,'JUV',1,0,3,'S','S',38);
insert into rodada values ( 'B',2026,5,30,'2026-04-19 16:00:00','BSP',1,'ACG',1,1,1,'S','S',25);
insert into rodada values ( 'B',2026,5,35,'2026-04-19 16:00:00','LEC',0,'CEA',0,1,1,'S','S',41);
insert into rodada values ( 'B',2026,5,40,'2026-04-19 18:00:00','GOI',0,'CUI',2,0,3,'S','S',30);
insert into rodada values ( 'B',2026,5,45,'2026-04-19 20:00:00','NOV',2,'ATH',1,3,0,'S','S',31);
insert into rodada values ( 'B',2026,5,50,'2026-04-19 20:00:00','FOR',3,'CRI',2,3,0,'S','S',42);
insert into rodada values ( 'B',2026,6,5,'2026-04-22 21:30:00','CUI',1,'BSP',1,1,1,'S','S',26);
insert into rodada values ( 'B',2026,6,10,'2026-04-24 20:00:00','PON',1,'AME',0,3,0,'S','S',36);
insert into rodada values ( 'B',2026,6,15,'2026-04-25 20:30:00','SPT',1,'NOV',0,3,0,'S','S',35);
insert into rodada values ( 'B',2026,6,20,'2026-04-25 21:00:00','JUV',1,'LEC',0,3,0,'S','S',32);
insert into rodada values ( 'B',2026,6,25,'2026-04-26 16:00:00','SBD',1,'GOI',0,3,0,'S','S',39);
insert into rodada values ( 'B',2026,6,30,'2026-04-26 18:00:00','OPE',0,'FOR',0,1,1,'S','S',24);
insert into rodada values ( 'B',2026,6,35,'2026-04-26 18:00:00','CEA',3,'VNO',3,1,1,'S','S',22);
insert into rodada values ( 'B',2026,6,40,'2026-04-26 20:30:00','ACG',2,'AVA',1,3,0,'S','S',34);
insert into rodada values ( 'B',2026,6,45,'2026-04-26 20:30:00','CRI',3,'CRB',1,3,0,'S','S',37);
insert into rodada values ( 'B',2026,6,50,'2026-04-27 19:00:00','ATH',0,'NAU',1,0,3,'S','S',29);
insert into rodada values ( 'A',2026,13,5,'2026-04-25 18:30:00','BOT',2,'INT',2,1,1,'S','S',43);
insert into rodada values ( 'A',2026,13,10,'2026-04-25 18:30:00','BAH',2,'SAN',2,1,1,'S','S',15);
insert into rodada values ( 'A',2026,13,15,'2026-04-25 18:30:00','REM',0,'CRU',1,0,3,'S','S',44);
insert into rodada values ( 'A',2026,13,20,'2026-04-25 21:00:00','SAO',1,'MIR',0,3,0,'S','S',45);
insert into rodada values ( 'A',2026,13,25,'2026-04-26 16:00:00','COR',1,'VAS',0,3,0,'S','S',19);
insert into rodada values ( 'A',2026,13,30,'2026-04-26 16:00:00','GRE',1,'CFC',0,3,0,'S','S',14);
insert into rodada values ( 'A',2026,13,35,'2026-04-26 18:30:00','RBB',0,'PAL',1,0,3,'S','S',11);
insert into rodada values ( 'A',2026,13,40,'2026-04-26 18:30:00','CAP',3,'VIT',1,3,0,'S','S',18);
insert into rodada values ( 'A',2026,13,45,'2026-04-26 20:30:00','FLU',2,'CHA',1,3,0,'S','S',5);
insert into rodada values ( 'A',2026,13,50,'2026-04-26 20:30:00','CAM',0,'FLA',4,0,3,'S','S',1);
insert into rodada values ( 'A',2026,14,5,'2026-05-02 16:00:00','BOT',1,'REM',2,0,3,'S','S',10);
insert into rodada values ( 'A',2026,14,10,'2026-05-02 18:30:00','PAL',1,'SAN',1,1,1,'S','S',21);
insert into rodada values ( 'A',2026,14,15,'2026-05-02 18:30:00','VIT',4,'CFC',1,3,0,'S','S',4);
insert into rodada values ( 'A',2026,14,20,'2026-05-02 20:30:00','CAP',0,'GRE',0,1,1,'S','S',18);
insert into rodada values ( 'A',2026,14,25,'2026-05-02 21:00:00','CRU',1,'CAM',3,0,3,'S','S',17);
insert into rodada values ( 'A',2026,14,30,'2026-05-03 16:00:00','FLA',2,'VAS',2,1,1,'S','S',5);
insert into rodada values ( 'A',2026,14,35,'2026-05-03 16:00:00','SAO',2,'BAH',2,1,1,'S','S',11);
insert into rodada values ( 'A',2026,14,40,'2026-05-03 18:30:00','INT',2,'FLU',0,3,0,'S','S',2);
insert into rodada values ( 'A',2026,14,45,'2026-05-03 18:30:00','CHA',1,'RBB',2,0,3,'S','S',7);
insert into rodada values ( 'A',2026,14,50,'2026-05-03 20:30:00','MIR',2,'COR',1,3,0,'S','S',9);
insert into rodada values ( 'B',2026,7,5,'2026-05-02 16:00:00','BSP',1,'NAU',1,1,1,'S','S',25);
insert into rodada values ( 'B',2026,7,10,'2026-05-02 18:30:00','CUI',1,'CRI',1,1,1,'S','S',26);
insert into rodada values ( 'B',2026,7,15,'2026-05-02 20:30:00','FOR',4,'GOI',1,3,0,'S','S',22);
insert into rodada values ( 'B',2026,7,20,'2026-05-03 16:00:00','SBD',3,'PON',0,3,0,'S','S',39);
insert into rodada values ( 'B',2026,7,25,'2026-05-03 16:00:00','OPE',3,'LEC',0,3,0,'S','S',24);
insert into rodada values ( 'B',2026,7,30,'2026-05-03 18:00:00','SPT',2,'CEA',0,3,0,'S','S',35);
insert into rodada values ( 'B',2026,7,35,'2026-05-03 18:30:00','ACG',0,'JUV',0,1,1,'S','S',34);
insert into rodada values ( 'B',2026,7,40,'2026-05-03 20:30:00','AME',1,'CRB',2,0,3,'S','S',40);
insert into rodada values ( 'B',2026,7,45,'2026-05-03 20:30:00','AVA',3,'NOV',3,1,1,'S','S',27);
insert into rodada values ( 'B',2026,7,50,'2026-05-04 19:00:00','VNO',1,'ATH',1,1,1,'S','S',23);
insert into rodada values ( 'B',2026,8,5,'2026-05-09 16:00:00','GOI',1,'VNO',0,3,0,'S','S',30);
insert into rodada values ( 'B',2026,8,10,'2026-05-09 18:00:00','ATH',0,'CUI',0,1,1,'S','S',29);
insert into rodada values ( 'B',2026,8,15,'2026-05-09 18:30:00','PON',1,'SPT',3,0,3,'S','S',36);
insert into rodada values ( 'B',2026,8,20,'2026-05-09 19:00:00','CEA',0,'ACG',1,0,3,'S','S',22);
insert into rodada values ( 'B',2026,8,25,'2026-05-09 20:30:00','CRB',3,'OPE',0,3,0,'S','S',38);
insert into rodada values ( 'B',2026,8,30,'2026-05-09 21:15:00','JUV',0,'CRI',0,1,1,'S','S',32);
insert into rodada values ( 'B',2026,8,35,'2026-05-10 16:00:00','NAU',4,'AME',0,3,0,'S','S',28);
insert into rodada values ( 'B',2026,8,40,'2026-05-10 18:30:00','AVA',0,'FOR',0,1,1,'S','S',27);
insert into rodada values ( 'B',2026,8,45,'2026-05-10 19:30:00','NOV',1,'BSP',0,3,0,'S','S',31);
insert into rodada values ( 'B',2026,8,50,'2026-05-12 19:30:00','LEC',1,'SBD',3,0,3,'S','S',41);
insert into rodada values ( 'A',2026,15,5,'2026-05-09 16:00:00','CFC',2,'INT',2,1,1,'S','S',3);
insert into rodada values ( 'A',2026,15,10,'2026-05-09 18:00:00','FLU',2,'VIT',2,1,1,'S','S',5);
insert into rodada values ( 'A',2026,15,15,'2026-05-09 21:00:00','BAH',1,'CRU',2,0,3,'S','S',15);
insert into rodada values ( 'A',2026,15,20,'2026-05-10 16:00:00','CAM',1,'BOT',1,1,1,'S','S',1);
insert into rodada values ( 'A',2026,15,25,'2026-05-10 16:00:00','REM',1,'PAL',1,1,1,'S','S',12);
insert into rodada values ( 'A',2026,15,30,'2026-05-10 18:30:00','SAN',2,'RBB',0,3,0,'S','S',6);
insert into rodada values ( 'A',2026,15,35,'2026-05-10 18:30:00','COR',3,'SAO',2,3,0,'S','S',19);
insert into rodada values ( 'A',2026,15,40,'2026-05-10 18:30:00','MIR',1,'CHA',1,1,1,'S','S',9);
insert into rodada values ( 'A',2026,15,45,'2026-05-10 19:30:00','GRE',0,'FLA',1,0,3,'S','S',14);
insert into rodada values ( 'A',2026,15,50,'2026-05-10 20:30:00','VAS',1,'CAP',0,3,0,'S','S',16);
insert into rodada values ( 'B',2026,9,5,'2026-05-16 16:00:00','SBD',1,'AME',1,1,1,'S','S',39);
insert into rodada values ( 'B',2026,9,10,'2026-05-16 16:00:00','OPE',2,'NAU',6,0,3,'S','S',24);
insert into rodada values ( 'B',2026,9,15,'2026-05-16 18:30:00','GOI',1,'BSP',0,3,0,'S','S',30);
insert into rodada values ( 'B',2026,9,20,'2026-05-16 20:30:00','CUI',0,'NOV',0,1,1,'S','S',26);
insert into rodada values ( 'B',2026,9,25,'2026-05-17 16:00:00','ATH',1,'JUV',1,1,1,'S','S',29);
insert into rodada values ( 'B',2026,9,30,'2026-05-17 18:00:00','VNO',2,'AVA',0,3,0,'S','S',23);
insert into rodada values ( 'B',2026,9,35,'2026-05-17 18:30:00','CEA',2,'FOR',1,3,0,'S','S',22);
insert into rodada values ( 'B',2026,9,40,'2026-05-17 18:30:00','CRI',1,'ACG',1,1,1,'S','S',37);
insert into rodada values ( 'B',2026,9,45,'2026-05-17 20:30:00','SPT',1,'CRB',2,0,3,'S','S',35);
insert into rodada values ( 'B',2026,9,50,'2026-05-18 19:00:00','PON',1,'LEC',4,0,3,'S','S',36);
insert into rodada values ( 'A',2026,16,5,'2026-05-16 18:30:00','CAM',3,'MIR',1,3,0,'S','S',1);
insert into rodada values ( 'A',2026,16,10,'2026-05-16 18:30:00','INT',4,'VAS',1,3,0,'S','S',2);
insert into rodada values ( 'A',2026,16,15,'2026-05-16 19:00:00','FLU',2,'SAO',1,3,0,'S','S',5);
insert into rodada values ( 'A',2026,16,20,'2026-05-16 21:00:00','PAL',1,'CRU',1,1,1,'S','S',13);
insert into rodada values ( 'A',2026,16,25,'2026-05-17 11:00:00','SAN',0,'CFC',3,0,3,'S','S',19);
insert into rodada values ( 'A',2026,16,30,'2026-05-17 16:00:00','BOT',3,'COR',1,3,0,'S','S',10);
insert into rodada values ( 'A',2026,16,35,'2026-05-17 16:00:00','BAH',1,'GRE',1,1,1,'S','S',15);
insert into rodada values ( 'A',2026,16,40,'2026-05-17 18:30:00','RBB',2,'VIT',0,3,0,'S','S',11);
insert into rodada values ( 'A',2026,16,45,'2026-05-17 18:30:00','CHA',2,'REM',3,0,3,'S','S',7);
insert into rodada values ( 'A',2026,16,50,'2026-05-17 19:30:00','CAP',1,'FLA',1,1,1,'S','S',18);
insert into rodada values ( 'B',2026,10,5,'2026-05-22 16:00:00','NAU',1,'CUI',0,3,0,'S','S',28);
insert into rodada values ( 'B',2026,10,10,'2026-05-23 16:00:00','NOV',2,'CEA',1,3,0,'S','S',31);
insert into rodada values ( 'B',2026,10,15,'2026-05-23 18:30:00','FOR',3,'LEC',0,3,0,'S','S',22);
insert into rodada values ( 'B',2026,10,20,'2026-05-23 20:30:00','JUV',0,'SPT',1,0,3,'S','S',32);
insert into rodada values ( 'B',2026,10,25,'2026-05-24 16:00:00','ACG',0,'SBD',1,0,3,'S','S',34);
insert into rodada values ( 'B',2026,10,30,'2026-05-24 16:30:00','CRB',4,'PON',2,3,0,'S','S',38);
insert into rodada values ( 'B',2026,10,35,'2026-05-24 18:30:00','AME',1,'VNO',2,0,3,'S','S',40);
insert into rodada values ( 'B',2026,10,40,'2026-05-24 19:00:00','AVA',0,'GOI',2,0,3,'S','S',27);
insert into rodada values ( 'B',2026,10,45,'2026-05-24 20:30:00','OPE',1,'CRI',1,1,1,'S','S',24);
insert into rodada values ( 'B',2026,10,50,'2026-05-25 19:00:00','BSP',1,'ATH',2,0,3,'S','S',25);
insert into rodada values ( 'A',2026,17,5,'2026-05-23 17:00:00','SAO',1,'BOT',1,1,1,'S','S',8);
insert into rodada values ( 'A',2026,17,10,'2026-05-23 17:00:00','VIT',2,'INT',0,3,0,'S','S',4);
insert into rodada values ( 'A',2026,17,15,'2026-05-23 19:00:00','MIR',1,'FLU',0,3,0,'S','S',9);
insert into rodada values ( 'A',2026,17,20,'2026-05-23 19:00:00','GRE',3,'SAN',2,3,0,'S','S',14);
insert into rodada values ( 'A',2026,17,25,'2026-05-23 21:00:00','FLA',0,'PAL',3,0,3,'S','S',5);
insert into rodada values ( 'A',2026,17,30,'2026-05-24 16:00:00','CRU',2,'CHA',1,3,0,'S','S',17);
insert into rodada values ( 'A',2026,17,35,'2026-05-24 16:00:00','REM',1,'CAP',2,0,3,'S','S',12);
insert into rodada values ( 'A',2026,17,40,'2026-05-24 18:30:00','COR',1,'CAM',0,3,0,'S','S',19);
insert into rodada values ( 'A',2026,17,45,'2026-05-24 20:30:00','VAS',0,'RBB',3,0,3,'S','S',16);
insert into rodada values ( 'A',2026,17,50,'2026-05-25 20:00:00','CFC',3,'BAH',2,3,0,'S','S',3);
insert into rodada values ( 'A',2026,18,5,'2026-05-30 16:00:00','FLA',3,'CFC',0,3,0,'S','S',5);
insert into rodada values ( 'A',2026,18,10,'2026-05-30 16:00:00','CAP',1,'MIR',0,3,0,'S','S',18);
insert into rodada values ( 'A',2026,18,15,'2026-05-30 17:30:00','GRE',1,'COR',3,0,3,'S','S',14);
insert into rodada values ( 'A',2026,18,20,'2026-05-30 17:30:00','BAH',2,'BOT',1,3,0,'S','S',6);
insert into rodada values ( 'A',2026,18,25,'2026-05-30 20:00:00','SAN',3,'VIT',1,3,0,'S','S',6);
insert into rodada values ( 'A',2026,18,30,'2026-05-31 11:00:00','RBB',3,'INT',1,3,0,'S','S',11);
insert into rodada values ( 'A',2026,18,35,'2026-05-31 16:00:00','VAS',0,'CAM',1,0,3,'S','S',16);
insert into rodada values ( 'A',2026,18,40,'2026-05-31 16:00:00','PAL',1,'CHA',0,3,0,'S','S',21);
insert into rodada values ( 'A',2026,18,45,'2026-05-31 20:30:00','CRU',1,'FLU',1,1,1,'S','S',17);
insert into rodada values ( 'A',2026,18,50,'2026-05-31 20:30:00','REM',1,'SAO',0,3,0,'S','S',12);
insert into rodada values ( 'B',2026,11,5,'2026-05-29 21:00:00','JUV',3,'AME',0,3,0,'S','S',32);
insert into rodada values ( 'B',2026,11,10,'2026-05-30 16:00:00','ACG',1,'GOI',1,1,1,'S','S',34);
insert into rodada values ( 'B',2026,11,15,'2026-05-30 16:00:00','AVA',1,'CRI',2,0,3,'S','S',27);
insert into rodada values ( 'B',2026,11,20,'2026-05-30 18:00:00','ATH',1,'FOR',0,3,0,'S','S',29);
insert into rodada values ( 'B',2026,11,25,'2026-05-30 20:30:00','SPT',2,'NAU',0,3,0,'S','S',35);
insert into rodada values ( 'B',2026,11,30,'2026-05-31 11:00:00','SBD',1,'NOV',1,1,1,'S','S',39);
insert into rodada values ( 'B',2026,11,35,'2026-05-31 11:00:00','LEC',0,'VNO',1,0,3,'S','S',41);
insert into rodada values ( 'B',2026,11,40,'2026-05-31 16:00:00','CEA',1,'OPE',2,0,3,'S','S',22);
insert into rodada values ( 'B',2026,11,45,'2026-05-31 20:30:00','CUI',2,'CRB',0,3,0,'S','S',26);
insert into rodada values ( 'B',2026,11,50,'2026-06-01 19:00:00','PON',0,'BSP',0,1,1,'S','S',36);
insert into rodada values ( 'B',2026,12,5,'2026-06-05 20:00:00','OPE',2,'JUV',1,3,0,'S','S',3);
insert into rodada values ( 'B',2026,12,10,'2026-06-06 11:00:00','CRI',1,'LEC',0,3,0,'S','S',37);
insert into rodada values ( 'B',2026,12,15,'2026-06-07 16:00:00','CRB',2,'SBD',3,0,3,'S','S',38);
insert into rodada values ( 'B',2026,12,20,'2026-06-08 20:00:00','AME',1,'ACG',2,0,3,'S','S',40);
insert into rodada values ( 'B',2026,12,25,'2026-06-08 20:00:00','VNO',1,'BSP',0,3,0,'S','S',23);
insert into rodada values ( 'B',2026,12,30,'2026-06-09 19:00:00','PON',1,'CUI',2,0,3,'S','S',36);
insert into rodada values ( 'B',2026,12,35,'2026-06-09 19:00:00','NAU',0,'FOR',1,0,3,'S','S',28);
insert into rodada values ( 'B',2026,12,40,'2026-06-10 20:00:00','CEA',2,'AVA',1,3,0,'S','S',42);
insert into rodada values ( 'B',2026,12,45,'2026-06-10 20:00:00','GOI',0,'NOV',4,0,3,'S','S',30);
insert into rodada values ( 'B',2026,12,50,'2026-06-10 20:00:00','SPT',1,'ATH',1,1,1,'S','S',35);
insert into rodada values ( 'B',2026,13,5,'2026-06-12 19:00:00','ACG',3,'CRB',3,1,1,'S','S',34);
insert into rodada values ( 'B',2026,13,10,'2026-06-14 11:00:00','SBD',0,'SPT',0,1,1,'S','S',39);
insert into rodada values ( 'B',2026,13,15,'2026-06-14 11:00:00','JUV',3,'PON',0,3,0,'S','S',32);
insert into rodada values ( 'B',2026,13,20,'2026-06-14 16:00:00','ATH',1,'GOI',1,1,1,'S','S',29);
insert into rodada values ( 'B',2026,13,25,'2026-06-14 16:00:00','CUI',1,'VNO',0,3,0,'S','S',26);
insert into rodada values ( 'B',2026,13,30,'2026-06-14 19:00:00','BSP',2,'OPE',1,3,0,'S','S',25);
insert into rodada values ( 'B',2026,13,35,'2026-06-14 19:00:00','NOV',2,'NAU',2,1,1,'S','S',31);
insert into rodada values ( 'B',2026,13,40,'2026-06-15 21:00:00','LEC',3,'AVA',2,3,0,'S','S',41);
insert into rodada values ( 'B',2026,13,45,'2026-06-15 21:00:00','CRI',1,'CEA',1,1,1,'S','S',30);
insert into rodada values ( 'B',2026,13,50,'2026-06-16 20:00:00','FOR',0,'AME',3,0,3,'S','S',22);
insert into rodada values ( 'B',2026,14,5,'2026-06-18 21:00:00','SPT',1,'ACG',1,1,1,'S','S',35);
insert into rodada values ( 'B',2026,14,10,'2026-06-20 11:00:00','LEC',2,'ATH',0,3,0,'S','S',41);
insert into rodada values ( 'B',2026,14,15,'2026-06-20 19:00:00','CEA',0,'BSP',1,0,3,'S','S',42);
insert into rodada values ( 'B',2026,14,20,'2026-06-20 19:00:00','VNO',4,'NAU',3,3,0,'S','S',23);
insert into rodada values ( 'B',2026,14,25,'2026-06-21 11:00:00','AVA',1,'CUI',0,3,0,'S','S',27);
insert into rodada values ( 'B',2026,14,30,'2026-06-21 16:00:00','CRB',1,'FOR',1,1,1,'S','S',38);
insert into rodada values ( 'B',2026,14,35,'2026-06-21 17:00:00','SBD',0,'JUV',1,0,3,'S','S',39);
insert into rodada values ( 'B',2026,14,40,'2026-06-21 18:30:00','GOI',0,'OPE',3,0,3,'S','S',30);
insert into rodada values ( 'B',2026,14,45,'2026-06-22 20:00:00','PON',0,'NOV',2,0,3,'S','S',36);
insert into rodada values ( 'B',2026,14,50,'2026-06-23 20:00:00','AME',0,'CRI',1,0,3,'S','S',40);
insert into rodada values ( 'B',2026,15,5,'2026-06-25 20:30:00','CUI',2,'LEC',2,1,1,'S','S',26);
insert into rodada values ( 'B',2026,15,10,'2026-06-26 19:00:00','NOV',2,'VNO',1,3,0,'S','S',31);
insert into rodada values ( 'B',2026,15,15,'2026-06-27 11:00:00','OPE',1,'AME',0,3,0,'S','S',24);
insert into rodada values ( 'B',2026,15,20,'2026-06-27 16:00:00','CRI',1,'SBD',0,3,0,'S','S',37);
insert into rodada values ( 'B',2026,15,25,'2026-06-28 16:00:00','ATH',1,'AVA',0,3,0,'S','S',29);
insert into rodada values ( 'B',2026,15,30,'2026-06-28 16:00:00','ACG',2,'PON',0,3,0,'S','S',34);
insert into rodada values ( 'B',2026,15,35,'2026-06-28 16:00:00','JUV',2,'CEA',0,3,0,'S','S',32);
insert into rodada values ( 'B',2026,15,40,'2026-06-28 18:30:00','FOR',2,'SPT',1,3,0,'S','S',22);
insert into rodada values ( 'B',2026,15,45,'2026-06-28 18:30:00','NAU',0,'GOI',1,0,3,'S','S',28);
insert into rodada values ( 'B',2026,15,50,'2026-06-30 20:00:00','BSP',0,'CRB',1,0,3,'S','S',25);
insert into rodada values ( 'B',2026,16,5,'2026-07-02 20:00:00','CUI',1,'AME',0,3,0,'S','S',26);
insert into rodada values ( 'B',2026,16,10,'2026-07-02 21:00:00','FOR',2,'PON',0,3,0,'S','S',22);
insert into rodada values ( 'B',2026,16,15,'2026-07-04 16:00:00','NOV',3,'ACG',0,3,0,'S','S',31);
insert into rodada values ( 'B',2026,16,20,'2026-07-04 16:00:00','LEC',5,'CRB',0,3,0,'S','S',41);
insert into rodada values ( 'B',2026,16,25,'2026-07-04 16:00:00','CRI',1,'SPT',0,3,0,'S','S',37);
insert into rodada values ( 'B',2026,16,30,'2026-07-04 20:00:00','GOI',2,'CEA',0,3,0,'S','S',30);
insert into rodada values ( 'B',2026,16,35,'2026-07-05 20:30:00','NAU',0,'JUV',0,1,1,'S','S',28);
insert into rodada values ( 'B',2026,16,40,'2026-07-06 19:00:00','BSP',3,'AVA',1,3,0,'S','S',25);
insert into rodada values ( 'B',2026,16,45,'2026-07-06 19:00:00','VNO',2,'SBD',1,3,0,'S','S',23);
insert into rodada values ( 'B',2026,16,50,'2026-07-07 20:00:00','ATH',0,'OPE',1,0,3,'S','S',29);
insert into rodada values ( 'A',2026,19,5,'2026-07-16 19:30:00','BOT',2,'SAN',1,3,0,'N','S',10);
insert into rodada values ( 'A',2026,19,10,'2026-07-16 19:30:00','VIT',1,'VAS',0,3,0,'N','S',4);
insert into rodada values ( 'A',2026,19,15,'2026-07-17 20:00:00','FLU',1,'RBB',1,1,1,'N','S',5);
insert into rodada values ( 'A',2026,19,20,'2026-07-17 20:00:00','MIR',2,'GRE',1,3,0,'N','S',9);
insert into rodada values ( 'A',2026,19,25,'2026-07-21 19:30:00','CAM',null,'BAH',null,null,null,'N','N',1);
insert into rodada values ( 'A',2026,19,30,'2026-07-22 19:30:00','CFC',null,'PAL',null,null,null,'N','N',3);
insert into rodada values ( 'A',2026,19,35,'2026-07-22 21:30:00','SAO',null,'CAP',null,null,null,'N','N',11);
insert into rodada values ( 'A',2026,19,40,'2026-07-22 21:30:00','INT',null,'CRU',null,null,null,'N','N',2);
insert into rodada values ( 'A',2026,19,45,'2026-07-22 21:30:00','CHA',null,'FLA',null,null,null,'N','N',7);
insert into rodada values ( 'A',2026,19,50,'2026-07-23 19:30:00','COR',null,'REM',null,null,null,'N','N',19);
insert into rodada values ( 'B',2026,17,5,'2026-07-08 20:00:00','PON',1,'CRI',2,0,3,'S','S',36);
insert into rodada values ( 'B',2026,17,10,'2026-07-10 19:00:00','JUV',1,'VNO',0,3,0,'S','S',32);
insert into rodada values ( 'B',2026,17,15,'2026-07-10 20:00:00','SPT',3,'BSP',3,1,1,'S','S',35);
insert into rodada values ( 'B',2026,17,20,'2026-07-12 11:00:00','OPE',2,'NOV',1,3,0,'S','S',24);
insert into rodada values ( 'B',2026,17,25,'2026-07-12 16:00:00','SBD',2,'CUI',2,1,1,'S','S',39);
insert into rodada values ( 'B',2026,17,30,'2026-07-12 16:00:00','AVA',2,'NAU',0,3,0,'S','S',27);
insert into rodada values ( 'B',2026,17,35,'2026-07-12 18:00:00','ACG',1,'FOR',0,3,0,'S','S',34);
insert into rodada values ( 'B',2026,17,40,'2026-07-12 19:00:00','CRB',2,'GOI',2,1,1,'S','S',38);
insert into rodada values ( 'B',2026,17,45,'2026-07-13 19:00:00','AME',1,'LEC',1,1,1,'S','S',40);
insert into rodada values ( 'B',2026,17,50,'2026-07-13 20:30:00','CEA',0,'ATH',0,1,1,'S','S',42);
insert into rodada values ( 'B',2026,18,5,'2026-07-16 20:00:00','CRB',2,'NAU',1,3,0,'S','S',38);
insert into rodada values ( 'B',2026,18,10,'2026-07-17 19:00:00','SBD',1,'AVA',1,1,1,'S','S',39);
insert into rodada values ( 'B',2026,18,15,'2026-07-17 19:00:00','AME',1,'CEA',1,1,1,'S','S',40);
insert into rodada values ( 'B',2026,18,20,'2026-07-17 19:00:00','JUV',2,'CUI',0,3,0,'S','S',32);
insert into rodada values ( 'B',2026,18,25,'2026-07-17 21:00:00','LEC',0,'BSP',0,1,1,'S','S',41);
insert into rodada values ( 'B',2026,18,30,'2026-07-17 21:00:00','FOR',1,'NOV',0,3,0,'S','S',22);
insert into rodada values ( 'B',2026,18,35,'2026-07-18 16:00:00','PON',1,'GOI',2,0,3,'S','S',36);
insert into rodada values ( 'B',2026,18,40,'2026-07-18 16:00:00','CRI',2,'VNO',0,3,0,'S','S',37);
insert into rodada values ( 'B',2026,18,45,'2026-07-18 16:00:00','SPT',2,'OPE',2,1,1,'S','S',35);
insert into rodada values ( 'B',2026,18,50,'2026-07-18 18:00:00','ACG',0,'ATH',0,1,1,'S','S',34);
insert into rodada values ( 'B',2026,19,5,'2026-07-21 19:30:00','NOV',null,'CRI',null,null,null,'N','N',31);
insert into rodada values ( 'B',2026,19,10,'2026-07-21 19:30:00','AVA',null,'AME',null,null,null,'N','N',27);
insert into rodada values ( 'B',2026,19,15,'2026-07-21 21:35:00','VNO',null,'FOR',null,null,null,'N','N',23);
insert into rodada values ( 'B',2026,19,20,'2026-07-22 19:30:00','OPE',null,'PON',null,null,null,'N','N',24);
insert into rodada values ( 'B',2026,19,25,'2026-07-22 19:30:00','CEA',null,'CRB',null,null,null,'N','N',22);
insert into rodada values ( 'B',2026,19,30,'2026-07-22 20:30:00','GOI',null,'SPT',null,null,null,'N','N',30);
insert into rodada values ( 'B',2026,19,35,'2026-07-22 21:30:00','NAU',null,'LEC',null,null,null,'N','N',28);
insert into rodada values ( 'B',2026,19,40,'2026-07-23 19:30:00','ATH',null,'SBD',null,null,null,'N','N',29);
insert into rodada values ( 'B',2026,19,45,'2026-07-23 20:30:00','CUI',null,'ACG',null,null,null,'N','N',26);
insert into rodada values ( 'B',2026,19,50,'2026-07-23 21:30:00','BSP',null,'JUV',null,null,null,'N','N',25);

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'rodada';


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

 insert into clube values ('CEA', 'Ceará', 'B', 'https://s.sde.globo.com/media/organizations/2019/10/10/ceara.svg', 15);
 insert into clube values ('SBD', 'São Bernardo', 'B', 'https://s.sde.globo.com/media/organizations/2022/01/20/Sao_Bernardo.svg', 16);
 insert into clube values ('VNO', 'Vila Nova', 'B', 'https://s.sde.globo.com/media/organizations/2021/04/07/vilanova.svg', 17);
 insert into clube values ('CRB', 'CRB', 'B', 'https://s.sde.globo.com/media/organizations/2018/03/11/crb.svg', 18);
 insert into clube values ('OPE', 'Operário-PR', 'B', 'https://s.sde.globo.com/media/organizations/2018/12/27/Oper%C3%A1rio-PR.svg', 19);
 insert into clube values ('ACG', 'Atlético-GO', 'B', 'https://s.sde.globo.com/media/organizations/2020/07/02/atletico-go-2020.svg', 17);
 insert into clube values ('BSP', 'Botafogo-SP', 'B', 'https://s.sde.globo.com/media/organizations/2024/05/15/BFC.svg', 20);
 insert into clube values ('FOR', 'Fortaleza', 'B', 'https://s.sde.globo.com/media/organizations/2021/09/19/Fortaleza_2021_1.svg', 15);
 insert into clube values ('CUI', 'Cuiabá', 'B', 'https://s.sde.globo.com/media/organizations/2018/12/26/Cuiaba_EC.svg', 21);
 insert into clube values ('SPT', 'Sport', 'B', 'https://s.sde.globo.com/media/organizations/2018/03/11/sport.svg', 22);
 insert into clube values ('AVA', 'Avaí', 'B', 'https://s.sde.globo.com/media/organizations/2024/05/12/ava%C3%AD.svg', 23);
 insert into clube values ('JUV', 'Juventude', 'B', 'https://s.sde.globo.com/media/organizations/2021/04/29/Juventude-2021-01.svg', 24);
 insert into clube values ('NAU', 'Náutico', 'B', 'https://s.sde.globo.com/media/organizations/2019/01/03/Nautico.svg', 22);
 insert into clube values ('CRI', 'Criciúma', 'B', 'https://s.sde.globo.com/media/teams/2026/01/16/criciuma-2026-svg-79692.svg', 25);
 insert into clube values ('ATH', 'Athletic Club', 'B', 'https://s.sde.globo.com/media/organizations/2025/01/22/Athletic_Club-mineiro.svg', 26);
 insert into clube values ('PON', 'Ponte Preta', 'B', 'https://s.sde.globo.com/media/organizations/2019/03/17/ponte-preta.svg', 27);
 insert into clube values ('GOI', 'Goiás', 'B', 'https://s.sde.globo.com/media/organizations/2021/03/01/GOIAS-2021.svg', 17);
 insert into clube values ('AME', 'América-MG', 'B', 'https://s.sde.globo.com/media/organizations/2024/05/07/America-MG-branco.svg', 13);
 insert into clube values ('NOV', 'Novorizontino', 'B', 'https://s.sde.globo.com/media/organizations/2019/01/08/Novohorizontino.svg', 28);
 insert into clube values ('LEC', 'Londrina', 'B', 'https://s.sde.globo.com/media/organizations/2018/03/11/londrina.svg', 29);

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

insert into estadio values (22, 'Castelão', 15);
insert into estadio values (23, 'OBA', 17);
insert into estadio values (24, 'Germano Kruger', 19);
insert into estadio values (25, 'Arena Nicnet', 20);
insert into estadio values (26, 'Arena Pantanal', 21);
insert into estadio values (27, 'Ressacada', 23);
insert into estadio values (28, 'Aflitos', 22);
insert into estadio values (29, 'Arena Sicredi', 26);
insert into estadio values (30, 'Hailé Pinheiro Serrinha', 17);
insert into estadio values (31, 'Jorge Ismael de Biasi', 28);
insert into estadio values (32, 'Alfredo Jaconi', 24);
insert into estadio values (33, 'Estádio do Café', 29);
insert into estadio values (34, 'Antônio Accioly', 17);
insert into estadio values (35, 'Ilha do Retiro', 22);
insert into estadio values (36, 'Moisés Lucarelli', 27);
insert into estadio values (37, 'Heriberto Hülse', 25);
insert into estadio values (38, 'Rei Pelé', 18);
insert into estadio values (39, 'Primeiro de Maio', 16);
insert into estadio values (40, 'Independência', 13);

INSERT INTO cartao VALUES('A', 2026, 'BOT', 0, 2);
INSERT INTO cartao VALUES('A', 2026, 'CHA', 0, 3);
INSERT INTO cartao VALUES('A', 2026, 'VIT', 0, 2);
INSERT INTO cartao VALUES('A', 2026, 'FLU', 0, 1);
INSERT INTO cartao VALUES('A', 2026, 'BAH', 2, 4);
INSERT INTO cartao VALUES('A', 2026, 'CAP', 0, 1);
INSERT INTO cartao VALUES('A', 2026, 'RBB', 0, 6);
INSERT INTO cartao VALUES('A', 2026, 'PAL', 0, 2);
INSERT INTO cartao VALUES('A', 2026, 'CAM', 1, 4);
INSERT INTO cartao VALUES('A', 2026, 'GRE', 0, 2);
INSERT INTO cartao VALUES('A', 2026, 'COR', 0, 2);
INSERT INTO cartao VALUES('A', 2026, 'FLA', 1, 0);
INSERT INTO cartao VALUES('A', 2026, 'CFC', 0, 1);

INSERT INTO estadio
(est_id, est_nome, cidade_cid_id)
VALUES(0, 'Canindé', 7);

select * from cidade c 

select * from usuario u 
select clu_sigla, clu_nome from clube
where clu_serie = 'B'
order by clu_nome

select * from cartao c where car_serie = "B"
select * from estadio
select c.clu_sigla, (c.clu_nome ), c.clu_serie, c.cidade_cid_id, c.clu_link_escudo  
from clube c 

select clu_nome as nome, clu_sigla as sigla   
  from clube
 where clu_serie = ?
 
--delete from rodada where rod_rodada = 4
SELECT * from rodada r 
where r.clube_clu_sigla_mandante = "VAS"
or r.clube_clu_sigla_visitante = "VAS"
--r.rod_rodada = 10
--and r.rod_serie  = "A"
order by r.rod_serie, r.rod_ano, r.rod_rodada,  r.rod_sequencia 

-- Verifica jogos atrasados
SELECT 
	rodada.rod_serie AS rodada_rod_serie,
	rodada.rod_ano AS rodada_rod_ano,
	rodada.rod_rodada AS rodada_rod_rodada,
	rodada.rod_sequencia AS rodada_rod_sequencia,
	rodada.rod_data AS rodada_rod_data,
	rodada.clube_clu_sigla_mandante AS rodada_clube_clu_sigla_mandante,
	rodada.clube_clu_sigla_visitante AS rodada_clube_clu_sigla_visitante,
	rodada.rod_pontos_mandante AS rodada_rod_pontos_mandante,
	rodada.rod_pontos_visitante AS rodada_rod_pontos_visitante,
	rodada.rod_calculou_classificacao AS rodada_rod_calculou_classificacao,
	rodada.estadio_est_id AS rodada_estadio_est_id,
	estadio.est_nome AS est_nome,
	clube_mandante.clu_nome AS clu_nome_mandante,
	clube_mandante.clu_link_escudo AS clu_link_escudo_mandante,
	clube_visitante.clu_nome AS clu_nome_visitante,
	clube_visitante.clu_link_escudo AS clu_link_escudo_visitante
FROM rodada
JOIN estadio ON
	rodada.estadio_est_id = estadio.est_id
JOIN clube AS clube_mandante ON
	rodada.clube_clu_sigla_mandante = clube_mandante.clu_sigla
JOIN clube AS clube_visitante ON
	rodada.clube_clu_sigla_visitante = clube_visitante.clu_sigla
WHERE rodada.rod_serie = 'A'
  AND rodada.rod_ano = 2026
  AND rodada.rod_partida_finalizada = 'N'
  AND rodada.rod_rodada IN (
        SELECT r2.rod_rodada
        FROM rodada r2
        WHERE r2.rod_serie = 'A'
          AND r2.rod_ano = 2026
          AND r2.rod_partida_finalizada = 'N'
        GROUP BY r2.rod_rodada
        HAVING COUNT(*) <> 10
  )
ORDER BY rodada.rod_data desc;


update rodada
set rod_calculou_classificacao = "N"
where rod_partida_finalizada = "S"
and rod_serie = "B"
and rod_ano = 2026

INSERT INTO rodada (rod_serie, rod_ano, rod_rodada, rod_sequencia, rod_data, clube_clu_sigla_mandante, rod_gols_mandante, clube_clu_sigla_visitante, rod_gols_visitante, rod_pontos_mandante, rod_pontos_visitante, rod_calculou_classificacao, rod_partida_finalizada, estadio_est_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
('A', 2026, 4, 5, '2026-02-25 19:00:00.000000', 'RBB', None, 'CAP', None, None, None, 'N', 'N', 11), 
('A', 2026, 4, 10, '2026-02-25 19:00:00.000000', 'REM', None, 'INT', None, None, None, 'N', 'N', 5), 
('A', 2026, 4, 15, '2026-02-25 19:30:00.000000', 'CFC', None, 'SAO', None, None, None, 'N', 'N', 3), 
('A', 2026, 4, 20, '2026-02-25 20:00:00.000000', 'CRU', None, 'COR', None, None, None, 'N', 'N', 17), 
('A', 2026, 4, 25, '2026-02-25 21:30:00.000000', 'PAL', None, 'FLU', None, None, None, 'N', 'N', 13), 
('A', 2026, 4, 30, '2026-02-25 21:30:00.000000', 'GRE', None, 'CAM', None, None, None, 'N', 'N', 14), 
('A', 2026, 7, 35, '2026-02-26 19:00:00.000000', 'SAN', None, 'VAS', None, None, None, 'N', 'N', 6), 
('A', 2026, 4, 40, '2026-02-26 19:00:00.000000', 'FLA', None, 'MIR', None, None, None, 'N', 'N', 5), 
('A', 2026, 4, 45, '2026-02-26 19:00:00.000000', 'BOT', None, 'VIT', None, None, None, 'N', 'N', 10), 
('A', 2026, 4, 50, '2026-02-26 19:00:00.000000', 'BAH', None, 'CHA', None, None, None, 'N', 'N', 15)

-- Lista rodada
       SELECT
            rodada.rod_serie AS rodada_rod_serie,
            rodada.rod_ano AS rodada_rod_ano,
            rodada.rod_rodada AS rodada_rod_rodada,
            rodada.rod_sequencia AS rodada_rod_sequencia,
            rodada.estadio_est_id AS rodada_estadio_est_id,
            estadio.est_nome AS est_nome,
            rodada.rod_data AS rodada_rod_data,

            rodada.clube_clu_sigla_mandante AS rodada_clube_clu_sigla_mandante,
            clube_mandante.clu_nome AS clu_nome_mandante,
            clube_mandante.clu_link_escudo AS clu_link_escudo_mandante,
            COALESCE(rodada.rod_gols_mandante, NULL) AS rodada_rod_gols_mandante,
            COALESCE(rodada.rod_pontos_mandante, NULL) AS rodada_rod_pontos_mandante,

            rodada.clube_clu_sigla_visitante AS rodada_clube_clu_sigla_visitante,
            clube_visitante.clu_nome AS clu_nome_visitante,
            clube_visitante.clu_link_escudo AS clu_link_escudo_visitante,
            COALESCE(rodada.rod_gols_visitante, NULL) AS rodada_rod_gols_visitante,
            COALESCE(rodada.rod_pontos_visitante, NULL) AS rodada_rod_pontos_visitante,

            cartao_mandante.car_qtd_vermelho AS cartoes_vermelhos_mandante,
            cartao_mandante.car_qtd_amarelo AS cartoes_amarelos_mandante,
            cartao_visitante.car_qtd_vermelho AS cartoes_vermelhos_visitante,
            cartao_visitante.car_qtd_amarelo AS cartoes_amarelos_visitante,

            rodada.rod_partida_finalizada AS rodada_rod_partida_finalizada,
            rodada.rod_calculou_classificacao AS rodada_rod_calculou_classificacao
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
            rodada.rod_serie = 'A'
            AND rodada.rod_ano = '2026'
     AND rodada.rod_rodada = 22
        ORDER BY
            rodada.rod_rodada,
            rodada.rod_data,
            rodada.rod_sequencia

-- Lista rodada para informar placares 
       SELECT
            rodada.rod_serie AS rodada_rod_serie,
            rodada.rod_ano AS rodada_rod_ano,
            rodada.rod_rodada AS rodada_rod_rodada,
            rodada.rod_sequencia AS rodada_rod_sequencia,
            rodada.estadio_est_id AS rodada_estadio_est_id,
            estadio.est_nome AS est_nome,
            rodada.rod_data AS rodada_rod_data,

            rodada.clube_clu_sigla_mandante AS rodada_clube_clu_sigla_mandante,
            clube_mandante.clu_nome AS clu_nome_mandante,
            clube_mandante.clu_link_escudo AS clu_link_escudo_mandante,
            COALESCE(rodada.rod_gols_mandante, NULL) AS rodada_rod_gols_mandante,
            COALESCE(rodada.rod_pontos_mandante, NULL) AS rodada_rod_pontos_mandante,

            rodada.clube_clu_sigla_visitante AS rodada_clube_clu_sigla_visitante,
            clube_visitante.clu_nome AS clu_nome_visitante,
            clube_visitante.clu_link_escudo AS clu_link_escudo_visitante,
            COALESCE(rodada.rod_gols_visitante, NULL) AS rodada_rod_gols_visitante,
            COALESCE(rodada.rod_pontos_visitante, NULL) AS rodada_rod_pontos_visitante,

            cartao_mandante.car_qtd_vermelho AS cartoes_vermelhos_mandante,
            cartao_mandante.car_qtd_amarelo AS cartoes_amarelos_mandante,
            cartao_visitante.car_qtd_vermelho AS cartoes_vermelhos_visitante,
            cartao_visitante.car_qtd_amarelo AS cartoes_amarelos_visitante,

            rodada.rod_partida_finalizada AS rodada_rod_partida_finalizada,
            rodada.rod_calculou_classificacao AS rodada_rod_calculou_classificacao
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
            rodada.rod_serie = 'A'
            AND rodada.rod_ano = '2026'
            AND rodada.rod_rodada <= 23
	        AND rodada.rod_partida_finalizada = 'N'
        ORDER BY
            rodada.rod_rodada,
            rodada.rod_data,
            rodada.rod_sequencia

select * 
from rodada r 
where rod_serie = 'A'
and r.rod_ano  = 2026
and r.rod_rodada = 19

SELECT *
FROM classificacao_rodada
where classificacao_rodada.clr_serie = "B"
and classificacao_rodada.clr_rodada = 15;

UPDATE rodada
SET 
    rod_pontos_mandante = CASE
        WHEN rod_gols_mandante > rod_gols_visitante THEN 3
        WHEN rod_gols_mandante = rod_gols_visitante THEN 1
        ELSE 0
    END,
    
    rod_pontos_visitante = CASE
        WHEN rod_gols_visitante > rod_gols_mandante THEN 3
        WHEN rod_gols_visitante = rod_gols_mandante THEN 1
        ELSE 0
    END,
    
    rod_calculou_classificacao = 'N'
WHERE rod_partida_finalizada = 'S'
  AND rod_serie = "A"
  AND rod_ano = 2026
  AND rod_rodada = 12
  AND rod_sequencia = 15;
            
update rodada
set rod_partida_finalizada = "S",
    rod_calculou_classificacao = "N"
where rod_serie = "B"
  and rod_ano = 2026
  and rod_rodada = 1
  and rod_gols_mandante is not null
    
select * from cartao
--update cartao 
--set car_qtd_amarelo = car_qtd_amarelo + 1
where car_serie = "B"
and car_ano = 2026
and car_qtd_vermelho > 0


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
	AND rodada.rod_rodada = 4
ORDER BY
	rodada.rod_rodada,
	rodada.rod_data,
	rodada.rod_sequencia

select estadio.est_id, 
       estadio.est_nome, 
       estadio.cidade_cid_id, 
       cidade.cid_nome
from estadio
join cidade ON 
   cidade.cid_id = estadio.cidade_cid_id
order by estadio.est_id 
   
--delete from classificacao_geral where clg_serie =  "B"
select * from classificacao_geral
where clg_serie =  "A"

            SELECT MAX(rod_rodada) AS ultimo_numero FROM rodada
            WHERE rod_serie = :serie
            AND rod_ano = :ano
            
select * from classificacao_rodada 

SELECT clube_clu_sigla, 
    clg_pontos,
    clg_qtd_jogou,
    clg_vitorias,
    clg_qtd_empates,
    clg_qtd_derrotas,
    clg_gols_pro,
    clg_gols_contra,
    clg_saldo_gols
from classificacao_geral
WHERE clg_serie = "A" 
  and clg_ano = 2026
  and clube_clu_sigla = "CAM"
  
 UPDATE classificacao_geral
SET clg_pontos = clg_pontos + 1,
    clg_qtd_jogou = clg_qtd_jogou + 1,
    clg_vitorias = clg_vitorias + 0,
    clg_qtd_empates = clg_qtd_empates + 1,
    clg_qtd_derrotas = clg_qtd_derrotas + 2,
    clg_gols_pro = clg_gols_pro + 3,
    clg_gols_contra = clg_gols_contra + 8,
    clg_saldo_gols = clg_saldo_gols + 5
WHERE clg_serie = "A" 
  and clg_ano = 2026
  and clube_clu_sigla = "CRU"
                  
select cg.clg_id ,
       cg.clube_clu_sigla,
       clube.clu_nome,
       clube.clu_link_escudo,
       cg.clg_pontos,  
       cg.clg_qtd_jogou,
       cg.clg_vitorias, 
       cg.clg_qtd_empates,
       cg.clg_qtd_derrotas,
       cg.clg_gols_pro,
       cg.clg_gols_contra, 
       cg.clg_saldo_gols,  
       car_qtd_amarelo,
       car_qtd_vermelho 
from classificacao_geral cg 
JOIN cartao AS cartao ON
	cg.clg_serie = cartao.car_serie AND
	cg.clg_ano = cartao.car_ano AND
	cg.clube_clu_sigla = cartao.clube_clu_sigla 
JOIN clube AS clube ON
	cg.clube_clu_sigla = clube.clu_sigla 	
order by cg.clg_pontos desc, 
         cg.clg_vitorias desc, 
         cg.clg_saldo_gols desc, 
         cg.clg_gols_pro desc, 
         cartao.car_qtd_vermelho asc,
         cartao.car_qtd_amarelo asc
         
 SELECT clr_id, clr_serie, clr_ano, clr_rodada, clr_pontos, clr_vitorias, clr_saldo_gols, clr_gols_pro, clr_confronto_direto, clube_clu_sigla, clr_qtd_jogou, clr_qtd_empates, clr_qtd_derrotas, clr_gols_contra
FROM classificacao_rodada
where classificacao_rodada.clr_ano = 2026
and classificacao_rodada.clr_serie = "B";

SELECT
    clr_serie,
    clr_ano,
    COUNT(DISTINCT clr_rodada) AS total_rodadas
FROM classificacao_rodada
GROUP BY clr_serie, clr_ano
ORDER BY clr_ano, clr_serie;

SELECT
    clr_serie,
    clr_ano,
    clr_rodada,
    COUNT(*) AS qtde_jogos
FROM classificacao_rodada
GROUP BY clr_serie, clr_ano, clr_rodada
ORDER BY clr_ano, clr_serie, clr_rodada;

