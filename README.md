
# Projeto Brasileirão Séries A e B

### Índice
1. Como surgiu a ídeia
2. Como foi o processo de criação dos prompts
3. Como é a estrutura do projeto
4. Como baixar, instalar o projeto e executar
5. Como executar os endpoints do Brasileirão

## 1. Como surgiu a ídeia

A empresa Hashtag disponibiliza no YouTube um curso de Python com o framework FasAPI – Rest API https://www.youtube.com/playlist?list=PLpdAy0tYrnKy3TvpCT-x7kGqMQ5grk1Xq 

A partir deste curso idealizei o projeto backend em Python do Brasileirão, com base nos sites:
- Globo Esporte: https://ge.globo.com/futebol/brasileirao-serie-a/
- CBF: https://www.cbf.com.br/futebol-brasileiro/tabelas/campeonato-brasileiro/serie-a/2026

Para a construção do projeto Brasileirão decidi que a IA faria a geração dos códigos Python, ou seja a IA foi o **"programador"**, utilizado o editor VSCode, configurado para acessar o Copilot e o ChatGPT (do site da Adapta). 

O objetivo é gerar a classificação do campeonato Brasileiro das séries A e B a partir dos jogos finalizados das rodadas do campeonato Brasileiro.

**É importante salientar que este projeto foi um estudo de como utilizar a IA para geração de código Python.**

## 2. Como foi o processo de criação dos prompts

A minha abordagem inicial para a criação dos models das tabelas foi a partir dos comandos SQL para criação das tabelas no banco SQLite e o exemplo do model em Python foi da tabela de usuário do curso que fiz da Hashtag. Segue a descrição do prompt.

**Então o 1º prompt com a IA GPT4o** formatei da seguinte maneira:  
O projeto Python back-end será construido com FastApi e SQLAlchemy.
Criei através do MySql Workbench o EER Diagram e a partir dele exportei para uma query que contém os comandos de criação do banco “brasileirao”.

Segue os comandos:
Neste ponto colei os comandos de criação das tabelas do banco brasileirao, gerado pelo MySql Workbench.

Vamos utilizar o SQLite para a criação do brasileirao.db, para isto usar o Alembic para criar as migrations.

Para cada tabela, criar um arquivo <nome_tabela>_models.py.
Colei o exemplo do model de usuário do curso da Hashtag.

Criar os arquivos Python para as tabelas a seguir, acrescentar para cada tabela "def int ( … ):
cartao, cidade, classificacao_geral, classificacao_rodada, clube, estádio, rodada e usuário.

**A resposta ao meu prompt**, foi a criação dos models, para cada uma das tabelas gerou:
Arquivo: cartão_models.py e as linhas de código os atributos, indicando o tipo (se int, str, date, ...), nullable ou não, a chave primária, chave estrangeira e o init da tabela.

**Fiz o 2º prompt**, com a seguinte pergunta:
Como fica as pastas dos arquivos .py?

**A resposta ao meu prompt foi**:
Nesta situação, ao organizar um projeto Python backend com FastAPI e SQLAlchemy, é importante criar uma estrutura de pastas bem organizada para facilitar a manutenção e o entendimento do sistema. Abaixo, proponho uma estrutura de diretórios e arquivos para incluir os modelos que você mencionou, bem como organizar o projeto como um todo.
A IA retornou todas as estruturas de pasta e a explicação de cada uma, o que deverá conter nas mesmas.

Acatei a sugestão da IA GPT4o dos models e a da estrutura de pastas e nomes dos arquivos .py, e com o VSCode criei o projeto braseileirao, com base com projeto de FastAPI da Hashtag.

Neste ponto é fundamental o **olhar do analista de sistemas / desenvolvedor**, pois realizei vários ajustes na proposta do GPT4o, tanto nos models quanto na estrutura de pastas. Mas vale destacar que o total linhas de códigos dos models é de *390 linhas geradas* a partir de um prompt do GPT4o e sem erros. Agora imagine digitando tudo, com certeza mandaria um bom tempo e ainda realizando várias correções de erros de grafía e erros de compilação.

