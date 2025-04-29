import pandas as pd
import re

# Carregar o arquivo
df = pd.read_excel("computadores.xlsx")

# Lista de cores para extrair
cores = [
    "amarelo", "amarela", "azul", "branco", "branca", "cinza", "creme", "dourado", "laranja", "marrom", "preto", 
    "rosa","roxo", "verde", "vermelho", "bege","graphite", "geada", "uva", "grey", "yellow", "blue", "silver",
    "red", "black","off white","white", "green", "purple","orange", "pink","fuchsia", "orchid","aqua","azure",
    "beige","darkred","coral"
]

# Função para extrair cor
def extrair_cor(texto):
    texto = str(texto).lower()
    for cor in cores:
        if cor in texto:
            return cor
    return "Desconhecida"

# Aplicar a função na coluna 'marca'
df["cor_principal"] = df["marca"].apply(extrair_cor)

# Contar quantas vezes aparece "Desconhecida"
contagem = df['cor_principal'].str.contains('Desconhecida', case=False, na=False).sum()
print(f'A palavra "desconhecida" aparece {contagem} vezes na coluna.')

# Ajustar formatação da coluna
df['cor_principal'] = df['cor_principal'].str.title()

# Criar coluna booleana se tem "RAM"
df['possui_RAM'] = df['marca'].str.contains('RAM', case=False, na=False)

# Extrair quantidade de RAM com regex
df['quantidade_RAM'] = df['marca'].str.extract(r'(\d+)\s*GB\s*RAM', flags=re.IGNORECASE)

# Preencher os vazios com "Não possui"
df['quantidade_RAM'] = df['quantidade_RAM'].fillna('Não possui')

# Salvar o DataFrame em Excel
df.to_excel('computadores_tratados.xlsx', index=False)

print("Arquivo 'computadores_tratados.xlsx' salvo com sucesso!")
