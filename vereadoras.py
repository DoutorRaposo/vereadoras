import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import sys
import os

def carregar_dados(csv_file):
    """Carrega o CSV e prepara os dados."""
    df = pd.read_csv(csv_file, sep=',')  # Usar vírgula como separador
    df.columns = df.columns.str.strip()  # Remover espaços extras
    
    # Verificar se as colunas necessárias existem
    colunas_necessarias = ['TAMANHO DO MUNICÍPIO', 'DS_COMPOSICAO_COLIGACAO', 'DS_COR_RACA', 'NR_IDADE_DATA_POSSE', 'DS_SIT_TOT_TURNO']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f"A coluna '{coluna}' não foi encontrada no CSV.")
    
    # Filtrar apenas 'ELEITO POR QP' e 'ELEITO POR MÉDIA'
    df = df[df['DS_SIT_TOT_TURNO'].isin(['ELEITO POR QP', 'ELEITO POR MÉDIA'])]
    
    return df

def extrair_nome_parenteses(nome):
    """Se houver parênteses no nome, retorna o conteúdo dentro dos parênteses."""
    match = re.search(r'\((.*?)\)', nome)
    return match.group(1) if match else nome

def filtrar_por_tamanho(df, tamanho):
    """Filtra os municípios pelo tamanho especificado."""
    return df[df['TAMANHO DO MUNICÍPIO'] == tamanho]

def contar_eleitos_por_tipo(df):
    """Calcula a proporção de 'ELEITO POR QP' e 'ELEITO POR MÉDIA' por tamanho de município."""
    tipos_municipios = ['TOTAL', 'PEQUENO', 'MÉDIO', 'GRANDE']
    resultados = []
    
    for tamanho in tipos_municipios:
        if tamanho == 'TOTAL':
            subset = df
        else:
            subset = filtrar_por_tamanho(df, tamanho)
        
        contagem = subset['DS_SIT_TOT_TURNO'].value_counts(normalize=True) * 100
        
        resultados.append({
            'Tamanho': tamanho,
            'ELEITO POR QP': contagem.get('ELEITO POR QP', 0),
            'ELEITO POR MÉDIA': contagem.get('ELEITO POR MÉDIA', 0)
        })
    
    return pd.DataFrame(resultados)

def salvar_csv(dados, nome_arquivo):
    """Salva os dados em um arquivo CSV."""
    nome_caminho = f"out/{nome_arquivo}"
    dados.to_csv(nome_caminho, index=True)

def gerar_grafico_barras_coloridas(df, titulo, nome_arquivo):
    """Gera um gráfico de barras com cores variadas e exibe os valores no topo."""
    plt.figure(figsize=(12, 6))
    colors = sns.color_palette("muted", len(df))
    ax = df.plot(kind='bar', color=colors, legend=False)
    ax.set_ylim(0, max(df) * 1.2) 
    plt.title(titulo)
    plt.ylabel("Quantidade")
    plt.xlabel("Categorias")
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Adicionar valores no topo das barras
    for i, v in enumerate(df):
        if v > 0:  # Evita exibir valores em barras vazias
            ax.text(i, v + (max(df) * 0.02), str(v), ha='center', fontsize=10, color='black')

    # Salvar o gráfico na pasta out/
    nome_caminho = f"out/{nome_arquivo}"
    plt.savefig(nome_caminho, bbox_inches='tight')
    plt.close()

def gerar_histograma_idades(df, titulo, nome_arquivo):
    """Gera um histograma para distribuição de idades."""
    plt.figure(figsize=(10, 6))
    sns.histplot(df['NR_IDADE_DATA_POSSE'].dropna(), bins=15, kde=True, color='#1E90FF')
    plt.title(titulo)
    plt.xlabel("Idade")
    plt.ylabel("Frequência")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    nome_caminho = f"out/{nome_arquivo}"
    plt.savefig(nome_caminho)
    plt.close()

def gerar_grafico_barras_duplas(df, titulo, nome_arquivo):
    """Gera um gráfico de barras lado a lado com porcentagens sobre cada categoria."""
    plt.figure(figsize=(10, 6))  # Aumentando a altura do gráfico para acomodar melhor a legenda
    df.set_index('Tamanho').plot(kind='bar', figsize=(10, 8), color=['blue', 'orange'])
    plt.title(titulo)
    plt.ylabel("Proporção (%)")
    plt.xlabel("Tamanho do Município")
    plt.xticks(rotation=0)
    plt.legend(title="Tipo", loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Adicionar valores no topo das barras
    for i, tamanho in enumerate(df['Tamanho']):
        qp = df.loc[i, 'ELEITO POR QP']
        media = df.loc[i, 'ELEITO POR MÉDIA']
        plt.text(i - 0.15, qp + 1, f'{qp:.1f}%', ha='center', fontsize=10, color='black')
        plt.text(i + 0.15, media + 1, f'{media:.1f}%', ha='center', fontsize=10, color='black')
    
    nome_caminho = f"out/{nome_arquivo}"
    plt.savefig(nome_caminho, bbox_inches='tight')
    plt.close()
    
def main():
    if len(sys.argv) != 2:
        print("Uso: python vereadoras.py <arquivo_csv>")
        sys.exit(1)
    
    os.makedirs("out", exist_ok=True)
    
    csv_file = sys.argv[1]
    df = carregar_dados(csv_file)
    
    # Substituir nomes das coligações pelos nomes dentro dos parênteses quando houver
    df['DS_COMPOSICAO_COLIGACAO'] = df['DS_COMPOSICAO_COLIGACAO'].apply(extrair_nome_parenteses)
    
    tamanhos = ['TOTAL', 'PEQUENO', 'MÉDIO', 'GRANDE']
    
    for tamanho in tamanhos:
        if tamanho == 'TOTAL':
            subset = df
        else:
            subset = filtrar_por_tamanho(df, tamanho)
        
        # Salvar CSVs filtrados
        salvar_csv(subset['DS_COR_RACA'].value_counts(), f"dados_raca_{tamanho.lower()}.csv")
        salvar_csv(subset['DS_COMPOSICAO_COLIGACAO'].value_counts().head(10), f"dados_coligacoes_{tamanho.lower()}.csv")
        salvar_csv(subset['NR_IDADE_DATA_POSSE'].value_counts().sort_index(), f"dados_idades_{tamanho.lower()}.csv")
        
        # Gerar gráficos
        gerar_grafico_barras_coloridas(subset['DS_COR_RACA'].value_counts(), f"Distribuição de raça por municípios {'paranaenses' if tamanho == 'TOTAL' else tamanho.lower() + 's'}", f"grafico_raca_{tamanho.lower()}.png")
        gerar_grafico_barras_coloridas(subset['DS_COMPOSICAO_COLIGACAO'].value_counts().head(10), f"Coligações com maior N de eleitas nos municípios {'paranaenses' if tamanho == 'TOTAL' else tamanho.lower() + 's'}", f"grafico_coligacoes_{tamanho.lower()}.png")
        gerar_histograma_idades(subset, f"Distribuição de idade por município {'paranaenses' if tamanho == 'TOTAL' else tamanho.lower() + 's'}", f"grafico_idades_{tamanho.lower()}.png")
    
    # Gráfico de eleitos por QP e Média
    proporcao_eleitos = contar_eleitos_por_tipo(df)
    gerar_grafico_barras_duplas(proporcao_eleitos, "Proporção de eleitos por tipo", "grafico_eleitos_proporcao.png")
    salvar_csv(proporcao_eleitos, "dados_eleitos_proporcao.csv")

if __name__ == "__main__":
    main()