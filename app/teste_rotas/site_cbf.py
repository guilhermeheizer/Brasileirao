import requests
from bs4 import BeautifulSoup


class extrair_cartoes_amarelo_vermelho:
    def __init__(self, serie, ano):
        self.serie = serie.lower()
        self.ano = ano
        self.url = self.get_url()
    
    def get_url(self):
        """Retorna a URL correspondente à série."""
        if self.serie == "a":
            return f"https://www.cbf.com.br/futebol-brasileiro/tabelas/campeonato-brasileiro/serie-a/{self.ano}"
        elif self.serie == "b":
            return f"https://www.cbf.com.br/futebol-brasileiro/tabelas/campeonato-brasileiro/serie-b/{self.ano}"
        else:
            raise ValueError("Série inválida. Use 'A' ou 'B' para a série.")
    
    def executar(self):
        """Executa o scraping para coletar os cartões amarelos e vermelhos."""
        # Faz a requisição e obtém o conteúdo HTML
        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Falha ao acessar a página {self.url}.")
        
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Busca o corpo da tabela
        section = soup.find("section", class_="styles_container__L5dGB")
        if not section:
            raise Exception("Seção da tabela não encontrada no site.")
        tbody = section.find("tbody")

        if not tbody:
            raise Exception("Tabela não encontrada no site.")

        # Lista para armazenar os resultados
        resultados = []

        # Loop pelos <tr> (linhas da tabela)
        for tr in tbody.find_all("tr"):
            try:
                # Extrai o nome do clube (no <td class="styles_teamPosition__CFIvz"> com <strong>)
                # Extrai o nome do clube (na segunda tag <strong>)
                td_nome_clube = tr.find("td", class_="styles_teamPosition__CFIvz")
                if td_nome_clube:
                    nome_clube = td_nome_clube.find_all("strong")[1].text.strip()
                else:
                    raise Exception("Nome do clube não encontrado.")

                # Extrai o número de cartões amarelos (10ª <td>, índice 9)
                td_cartoes_amarelos = tr.find_all("td")[9]  # 9º índice → 10º <td>
                cartoes_amarelos = int(td_cartoes_amarelos.text.strip())

                # Extrai o número de cartões vermelhos (11ª <td>, índice 10)
                td_cartoes_vermelhos = tr.find_all("td")[10]  # 10º índice → 11º <td>
                cartoes_vermelhos = int(td_cartoes_vermelhos.text.strip())

                # Adiciona ao resultado
                resultados.append({
                    "clube": nome_clube,
                    "cartoes_amarelos": cartoes_amarelos,
                    "cartoes_vermelhos": cartoes_vermelhos
                })
            except Exception as e:
                print(f"Erro ao processar uma linha: {e}")
                continue

        # Dicionário de correspondência entre clubes e siglas
        clubes_para_siglas = {
            "Palmeiras": "PAL",
            "São Paulo": "SAO",
            "Fluminense": "FLU",
            "Bahia": "BAH",
            "Athletico Paranaense": "CAP",
            "Red Bull Bragantino": "RBB",
            "Chapecoense": "CHA",
            "Mirassol": "MIR",
            "Coritiba S.a.f.": "CFC",
            "Flamengo": "FLA",
            "Botafogo": "BOT",
            "Corinthians": "COR",
            "Grêmio": "GRE",
            "Vitória": "VIT",
            "Atlético Mineiro": "CAM",
            "Remo": "REM",
            "Vasco da Gama Saf": "VAS",
            "Santos Fc": "SAN",
            "Internacional": "INT",
            "Cruzeiro": "CRU"
        }

        # Nova lista com siglas no lugar dos nomes dos clubes
        nova_lista = []

        for item in resultados:
            nome_clube = item["clube"]
            # Procura a sigla correspondente no dicionário
            sigla = clubes_para_siglas.get(nome_clube, "N/A")  # "N/A" se o clube não estiver no dicionário

            # Adiciona o novo dicionário com as siglas à nova lista
            nova_lista.append({
                "clube": sigla,
                "cartoes_amarelos": item["cartoes_amarelos"],
                "cartoes_vermelhos": item["cartoes_vermelhos"]
            })

        # Exibe a nova lista
        for itens_nova_lista in nova_lista:
            print(itens_nova_lista)
            
        return nova_lista


# Exemplo de uso
if __name__ == "__main__":
    # Exemplo para série A de 2026
    serie = "A"
    ano = 2026

    # Instanciar a classe e executar
    extrator = extrair_cartoes_amarelo_vermelho(serie, ano)
    resultados = extrator.executar()

    # Exibir os resultados
    for resultado in resultados:
        print(f"Clube: {resultado['clube']}, Cartões Amarelos: {resultado['cartoes_amarelos']}, Cartões Vermelhos: {resultado['cartoes_vermelhos']}")