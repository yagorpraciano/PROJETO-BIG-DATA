import pandas as pd
import numpy as np
import os

print("=== INICIANDO PIPELINE DE BIG DATA (ETAPA 2) ===")

# 1. Ingestão
raw_path = os.path.expanduser('~/projeto-bigdata/avaliacao_transactions.csv')
print(f"\n[Etapa 1 - Ingestão]: Lendo arquivo bruto de {raw_path}...")
df_raw = pd.read_csv(raw_path)
print(f"-> Registros ingeridos: {len(df_raw):,} linhas")

# 2. Schema Raw e Tipagem
print("\n[Etapa 2 - Schema Raw]: Validando e convertendo tipagens primitivas...")
df_raw['timestamp'] = pd.to_datetime(df_raw['timestamp'])
df_raw['amount'] = df_raw['amount'].astype(float)
df_raw['risk_score'] = df_raw['risk_score'].astype(float)
df_raw['credit_score'] = df_raw['credit_score'].astype(int)

# 3. Particionamento (Criação de colunas de particionamento: ano, mes, status)
print("\n[Etapa 3 - Particionamento]: Extraindo chaves de particao (ano, mes, status)...")
df_raw['ano'] = df_raw['timestamp'].dt.year
df_raw['mes'] = df_raw['timestamp'].dt.month

# 4. Camada Bronze (Limpeza de duplicatas e valores impossíveis)
print("\n[Etapa 4 - Bronze]: Aplicando regras de qualidade e saneamento...")
# Inserção de regra defensiva: remoção de duplicatas de IDs e amounts negativos/zerados
linhas_iniciais = len(df_raw)
df_bronze = df_raw.drop_duplicates(subset=['transaction_id']).copy()
df_bronze = df_bronze[(df_bronze['amount'] > 0) & (df_bronze['credit_score'] >= 300) & (df_bronze['credit_score'] <= 900)]
linhas_descartadas = linhas_iniciais - len(df_bronze)
print(f"-> Linhas que entraram: {linhas_iniciais:,}")
print(f"-> Linhas descartadas por inconsistência: {linhas_descartadas}")
print(f"-> Linhas sobreviventes na Bronze: {len(df_bronze):,}")

# 5. Camada Silver (Enriquecimento de Negócio)
print("\n[Etapa 5 - Silver]: Enriquecendo dados com variaveis de negocio...")
# Enriquecimento 1: Faixa de Valor (ticket de compra)
df_silver = df_bronze.copy()
df_silver['faixa_valor'] = pd.cut(
    df_silver['amount'], 
    bins=[-np.inf, 50, 200, 1000, np.inf], 
    labels=['Baixo (<=50)', 'Medio (51-200)', 'Alto (201-1000)', 'Critico (>1000)']
)

# Enriquecimento 2: Periodo do dia
hora = df_silver['timestamp'].dt.hour
df_silver['periodo_dia'] = np.where(
    (hora >= 0) & (hora < 6), 'Madrugada',
    np.where((hora >= 6) & (hora < 12), 'Manha',
    np.where((hora >= 12) & (hora < 18), 'Tarde', 'Noite'))
)

# Enriquecimento 3: Sinalizador de alto risco cruzado
df_silver['alerta_risco'] = np.where(
    (df_silver['risk_score'] > 75) & (df_silver['amount'] > 500), 
    'Suspeita Alta', 'Normal'
)
print(f"-> Silver concluida com {len(df_silver):,} linhas e {df_silver.shape[1]} colunas.")

# 6. Camada Gold (Agregações para Serving / BI da Etapa 3)
print("\n[Etapa 6 - Gold]: Gerando visoes analiticas agregadas...")

# Tabela Gold 1: Taxa de Fraude e Volume por Canal e Categoria de Estabelecimento
gold_canal_categoria = df_silver.groupby(['channel', 'merchant_category']).agg(
    total_transacoes=('transaction_id', 'count'),
    volume_total=('amount', 'sum'),
    ticket_medio=('amount', 'mean'),
    qtd_fraudes=('is_fraud', lambda x: x.sum()),
    taxa_fraude_pct=('is_fraud', lambda x: (x.mean() * 100).round(2)),
    score_risco_medio=('risk_score', 'mean')
).reset_index()

# Tabela Gold 2: Comportamento por Segmento de Cliente e Periodo do Dia
gold_segmento_periodo = df_silver.groupby(['segment', 'periodo_dia']).agg(
    total_transacoes=('transaction_id', 'count'),
    volume_total=('amount', 'sum'),
    qtd_fraudes=('is_fraud', lambda x: x.sum()),
    taxa_fraude_pct=('is_fraud', lambda x: (x.mean() * 100).round(2)),
    score_credito_medio=('credit_score', 'mean')
).reset_index()

# Salvando tabelas locais para serving/dashboard
os.makedirs('avaliacao_final/etapa2_bigdata/dados_gold', exist_ok=True)
gold_canal_categoria.to_csv('avaliacao_final/etapa2_bigdata/dados_gold/gold_canal_categoria.csv', index=False)
gold_segmento_periodo.to_csv('avaliacao_final/etapa2_bigdata/dados_gold/gold_segmento_periodo.csv', index=False)

print("\n=== RESUMO DAS TABELAS GOLD ===")
print("\n--- Gold 1: Fraude por Canal e Categoria (Amostra) ---")
print(gold_canal_categoria.head())

print("\n--- Gold 2: Fraude por Segmento e Periodo do Dia (Amostra) ---")
print(gold_segmento_periodo.head())
print("\nPipeline executado com sucesso!")