A estrutura de pastas do Brasileirão é diferente da estrutura do curso de FastAPI da Hashtag e o GPT4o ajudou muito nos ajustes, mas o GPT4o sugeriu muitas soluções que simplesmente não funcionaram, para buscar as correções acessei o Stack Overflow, documentação oficial do Python, assisti vídeos no YouTube, até que o primeiro endpoint para listar as cidades funcionou. **Tudo que o GPT4o propõem é importante questionar, validar e se a solução proposta atende**. 

Resumi algumas boas práticas na preparação de prompt, sugere que prompt tenha:
- **Definição do Contexto**: Descrever o cenário e o esperado do modelo.
- **Objetivo ou Instruções Principais**: Declarar a tarefa que o modelo deve realizar.
- **Detalhes ou Requisitos Técnicos**: Listar os detalhes técnicos, como um exemplo código para seguir.
- **Exemplos de códigos**
- **Especificação do Formato de Saída**: Como será a saída da funcionalidade.
- **Restrições e Limitações**: O que não deve ser feito ou as condições específicas.
- **Sempre repita o que deseja e não simplifique**: Exemplo: Quero que grave a tabela de cidade obtendo os dados da entrada do endpoint, depois faça o insert *“na mesma”*. Não coloque *“na mesma”*, pois estamos *“conversando”* com IA, substitua *“na mesma”* por *“na tabela de cidade”*.

O VSCode com o Copilot trás uma velocidade durante a digitação do código, porque vai sugerindo as novas linhas de código, achei fantástico este recurso. Também é muito eficaz na correção dos erros de compilação. Outra inteligência do Copilot é gerar um código a partir do comentário no programa, por exemplo, se já estiver pronto a função para a inclusão e consistência de uma tabela, quando no comentário da próxima função você descrever que a função será de alteração, o Copilot gera todo o código da função. Neste ponto o **“olhar do analista de sistemas / desenvolvedor”** tem que avaliar se o código gerado atende os propósitos do que deseja, se está de acordo com as boas práticas de Designer Patterns.

Uma das tarefas do **analista de sistemas / desenvolvedor** que sempre pratiquei quando outro profissional executaria a codificação do programa, é descrever a **“definição do programa”**, contém os requisitos de como o programa deve funcionar. Com o GPT4o segui a mesma linha de raciocínio, pois o **GPT4o é o meu “programador”**.

Uma boa definição de um programa, deve conter:
- Objetivo do programa bem claros e sucintos
- Explicação quais são os parâmetros de entrada, as tabelas a serem idas, as tabelas que terão inclusão ou alteração ou exclusão, se teremos um relatório ou um json ou arquivo texto como resultado do processamento.
- Detalhamento de como o programa vai funcionar, quais tabelas serão lidas para obter parâmetros que serão utilizados na lógica principal. Qual é a tabela principal a ser lida, se fará loop até o fim ou outra condição de termino do loop. Quais as leituras secundárias. Explicar como proceder nas exceções e explicar as regras do processo.
- Se tiver tela, obrigatoriamente tem que ter o desenho da tela e a explicação de como funciona a tela, as consistências de cada campo da tela, e para cada clique indicar quais endpoints a serem chamados ou uma tela de popup.
- Se tiver relatório, arquivo de sáida, xml ou json, é importante ter um “desenho ou exemplo” e explicar de onde vem cada campo do relatório, quebras e totalização. 

Exemplificando, na função do Brasileirão para calcular a classificação geral do campeonato, construir a definição da seguinte forma. Observe que inseri *“---”* para destacar que termina uma explicação e começa outra e colocando linhas em branco após os 3 traços, isto é muito importante para separar os assuntos.

No projeto Brasileirao em Python com FastApi e SQLAchemic. Tenho:

\---

rodada_models.py: (inclui o código)

\---

cartao_models.py: (inclui o código)

\---

Classificação_geral_models.py: (inclui o código Python de exemplo)

\---

Criar uma função para calcular a classificação do Brasileirao a partir da tabela rodada e inserir ou update na tabela classificacao_geral. 

Parametro de entrada: serie, ano, rodada e carrega jogos nao realizados de rodadas anteriores (true = carrega e false = não carrega).

Ler a tabela de rodada de acordo com os parametros acima.

