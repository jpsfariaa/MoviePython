# Inserir Dados na Tabela 'Usuários'
INSERT INTO usuarios (nome_usuario, email, senha) VALUES ("João Pedro", "joao.faria3@fatec.sp.gov.br", "123abc");
COMMIT;

# Inserir Dados na Tabela 'Filmes'
INSERT INTO filmes (nome_filme, data_lancamento, nome_diretor, nome_ator) VALUES ("xXx: Return of Xander Cage", "2017-01-19", "D. J. Caruso", "Vin Diesel");
COMMIT;

# Inserir Dados na Tabela 'Plataformas'
INSERT INTO plataformas (nome_plataforma) VALUES ("Amazon Prime Video");
COMMIT;

# Inserir Dados na Tabela 'Comentários'
INSERT INTO comentarios (comentario) VALUES ("Xander Cage desiste de sua aposentadoria quando Xiang, um guerreiro alfa mortal, coloca suas mãos em uma arma indestrutível chamada de "Caixa de Pandora". Xander recruta os melhores soldados do mundo para destruir o vilão e paralelamente tem que enfrentar uma resistência formada por governos corruptos de todo o mundo.");

# Selecionar os Dados das Tabelas
SELECT *
FROM usuarios;

SELECT *
FROM filmes;

SELECT *
FROM plataformas;

SELECT *
FROM comentarios;