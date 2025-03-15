import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def carregar_dados(csv_file):
    """Carrega o CSV e prepara os dados."""
    df = pd.read_csv(csv_file, sep=',')  # Usar vírgula como separador
    df.columns = df.columns.str.strip()  # Remover espaços extras
    
    # Verificar se as colunas necessárias existem
    colunas_necessarias = ['TAMANHO DO MUNICÍPIO', 'DS_COMPOSICAO_COLIGACAO', 'DS_COR_RACA', 'NR_IDADE_DATA_POSSE']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f"A coluna '{coluna}' não foi encontrada no CSV.")
    
    return df

def contar_tamanhos(df):
    """Conta quantos municípios há em cada categoria."""
    return df['TAMANHO DO MUNICÍPIO'].value_counts()

def filtrar_por_tamanho(df, tamanho):
    """Filtra os municípios pelo tamanho especificado."""
    return df[df['TAMANHO DO MUNICÍPIO'] == tamanho]

def obter_top_coligacoes(df, top_n=10):
    """Retorna os top N coligações."""
    return df['DS_COMPOSICAO_COLIGACAO'].value_counts().head(top_n)

def contar_raca(df):
    """Conta a distribuição de raça no conjunto de dados."""
    return df['DS_COR_RACA'].value_counts()

def contar_idades(df):
    """Conta a distribuição de idades no conjunto de dados."""
    return df['NR_IDADE_DATA_POSSE'].value_counts().sort_index()

def salvar_csv(dados, nome_arquivo):
    """Salva os dados em um arquivo CSV."""
    dados.to_csv(nome_arquivo, index=True)

def gerar_grafico_barras(dados, titulo, nome_arquivo):
    """Gera um gráfico de barras a partir de uma contagem."""
    plt.figure(figsize=(10, 6))
    dados.plot(kind='bar', color='royalblue')
    plt.title(titulo)
    plt.xlabel("Categorias")
    plt.ylabel("Quantidade")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(nome_arquivo)
    plt.close()

def gerar_histograma_idades(dados, titulo, nome_arquivo):
    """Gera um histograma para distribuição de idades."""
    plt.figure(figsize=(10, 6))
    sns.histplot(dados.index.repeat(dados.values), bins=15, kde=True, color='purple')
    plt.title(titulo)
    plt.xlabel("Idade")
    plt.ylabel("Frequência")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(nome_arquivo)
    plt.close()

def main():
    csv_file = "vereadoras.csv"  # Nome correto do arquivo
    df = carregar_dados(csv_file)
    
    # Separação dos conjuntos
    df_pequeno = filtrar_por_tamanho(df, 'PEQUENO')
    df_medio = filtrar_por_tamanho(df, 'MÉDIO')
    df_grande = filtrar_por_tamanho(df, 'GRANDE')
    
    # Contagem de raça
    contagem_raca_total = contar_raca(df)
    gerar_grafico_barras(contagem_raca_total, "Distribuição de Raça - Total", "grafico_raca_total.png")
    gerar_grafico_barras(contar_raca(df_pequeno), "Distribuição de Raça - Pequeno", "grafico_raca_pequeno.png")
    gerar_grafico_barras(contar_raca(df_medio), "Distribuição de Raça - Médio", "grafico_raca_medio.png")
    gerar_grafico_barras(contar_raca(df_grande), "Distribuição de Raça - Grande", "grafico_raca_grande.png")
    
    # Contagem de idades
    contagem_idades_total = contar_idades(df)
    gerar_histograma_idades(contagem_idades_total, "Distribuição de Idades - Total", "grafico_idades_total.png")
    gerar_histograma_idades(contar_idades(df_pequeno), "Distribuição de Idades - Pequeno", "grafico_idades_pequeno.png")
    gerar_histograma_idades(contar_idades(df_medio), "Distribuição de Idades - Médio", "grafico_idades_medio.png")
    gerar_histograma_idades(contar_idades(df_grande), "Distribuição de Idades - Grande", "grafico_idades_grande.png")
    
    # Top 10 coligações por categoria
    gerar_grafico_barras(obter_top_coligacoes(df), "Top 10 Coligações - Total", "grafico_coligacoes_total.png")
    gerar_grafico_barras(obter_top_coligacoes(df_pequeno), "Top 10 Coligações - Pequeno", "grafico_coligacoes_pequeno.png")
    gerar_grafico_barras(obter_top_coligacoes(df_medio), "Top 10 Coligações - Médio", "grafico_coligacoes_medio.png")
    gerar_grafico_barras(obter_top_coligacoes(df_grande), "Top 10 Coligações - Grande", "grafico_coligacoes_grande.png")

if __name__ == "__main__":
    main()