Considerar somente os registros que possuem os atributos rod_partida_finalizada = "S" e rod_calculou_classificacao = "N"  
Para cada registro lido da tabela rodada, considerar o seguinte:  
Temos para o "clube_clu_sigla_mandante": rod_gols_mandante, rod_pontos_mandante (que pode ser 0, 1 ou 3 pontos)  
Temos para o "clube_clu_sigla_visitante": rod_gols_visitante, rod_pontos_visitante (que pode ser 0, 1 ou 3 pontos)

Então cada de registro lido da tabela rodada teremos para o time mandante um insert ou update na tabela classificacao_geral e para o time visitante um insert ou update na tabela classificacao_geral.  
Como atualizar os atributos da tabela classificacao_geral, terá dois processamentos um para o time mandante e outro para o time visitante:  
clg_pontos: incrementar - rod_pontos_mandante ou rod_pontos_visitante  
clg_vitorias: incrementar - Se ganhou a partida, ou seja, rod_gols_visitante maior rod_pontos_mandante e depois o mesmo para o time visitante  
clg_saldo_gols: incrementar - rod_gols_visitante menos rod_pontos_mandante e depois o mesmo para o time visitante  
clg_gols_pro: incrementar - rod_gols_visitante e depois o mesmo para o time visitante
clg_confronto_direto: gravar zero  
clg_vermelho_clube_clu_sigla: Ler a tabela cartao para car_qtd_vermelho e atualizar o valor, fazer o mesmo para o time visitante  
clg_amarelo_clube_clu_sigla: Ler a tabela cartao para car_qtd_amarelo e atualizar o valor, fazer o mesmo para o time visitante  
clube_clu_sigla: Pegar da rodada - clube_clu_sigla_mandante e depois o mesmo para o time visitante  
clg_qtd_empates: incrementar - se o placar ou rod_gols_mandante > rod_gols_visitante e depois o mesmo para o time visitante  
clg_qtd_derrotas: incrementar - se o placar ou rod_gols_visitante rod_gols_mandante e depois o mesmo para o time visitante  
clg_qtd_empates: incrementar - se o placar ou rod_gols_mandante = rod_gols_visitante e depois o mesmo para o time visitante  
clg_gols_contra: incrementar - rod_gols_visitante e e depois o mesmo para o time visitante rod_gols_mandante  

Criar a rota que vou inserir form_placar_rodada_routers.py

**A resposta ao meu prompt foi a criação form_placar_rodada_routers.py e form_placar_rodada_service.py**

O resultado foi muito bom, o código gerado foi perfeito e fiz intervenções. A classificação geral ficou correta e de acordo com os sites do Globo Esporte e da CBF.

Para cada código gerado pelo GPT4o é obrigatório realizar os testes unitários, passando por todas as condições do programa (os “if”, as exceções), verificar no banco de dados se a gravação / alteração / exclusão estão corretas, conferir as saídas, verificar o português e a clareza das mensagens.  
*Parece obvio “realizar testes unitários”, mas muitos profissionais não possuem este cuidado.*

Realizados os testes unitários passamos para os testes funcionais, validam o que o sistema faz (funcionalidades, regras de negócio), verificando se cada recurso entrega o resultado esperado, comumente via testes de unidade e aceitação.

Conclusão sobre a geração de código pelo GPT4o e o Copilot.

A experiência de uso combinando GPT4o e Copilot demonstrou que ambos aceleram significativamente o desenvolvimento backend em Python com FastAPI, SQLAlchemy e organização de projetos. A IA ajudou tanto na criação inicial do projeto quanto na refatoração, documentação, geração de modelos e definição de pastas e por fim a minha curva de aprendizagem foi muita eficaz.

## 3. Como é a estrutura do projeto

A estrutura do projeto Brasileirao em Python utilizando o FastApi é:

