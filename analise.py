import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# --- Configurações Iniciais ---
sns.set_theme(style="whitegrid")

# O nome do arquivo .json que você forneceu
input_filename = 'teste.json'

print(f"Iniciando a análise do arquivo: {input_filename}\n")

# --- 1. Carregamento e Preparação dos Dados ---
try:
    if not os.path.exists(input_filename):
        raise FileNotFoundError(f"Erro: O arquivo '{input_filename}' não foi encontrado no diretório.")
        
    # Lê o JSON (assumindo um objeto JSON por linha)
    df = pd.read_json(input_filename, lines=True)
    
    print("Dados carregados com sucesso.")
    print(f"Total de conexões no dataset: {len(df)}")

    # Converte 'label' para nomes mais claros para os gráficos
    df['status'] = df['label'].map({0: 'Normal', 1: 'Ataque'})

except FileNotFoundError as e:
    print(e)
    exit()
except Exception as e:
    print(f"Ocorreu um erro ao ler o arquivo JSON: {e}")
    print("Verifique se o formato do JSON está correto (um objeto por linha).")
    exit()


# --- 2. Relatório: Resumo Geral do Tráfego ---
print("\n--- Gerando Relatório 1: Resumo Geral ---")
total_conexoes = len(df)
ataque_counts = df['status'].value_counts()
perc_normal = (ataque_counts.get('Normal', 0) / total_conexoes) * 100
perc_ataque = (ataque_counts.get('Ataque', 0) / total_conexoes) * 100

print(f"Total de Conexões: {total_conexoes}")
print(f"Conexões Normais: {ataque_counts.get('Normal', 0)} ({perc_normal:.1f}%)")
print(f"Conexões de Ataque: {ataque_counts.get('Ataque', 0)} ({perc_ataque:.1f}%)")

# Gráfico de Pizza
plt.figure(figsize=(8, 6))
plt.pie(
    [perc_normal, perc_ataque],
    labels=['Normal', 'Ataque'],
    autopct='%1.1f%%',
    colors=['#4CAF50', '#F44336'],
    startangle=90
)
plt.title('Relatório 1: Resumo do Tráfego: Normal vs. Ataque')
plt.savefig('1_resumo_geral.png')
print("Salvo: 1_resumo_geral.png")
plt.clf() # Limpa a figura para o próximo gráfico


# --- 3. Relatório: Distribuição dos Ataques por Categoria ---
print("\n--- Gerando Relatório 2: Distribuição de Ataques ---")
df_ataques = df[df['label'] == 1]

if not df_ataques.empty:
    attack_cat_counts = df_ataques['attack_cat'].value_counts()
    print("Contagem de ataques por categoria:")
    print(attack_cat_counts)

    plt.figure(figsize=(12, 7))
    sns.barplot(
        x=attack_cat_counts.values,
        y=attack_cat_counts.index,
        palette='Reds_r'
    )
    plt.title('Relatório 2: Distribuição de Ataques por Categoria')
    plt.xlabel('Número de Conexões')
    plt.ylabel('Categoria do Ataque')
    plt.tight_layout()
    plt.savefig('2_distribuicao_ataques.png')
    print("Salvo: 2_distribuicao_ataques.png")
    plt.clf()
else:
    print("Nenhum ataque encontrado no dataset.")


# --- 4. Relatório: Distribuição dos Protocolos ---
print("\n--- Gerando Relatório 3: Protocolos Mais Utilizados ---")
proto_counts = df['proto'].value_counts().head(10)
print("Contagem dos 10 principais protocolos:")
print(proto_counts)

plt.figure(figsize=(10, 6))
sns.barplot(
    x=proto_counts.values,
    y=proto_counts.index,
    palette='Blues_d'
)
plt.title('Relatório 3: Top 10 Protocolos Mais Utilizados (Geral)')
plt.xlabel('Número de Conexões')
plt.ylabel('Protocolo')
plt.tight_layout()
plt.savefig('3_distribuicao_protocolos.png')
print("Salvo: 3_distribuicao_protocolos.png")
plt.clf()


