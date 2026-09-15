import pandas as pd
import plotly.express as px
import plotly.io as pio

# 1. Carregar os dados extraídos do Hive
df_channel = pd.read_csv('avaliacao_final/etapa3_analise/risk_channel.csv')
df_merchant = pd.read_csv('avaliacao_final/etapa3_analise/risk_merchant.csv')

# 2. Limpeza no nome das colunas (O Hive exporta no formato 'tabela.coluna', isso limpa para 'coluna')
df_channel.columns = [c.split('.')[-1] for c in df_channel.columns]
df_merchant.columns = [c.split('.')[-1] for c in df_merchant.columns]

# 3. Criar Gráfico 1: Valor de Fraude por Canal e Segmento
fig1 = px.bar(df_channel, x='channel', y='fraud_amount', color='segment', barmode='group',
              title='Valor Total de Fraudes por Canal e Segmento', 
              labels={'fraud_amount': 'Valor Fraudado (R$)', 'channel': 'Canal', 'segment': 'Segmento'})

# 4. Criar Gráfico 2: Risco por Categoria de Estabelecimento
fig2 = px.bar(df_merchant, x='merchant_category', y='avg_risk_score',
              title='Score de Risco Médio por Setor (Estabelecimento)', 
              labels={'avg_risk_score': 'Risco Médio', 'merchant_category': 'Categoria do Estabelecimento'},
              color='avg_risk_score', color_continuous_scale='Reds')

# 5. Montar a página HTML do Dashboard
html_content = f"""
<html>
<head>
    <title>Dashboard de Risco - TechPay</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f4f7f6; }}
        .container {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0px 0px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; text-align: center; }}
        p {{ text-align: center; color: #7f8c8d; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Painel de Monitoramento de Fraudes (Camada Gold)</h1>
        <p>Visões analíticas processadas no Data Lake TechPay.</p>
        <hr>
        {fig1.to_html(full_html=False, include_plotlyjs='cdn')}
        <br>
        {fig2.to_html(full_html=False, include_plotlyjs='cdn')}
    </div>
</body>
</html>
"""

# Salvar o arquivo final
with open('avaliacao_final/etapa3_analise/dashboard_risco.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Sucesso! Dashboard gerado: avaliacao_final/etapa3_analise/dashboard_risco.html")