Brasileirao/  
├─ app/  
│   ├─ _init_.py  
│   ├─ core/  
│   │   ├─ _init_.py  
│   │   ├─ config.py         # Configurações principais, como database, CORS, etc.  
│   │   ├─ database.py       # Configuração e inicialização do banco de dados  
│   │   ├─ dependencies.py   # Dependências para autenticação e acesso ao banco de dados   
│   ├─ models/   
│   │   ├─ cartao_models.py                # Modelo para a tabela de cartao  
│   │   ├─ cidade_models.py                # Modelo para a tabela de cidades  
│   │   ├─ estado_models.py                # Modelo para a tabela de estados  
│   │   ├─ clube_models.py                 # Modelo para a tabela de clubes  
│   │   ├─ rodada_models.py                # Modelo para a tabela de rodadas  
│   │   ├─ classificacao_geral_models.py   # Modelo para a tabela de classificações  
│   │   ├─ classificacao_rodada_models.py  # Modelo para a tabela de rodada  
│   │   ├─ usuario_models.py               # Modelo para a tabela de usuários  
│   ├─ routes/  
│   │   ├─ _init_.py  
│   │   ├─ crud/  
│   │   │   ├─ _init_.py   
│   │   │   ├─ cartao_routes.py     # CRUD de cidade  
│   │   │   ├─ cidade_routes.py     # CRUD de cidade  
│   │   │   ├─ estado_routes.py     # CRUD de estado  
│   │   │   ├─ clube_routes.py      # CRUD de clube  
│   │   │   ├─ rodada_routes.py     # CRUD de rodada  
│   │   │   ├─ usuario_routes.py    # CRUD de usuário  
│   │   ├─ form/  
│   │       ├─ _init_.py  
│   │       ├─ form_cadastra_rodada_routers.py       # Endpoint tela para cadastrar rodada  
│   │       ├─ form_classificacao_rodada_routers.py  # Endpoint copiar classificação geral por rodada  
│   │       ├─ login_routes.py                       # Endpoint específico para tela de login  
│   │       ├─ form_placar_rodada_routes.py          # Endpoint tela calculo da classificacao  
│   ├─ services/  
│   │   ├─ _init_.py  
│   │   ├─ cartao_service.py  # Regras de negócios para cartao  
│   │   ├─ cidade_service.py  # Regras de negócios para cidade  
│   │   ├─ estado_service.py  # Regras de negócios para estado  
│   │   ├─ clube_service.py   # Regras de negócios para clube  
│   │   ├─ rodada_service.py  # Regras de negócios para rodada  
│   │   ├─ usuario_service.py # Regras de negócios para usuário  
│   │   ├─ login_service.py   # Regras de negócios para login  
│   │   ├─ form/  
│   │       ├─ _init_.py  
│   │       ├─ form_cadastra_rodada_service.py       # Regra negócio cadastrar rodada  
│   │       ├─ form_classificacao_rodada_service.py  # Regra negócio classificação geral por rodada  
│   │       ├─ form_placar_rodada_service.py         # Regra negócio calculo da classificacao  
│   ├─ schema/  
│   │   ├─ _init_.py  
│   │   ├─ cartao_schema.py         
│   │   ├─ cidade_schema.py       
│   │   ├─ classificacao_geral_schema.py  
│   │   ├─ classificacao_rodada_schema.py   
│   │   ├─ estadio_schema.py         
│   │   ├─ clube_schema.py    
│   │   ├─ from_login_schema.py      
│   │   ├─ rodada_schema.py         
│   │   ├─ classificacao_schema.py  
│   │   ├─ usuario_schema.py        
│   ├─ utils/  
│   │   ├─ _init_.py  
│   │   ├─ token.py          # Lógica para geração/validação de tokens JWT  
├─ teste_rotas/  
│   ├─ lista_classificacao_geral.py        # Testes relacionados a cidade  
├─ .env                      # Variáveis de ambiente (ex. DATABASE_URL)  
├─ .gitignore                # Arquivos ignorados pelo controle de versão  
├─ main.py                   # Arquivo principal para executar o servidor  
├─ brasileirao.db            # Banco de dados SQLite  
├─ requirements.txt          # Dependências do projeto  
└─ README.md                 # Documentação do projeto  

**EER do Brasileirão**

![Tabelas do Brasileirão.](/imagens_readme/eer.png "Brasileirão")

## 4. Como baixar, instalar o projeto e executar

Acesse o repositório do GitHub https://github.com/guilhermeheizer/Brasileirao e faça um **Fork**.  

Após realizado o fork e como o projeto no computador, configue o ambiente virtual. Siga os passos:   
* Verificar se o Python está instalado  
    No PowerShell ou Prompt de Comando, execute: python --version  
    Se aparecer a versão, está tudo OK
* Criar o ambiente virtual  
    No termial do VSCode, vá até a pasta do Brasileirão:  
    cd <caminho_do_projeto>
    Digite: python -m venv venv  
    Este comando cria uma pasta venv dentro do projeto  
