import pandas as pd
import re

# Carregar os dados
df = pd.read_excel('computadores.xlsx')

# Exibir as primeiras linhas do DataFrame para inspeção
print("Primeiras linhas do DataFrame:")
print(df.head())

# Verificar dados faltantes
print("\nVerificando dados faltantes:")
print(df.isnull().sum())  # Mostra a quantidade de dados faltantes por coluna

# Limpar a coluna 'marca' removendo números, espaços extras e aplicando title case
df['marca'] = df['marca'].replace(r'\d+', '', regex=True).str.strip().str.title()

# Exibir as primeiras linhas após a limpeza da coluna 'marca'
print("\nPrimeiras linhas após limpeza da coluna 'marca':")
print(df.head())

# Adicionar uma coluna para verificar se o nome da marca contém a palavra 'RAM'
df['possui_RAM'] = df['marca'].str.contains('RAM', case=False, na=False)

# Adicionar uma coluna para extrair a quantidade de RAM
df['quantidade_RAM'] = df['marca'].str.extract(r'(\d+)\s*GB\s*RAM', flags=re.IGNORECASE)

# Substituir valores NaN na coluna 'quantidade_RAM' por "Não possui"
df['quantidade_RAM'] = df['quantidade_RAM'].fillna('Não possui')

# Adicionar uma coluna para classificar as cores dos computadores
cores = [
    "amarelo", "amarela", "azul", "branco", "branca", "cinza", "creme", "dourado", "laranja", "marrom", "preto", 
    "rosa", "roxo", "verde", "vermelho", "bege", "graphite", "geada", "uva", "grey", "yellow", "blue", "silver",
    "red", "black", "off white", "white", "green", "purple", "orange", "pink", "fuchsia", "orchid", "aqua", "azure",
    "beige", "darkred", "coral"
]

def extrair_cor(texto):
    texto = str(texto).lower()
    for cor in cores:
        if cor in texto:
            return cor
    return "Desconhecida"

df['cor_principal'] = df['marca'].apply(extrair_cor)

# Exibir as primeiras linhas com as novas colunas
print("\nPrimeiras linhas com análise adicional (RAM e cor principal):")
print(df.head())

# Salvar o DataFrame tratado em um arquivo Excel
df.to_excel('computadores_analise.xlsx', index=False)

print("\nArquivo 'computadores_analise.xlsx' foi salvo com sucesso!")
