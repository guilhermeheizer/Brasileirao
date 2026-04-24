import httpx
import ssl, certifi

url = "https://www.cbf.com.br/futebol-brasileiro/tabelas/campeonato-brasileiro/serie-a/2026"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
}

r = httpx.Client(http2=True, verify=certifi.where(), headers=headers)
response = r.get(url)
print(response.status_code)
print(response.text)