* Ativar o ambiente virtual. No terminal:venv\Scripts\activateAo ativar, o terminal vai mostrar algo assim:(venv) C:\seuprojeto>
* Configurar o VSCode para usar o venv automaticamenteNo VSCode:
Pressione Ctrl + Shift + P
Digite: Python: Select Interpreter
Selecione o interpretador dentro da venv:
.\venv\Scripts\python.exe  
Agora o VSCode usará esse ambiente virtual para rodar o projeto.
* Instalar dependências dentro do venv. Tudo que instalar, agora irá somente para o ambiente virtual:  
pip install fastapi  
pip install uvicorn  
pip install sqlalchemy  
* Para desativar o venvBasta executar:deactivate
* Rodar seu projeto com o venv ativoExemplo:uvicorn main:app --reload

Toda vez que abrir o projeto Brasileirão no VSCode executar os dois passos:  
- No terminal, ativar o ambiente virtual digitando: **venv\Scripts\activate**  
- Selecione o interpretador pressionando **Ctrl + Shift + P**, escolha o interpretador associado ao seu ambiente virtual (geralmente terá o caminho do seu projeto seguido de venv).  

Um ponto importante é o **requirements.txt**, contém todas as dependências do projeto Python — especialmente importante em projetos FastAPI, SQLAlchemy dentre outras bibliotecas.  Garante que qualquer pessoa (ou servidor) consiga instalar exatamente as mesmas versões usadas por você, evitando erros de incompatibilidade.   
O comando **pip freeze > requirements.txt**  gera a lista completa dos pacotes instalados.  
Após baixar o projeto Brasileirão execute o comando:  
**pip install -r requirements.txt** irá instalar as bibliotecas.



## 5. Como executar os endpoints do Brasileirão

No terminal digite **uvicorn main:app --reload** para carregar o sistema.    

INFO:     Will watch for changes in these directories: ['D:\\PythonMeusProjetos\\Brasileirao']  
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)  
INFO:     Started reloader process [10568] using StatReload  
INFO:     Started server process [5808]  
INFO:     Waiting for application startup.  
INFO:     Application startup complete.  

Clicando no link http://127.0.0.1:8000 irá carregar no navegador uma página, veja abaixo.  

![Swagger](/imagens_readme/swagger_01.png)  

No navegador http://127.0.0.1:8000/docs irá carregar os endpoints do Brasileirão

![Swagger](/imagens_readme/swagger_02.png)

Segue os passos para execução dos endpoints.

### Observação importante para o Frontend
No frontend após o login do usuário deve-se selecionar a série e o ano para repassar para os demais formulários.  
Este projeto aborda as séries A e B do Brasileirão, para o ano de 2026 em diante. As tabelas rodada, cartao, classificacao_geral e classificacao_rodada a série e o ano são parte da chave primária (PK) e a tabela clube possui a série dentre os atributos afim melhorar algumas queries.  

**É importante salientar que este projeto foi um estudo de como utilizar a IA para geração de código Python.**  


### **Passo 01**: Usuário
Caso não tenha usuário de login cadastrado, acessar a **tag usuario**  
![Swagger - usuario](/imagens_readme/swagger_usuario.png)

