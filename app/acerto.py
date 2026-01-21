# Lista com as siglas e os nomes dos times
times = [
    ("GOI", "Goiás", "Goiânia", "GO"),
    ("AMA", "Amazonas", "Manaus", "AM"),
    ("PAY", "Paysandu", "Belém", "PA"),
    ("CAP", "Athletico-PR", "Curitiba", "PR"),
    ("CRI", "Criciúma", "Criciúma", "SC"),
    ("OPE", "Operário-PR", "Ponta Grossa", "PR"),
    ("CFC", "Coritiba", "Curitiba", "PR"),
    ("VNO", "Vila Nova", "Goiânia", "GO"),
    ("CRB", "CRB", "Maceió", "AL"),
    ("CHA", "Chapecoense", "Chapecó", "SC"),
    ("AME", "América-MG", "Belo Horizonte", "MG"),
    ("BSP", "Botafogo-SP", "Ribeirão Preto", "SP"),
    ("AFE", "Ferroviária", "Araraquara", "SP"),
    ("REM", "Remo", "Belém", "PA"),
    ("VRE", "Volta Redonda", "Volta Redonda", "RJ"),
    ("CUI", "Cuiabá", "Cuiabá", "MT"),
    ("AVA", "Avaí", "Florianópolis", "SC"),
    ("NOV", "Novorizontino", "Novo Horizonte", "SP"),
    ("ACG", "Atlético-GO", "Goiânia", "GO"),
    ("ATH", "Athletic Club", "São João del-Rei", "MG"),
]

# Ordena a lista alfabeticamente pelo nome da cidade
times_ordenados = sorted(times, key=lambda x: x[2])

# Exibe a lista ordenada
print("Sigla | Time             | Cidade                 | UF")
print("-----------------------------------------------------")
for sigla, time, cidade, uf in times_ordenados:
    print(f"{sigla:<5} | {time:<15} | {cidade:<20} | {uf:<2}")