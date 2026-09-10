USE techpay_db;

-- Tabela 1: Sumário de Risco por Canal e Segmento do Cliente
CREATE TABLE IF NOT EXISTS gold_risk_channel_segment
STORED AS PARQUET
AS
SELECT 
    ano, 
    mes, 
    channel, 
    segment,
    COUNT(transaction_id) AS total_transactions,
    SUM(amount) AS total_amount,
    SUM(CASE WHEN is_fraud = true THEN 1 ELSE 0 END) AS fraud_count,
    SUM(CASE WHEN is_fraud = true THEN amount ELSE 0 END) AS fraud_amount
FROM transactions_silver
GROUP BY ano, mes, channel, segment;

-- Tabela 2: Sumário de Risco e Score por Categoria de Estabelecimento
CREATE TABLE IF NOT EXISTS gold_risk_merchant
STORED AS PARQUET
AS
SELECT 
    ano, 
    mes, 
    merchant_category,
    COUNT(transaction_id) AS total_transactions,
    SUM(amount) AS total_amount,
    SUM(CASE WHEN is_fraud = true THEN 1 ELSE 0 END) AS fraud_count,
    AVG(risk_score) AS avg_risk_score
FROM transactions_silver
GROUP BY ano, mes, merchant_category;

-- Consultas rápidas para validação na tela
SELECT '--- Amostra Gold: Canal e Segmento ---';
SELECT * FROM gold_risk_channel_segment LIMIT 5;