Em seguida, faça a inclusão de um usuário:
![Swagger - usuario/incluir](/imagens_readme/swagger_usuario_incluir.png)
Os usuários cadastrados são armazenados na tabela usuario.  
As rotas para alterar, exclui, listar, alterar senha, esqueci minha senha dentre outras serão desenvolvidas posteriormente.
### **Passo 02**: Login
Todas as vezes que carregar a API do Brasileirão é necessário executar o login e realizar autenticação.
![Swagger - login/login](/imagens_readme/swagger_login.png)
![Swagger - login/login execute](/imagens_readme/swagger_login_login_01.png)
![Swagger - login/login response](/imagens_readme/swagger_login_login_02.png)
![Swagger - login/form execute](/imagens_readme/swagger_login_form_01.png)
![Swagger - login/form response](/imagens_readme/swagger_login_form_02.png)
![Swagger - Authenticator botton](/imagens_readme/swagger_autorizacao_01.png)
![Swagger - Authenticator execute](/imagens_readme/swagger_autorizacao_02.png)
![Swagger - Authenticator response](/imagens_readme/swagger_autorizacao_03.png)
![Swagger - login/refresh](/imagens_readme/swagger_refresh.png)
### **Passo 03**: Cidade
Os endpoints de cidade são os primeiros a serem executados quando inicia-se o Brasileirão, porque o código da cidade é chave estrangeira das tabelas de clube e estádio.
![Swagger - cidade](/imagens_readme/swagger_cidade.png)
![Swagger - cidade](/imagens_readme/swagger_cidade_listar.png)
![Swagger - cidade](/imagens_readme/swagger_cidade_incluir.png)
![Swagger - cidade](/imagens_readme/swagger_cidade_alterar.png)
![Swagger - cidade](/imagens_readme/swagger_cidade_deletar.png)
![Swagger - cidade execute](/imagens_readme/swagger_cidade_listar_paginado_01.png)
![Swagger - cidade response](/imagens_readme/swagger_cidade_listar_paginado_01.png)
### **Passo 04**: Clube 
O endpoint para incluir clube solicita sigla, nome, série, link do escudo e o código da cidade do clube, tais informações considere obte-las do site "Globo Esporte" ou outro site que posso obter o link.  
O escudo do Cruzeiro no G1: https://s.sde.globo.com/media/organizations/2021/02/13/cruzeiro_2021.svg
![Swagger - clube](/imagens_readme/swagger_clube.png)
![Swagger - clube](/imagens_readme/swagger_clube_listar.png)
![Swagger - clube](/imagens_readme/swagger_clube_incluir.png)
![Swagger - clube](/imagens_readme/swagger_clube_alterar.png)
![Swagger - clube](/imagens_readme/swagger_clube_deletar.png)
![Swagger - clube](/imagens_readme/swagger_clube_listar_paginado.png)
### **Passoo 5**: Estádio
Executar o endpoint para incluir os estádios onde os jogos aconteceram, mas antes de cadastrar os jogos das primeiras rodadas. Acessar o site do Globo Esporte para consultar as rodadas, para cada jogo anote o nome do estádio e consulte qual é a cidade do estádio.  
![Swagger - estadio](/imagens_readme/swagger_estadio.png)
![Swagger - estadio](/imagens_readme/swagger_estadio_listar.png)
![Swagger - estadio](/imagens_readme/swagger_estadio_incluir.png)
![Swagger - estadio](/imagens_readme/swagger_estadio_alterar.png)
![Swagger - estadio](/imagens_readme/swagger_estadio_deletar.png)
![Swagger - estadio](/imagens_readme/swagger_estadio_listar_paginado.png)
### **Passo 06**: Cartão
**Restrição do projeto**: A quantidade de cartões armazenada é por série / ano / clube, ou seja, um clube terá o total de cartões por campeonato e tais quantidades fazem parte dos critérios de desempate quando dois ou mais clubles possuem pontuações iguais. Não optei de gravar a quantidade por jogo, porque esta informação se encontra somente no documento do jogo no site da CBF e ficaria inviável abrir jogo por jogo, acessar o documento do jogo e visualmente contar a quantidade de amarelos e vermelhos.

Os endpoints desta tag são para realizar manutenção nas quantidades de cartões amarelos e vermelhos dos clubes das séries A ou B do ano do campeonato.  
O endpoint "**criar_cartoes**" é acionado após cadastrar os clubes da série A ou B, com objetivo de criar na tabela cartao todos os registros dos clubles que estão cadastrados na tabela clube.  

