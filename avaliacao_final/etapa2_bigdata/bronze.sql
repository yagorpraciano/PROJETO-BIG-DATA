-- Criação do banco de dados do projeto
CREATE DATABASE IF NOT EXISTS techpay_db;
USE techpay_db;

-- Criação da tabela Bronze (Raw) apontando para o HDFS
CREATE EXTERNAL TABLE IF NOT EXISTS transactions_bronze (
    transaction_id INT,
    customer_id INT,
    amount DOUBLE,
    transaction_type STRING,
    channel STRING,
    merchant_category STRING,
    timestamp_str STRING,
    status STRING,
    risk_score DOUBLE,
    segment STRING,
    credit_score INT,
    is_fraud BOOLEAN
)
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/bigdata/avaliacao/raw/'
TBLPROPERTIES ("skip.header.line.count"="1");

-- Validação rápida
SELECT * FROM transactions_bronze LIMIT 10;
