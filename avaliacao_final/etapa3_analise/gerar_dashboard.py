import pandas as pd
import plotly.express as px

# 1. Carregar os dados
df_channel = pd.read_csv('avaliacao_final/etapa3_analise/risk_channel.csv')
df_merchant = pd.read_csv('avaliacao_final/etapa3_analise/risk_merchant.csv')

# Limpeza no nome das colunas
df_channel.columns = [c.split('.')[-1] for c in df_channel.columns]
df_merchant.columns = [c.split('.')[-1] for c in df_merchant.columns]

# 2. Calcular KPIs para os Cartões
kpi_valor_fraude = df_channel['fraud_amount'].sum()
kpi_qtd_fraude = df_channel['fraud_count'].sum()
kpi_risco_medio = df_merchant['avg_risk_score'].mean()

cartoes_html = f"""
<div style="display: flex; gap: 20px; margin-bottom: 30px;">
    <div style="flex: 1; background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h3 style="margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">💰 Valor Total Fraudado</h3>
        <h2 style="margin: 15px 0 0 0; font-size: 32px;">R$ {kpi_valor_fraude:,.2f}</h2>
    </div>
    <div style="flex: 1; background: linear-gradient(135deg, #f39c12, #d35400); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h3 style="margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">🚨 Transações Suspeitas</h3>
        <h2 style="margin: 15px 0 0 0; font-size: 32px;">{kpi_qtd_fraude:,.0f}</h2>
    </div>
    <div style="flex: 1; background: linear-gradient(135deg, #34495e, #2c3e50); color: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h3 style="margin: 0; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">📊 Risco Médio Global</h3>
        <h2 style="margin: 15px 0 0 0; font-size: 32px;">{kpi_risco_medio:.1f} <span style="font-size:16px">/ 1000</span></h2>
    </div>
</div>
"""

# 3. Criar Gráficos
fig1 = px.bar(df_channel, x='channel', y='fraud_amount', color='segment', barmode='group',
              title='Valor Fraudado por Canal e Segmento', labels={'fraud_amount': 'R$', 'channel': 'Canal', 'segment': 'Segmento'})
fig2 = px.bar(df_merchant, x='merchant_category', y='avg_risk_score', color='avg_risk_score', color_continuous_scale='Reds',
              title='Risco por Setor', labels={'avg_risk_score': 'Risco', 'merchant_category': 'Setor'})
fig3 = px.pie(df_channel, values='fraud_count', names='channel', hole=0.4,
              title='Distribuição de Fraudes por Canal')

# 4. Montar a página HTML final usando Grid
html_content = f"""
<html>
<head>
    <title>Dashboard de Risco - TechPay</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; background-color: #f0f2f5; padding: 30px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .header h1 {{ color: #1a237e; margin: 0; font-size: 28px; }}
        .header p {{ color: #546e7a; margin-top: 5px; font-size: 16px; }}
        .grid-container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .chart-box {{ background: white; padding: 15px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .chart-full {{ grid-column: span 2; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛡️ Executive Risk Dashboard (Camada Gold)</h1>
        <p>Monitoramento de Fraudes e Vulnerabilidades Sistêmicas - Data Lake TechPay</p>
    </div>
    
    {cartoes_html}

    <div class="grid-container">
        <div class="chart-box chart-full">
            {fig1.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
        <div class="chart-box">
            {fig3.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
        <div class="chart-box">
            {fig2.to_html(full_html=False, include_plotlyjs='cdn')}
        </div>
    </div>
</body>
</html>
"""

# Salvar
with open('avaliacao_final/etapa3_analise/dashboard_risco.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ Dashboard turbinado gerado com sucesso!")
