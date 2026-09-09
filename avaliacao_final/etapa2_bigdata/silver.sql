USE techpay_db;

-- Habilita o particionamento dinâmico no Hive para gerar as pastas automaticamente
SET hive.exec.dynamic.partition = true;
SET hive.exec.dynamic.partition.mode = nonstrict;

-- Cria a tabela Silver otimizada (Parquet) e particionada
CREATE TABLE IF NOT EXISTS transactions_silver (
    transaction_id INT,
    customer_id INT,
    amount DOUBLE,
    transaction_type STRING,
    channel STRING,
    merchant_category STRING,
    transaction_timestamp TIMESTAMP,
    risk_score DOUBLE,
    segment STRING,
    credit_score INT,
    is_fraud BOOLEAN
)
PARTITIONED BY (ano STRING, mes STRING, status STRING)
STORED AS PARQUET;

-- Ingestão de dados da Bronze para a Silver com transformações e limpeza
INSERT OVERWRITE TABLE transactions_silver PARTITION (ano, mes, status)
SELECT 
    transaction_id,
    customer_id,
    amount,
    transaction_type,
    channel,
    merchant_category,
    CAST(timestamp_str AS TIMESTAMP) AS transaction_timestamp,
    risk_score,
    segment,
    credit_score,
    is_fraud,
    -- Colunas de partição DEVEM vir no final do SELECT na mesma ordem da declaração
    SUBSTR(timestamp_str, 1, 4) AS ano,
    SUBSTR(timestamp_str, 6, 2) AS mes,
    status
FROM transactions_bronze
WHERE transaction_id IS NOT NULL; 

-- Consulta rápida para validar se os dados foram gravados corretamente
SELECT * FROM transactions_silver LIMIT 10;