# --- 5. Relatório: Top 5 Serviços ---
print("\n--- Gerando Relatório 4: Top 5 Serviços Acessados ---")
service_counts = df[df['service'] != '-']['service'].value_counts().head(5)

if not service_counts.empty:
    print("Contagem dos 5 principais serviços (excluindo '-'):")
    print(service_counts)

    plt.figure(figsize=(10, 5))
    sns.barplot(
        x=service_counts.values,
        y=service_counts.index,
        palette='Greens_d'
    )
    plt.title('Relatório 4: Top 5 Serviços Mais Acessados (excluindo "-")')
    plt.xlabel('Número de Conexões')
    plt.ylabel('Serviço')
    plt.tight_layout()
    plt.savefig('4_top_5_servicos.png')
    print("Salvo: 4_top_5_servicos.png")
    plt.clf()
else:
    print("Nenhum serviço identificado (além de '-').")


# --- 6. Relatório: Tendência Temporal (Simulada) ---
print("\n--- Gerando Relatório 5: Tendência Temporal (Simulada) ---")
tamanho_lote = max(1, len(df) // 100) 
df['grupo_temporal'] = df.index // tamanho_lote

ataques_por_grupo = df.groupby('grupo_temporal')['label'].sum()
conexoes_normais_grupo = df[df['label'] == 0].groupby('grupo_temporal').size()

plt.figure(figsize=(14, 6))
ataques_por_grupo.plot(kind='line', color='red', label='Ataques', lw=2)
conexoes_normais_grupo.plot(kind='line', color='green', label='Normal', linestyle='--')
plt.title('Relatório 5: Tendência de Tráfego (Simulada por Lotes de Registros)')
plt.xlabel(f'Lote de Registros (Tamanho do Lote: {tamanho_lote})')
plt.ylabel('Número de Conexões')
plt.legend()
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.savefig('5_tendencia_temporal.png')
print(f"Salvo: 5_tendencia_temporal.png (Lotes de {tamanho_lote} conexões)")
plt.clf()


# --- 7. Relatório: Insights Relevantes (Protocolos e Ataques) ---
print("\n--- Gerando Relatório 6: Insights de Ataque ---")
proto_ataque = pd.crosstab(df['proto'], df['status'])

if 'Ataque' in proto_ataque.columns:
    proto_ataque['total'] = proto_ataque.sum(axis=1)
    proto_ataque['perc_ataque'] = (proto_ataque['Ataque'] / proto_ataque['total']) * 100
    proto_ataque_sorted = proto_ataque.sort_values(by='perc_ataque', ascending=False)

    print("\nInsights - % de Ataque por Protocolo:")
    print(proto_ataque_sorted[['perc_ataque', 'Ataque', 'total']].head())

    # Seleciona os N principais protocolos para um gráfico mais limpo
    top_protos_idx = df['proto'].value_counts(normalize=True).head(15).index
    proto_ataque_top = proto_ataque.loc[top_protos_idx]
    
    # Normaliza para 100%
    proto_ataque_perc = proto_ataque_top[['Normal', 'Ataque']].div(
        proto_ataque_top['total'], axis=0
    ).sort_values(by='Ataque', ascending=False)

    proto_ataque_perc.plot(
        kind='barh',
        stacked=True,
        figsize=(12, 8),
        colormap='coolwarm_r',
        legend=True
    )
    plt.title('Relatório 6: Proporção Ataque vs. Normal por Protocolo (Top 15)')
    plt.xlabel('Proporção')
    plt.ylabel('Protocolo')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter('{:.0%}'.format))
    plt.tight_layout(rect=[0, 0, 0.85, 1]) 
    plt.savefig('6_insight_protocolos_ataque.png')
    print("Salvo: 6_insight_protocolos_ataque.png")
    plt.clf()
else:
    print("Nenhum ataque encontrado para gerar insights de protocolo.")

print("\n--- Análise Concluída ---")
print("Todos os relatórios visuais foram salvos como arquivos .png na sua pasta.")
print("Use 'plt.show()' após cada 'plt.savefig()' se quiser exibi-los interativamente.")