O endpoint "**dados_cbf**" atualiza automaticamente a partir do site da CBF a quantidade de amarelos e vermelhos de cada clube da série/ano informados no parametro. É importante resaltar que a CBF atualiza a quantidade de cartões somente um dia após finalizados os jogos.  
**Hard code no processo de busca dos cartões ns CBF:** Utilizo a biblioteca **BeautifulSoup** para acessar o site da CBF, esta biblioteca não carrega o site no Google Chrome, ou seja, abre em background. Procuro no site pelos nomes dos clubes (hard code) e um de-para para a sigla do clube de acordo com a sigla do time no Globe Esporte e obtem os cartões amarelos e vermelhos. Então, no Globo Esporte é "Vasco" e na CBF é "Vasco da Gama Saf", então a cada novo ano de campeonato é necessário ajustar o programa Python. Uma solução para não ter hard code seria criar um atributo na tabela clube para armazenar o nome clube do site da CBF.
![Swagger - cartao](/imagens_readme/swagger_cartao.png)
![Swagger - cartao](/imagens_readme/swagger_cartao_listar.png)
![Swagger - cartao](/imagens_readme/swagger_cartao_incluir.png)
![Swagger - cartao](/imagens_readme/swagger_cartao_criar_cartoes.png)
![Swagger - cartao](/imagens_readme/swagger_cartao_atualizar.png)
![Swagger - cartao](/imagens_readme/swagger_cartao_dados_cbf.png)
![Swagger - cartao](/imagens_readme/swagger_cartao_deletar.png)
![Swagger - cartao](/imagens_readme/swagger_cartao_listar_paginado.png)
### **Passo 07**: Cadastra Rodada
Os endpoints da **tag cadastra rodada** serão chamados pela tela form_manut_rodada
![Swagger - cadastra rodada](/imagens_readme/swagger_cadastra_rodada_form_manut_rodada_criar_rodada.png)
![Swagger - cadastra rodada](/imagens_readme/swagger_cadastra_rodada_form_manut_rodada_pesquisar_clubes.png)
![Swagger - cadastra rodada](/imagens_readme/swagger_cadastra_rodada_form_manut_rodada_pesquisar_estadios.png)
### **Passo 08**: Placar Rodada
Os endpoints da **tag placar rodada** serão chamados pela tela form_classificacao_rodada.  
Quando inicia a rodada e os jogos do dia são finalizados, executa-se o endpoint que faz a atualização dos placares dos jogos.  
Após todos placares atualizados, acessar a **tag cartao** para atualizar os cartões amarelos e vermelhos de cada clube. Tais informações constam no site da CBF, e os cartões são atualizados somente um dia após o termino dos jogos.  
Depois de atualizar os cartões, executar o endpoint "classificacao", este endpoint possui os parametros: série, ano, rodada e carrega jogos nao realizados (informando "true", o processo irá procurar nas rodadas anteriores, os jogos finalizados e que não tiveram a classificacao calculada ou seja vai atualizar os jogos que foram prorrogados).
![Swagger - placar rodada](/imagens_readme/swagger_placar_rodada.png)
![Swagger - placar rodada](/imagens_readme/swagger_placar_rodada_buscar_placares.png)
![Swagger - placar rodada](/imagens_readme/swagger_placar_rodada_atualizar_placares.png)
![Swagger - placar rodada](/imagens_readme/swagger_placar_rodada_listar_paginado.png)
![Swagger - placar rodada](/imagens_readme/swagger_placar_rodada_classificacao.png)
![Swagger - placar rodada](/imagens_readme/swagger_placar_rodada_classificacao_geral.png)
### **Passo 09**: Copiar Classificação por Rodada
Nesta tag tem o endpoint para copiar a classificação geral com objetivo de salvar a classificação de cada rodada, para em novas implementações mostrar estatísticas dos time em qual posição estava na rodada 01 até a 38.  
Outra opção é reclacular a classficação geral, a partir da última rodada. Vai recorrer a este endpoint quando em algum momento a classficação foi calculada com um placar errado ou esqueceu de buscar os cartões no site da CBF.
![Swagger - placar rodada](/imagens_readme/swagger_copiar_classificacao.png)
![Swagger - placar rodada](/imagens_readme/swagger_copiar_classificacao_copiar.png)
![Swagger - placar rodada](/imagens_readme/swagger_copiar_classificacao_recalcular.png)
```
O projeto esta disponível no github: https://github.com/guilhermeheizer/Brasileirao
```

## Agradecimentos
Contribuíram com meu projeto e agradeço pela ajuda:

- João Paulo Rodrigues de Lira - Sócio e Professor da Hashtag Treinamentos. Fiz o curso de Python do framework FastApi disponível no YouTube: https://www.youtube.com/playlist?list=PLpdAy0tYrnKy3TvpCT-x7kGqMQ5grk1Xq
## Autor
- [@guilhermeheizer](https://www.github.com/guilhermeheizer)
- [@LinkedIn](www.linkedin.com/in/guilhermeheizernogueira/)