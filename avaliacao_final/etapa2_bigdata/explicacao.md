# Relatório de Execução do Pipeline de Big Data (Etapa 2)

## 1. Ingestão de Dados
A ingestão foi realizada transferindo o arquivo `avaliacao_transactions.csv` do ambiente local diretamente para o HDFS. Criamos o diretório `/user/bigdata/avaliacao/raw/` para isolar fisicamente os dados brutos, garantindo que o Data Lake mantenha a imutabilidade do dado original antes de qualquer processamento.

## 2. Criação da Tabela Raw (Camada Bronze)
Foi criada a tabela externa `transactions_bronze` no Hive apontando para o diretório no HDFS. Nesta camada, a prioridade foi projetar um esquema sobre o arquivo CSV, mantendo dados temporais no formato string para evitar falhas de conversão durante a leitura inicial e pulando a linha de cabeçalho.

## 3. Estratégia de Particionamento
Na transição para a camada Silver, aplicamos o particionamento dinâmico no Hive pelas colunas `ano`, `mes` e `status`. Essa escolha foi feita para otimizar futuras varreduras. Como auditorias de risco geralmente buscam um recorte temporal específico e separam transações aprovadas de declinadas, o particionamento evita o full table scan, poupando recursos do cluster.

## 4. Limpeza e Tipagem (Camada Silver)
A tabela `transactions_silver` foi criada utilizando o formato Parquet, otimizando o armazenamento (colunar e compactado). Durante a ingestão, aplicamos a conversão do campo de data de string para `TIMESTAMP` e a filtragem de qualidade `transaction_id IS NOT NULL`. Todos os 30.000 registros sobreviveram a esta etapa, pois não havia IDs nulos na base gerada.

Além disso, optamos por manter e utilizar as colunas `channel` e `merchant_category`. Elas são indispensáveis para a área de risco, pois fraudes possuem forte correlação com o meio de captura (ex: App vs. ATM) e com o setor (ex: eletrônicos vs. alimentação). Sem essas colunas, perderíamos a granularidade necessária para os KPIs.

## 5. Agregações para Negócio (Camada Gold)
Na camada Gold, construímos duas visões analíticas agregadas focadas no BI:
1. **gold_risk_channel_segment:** Sumariza o volume transacionado e a contagem/valor de fraudes por canal de venda e segmento do cliente. 
2. **gold_risk_merchant:** Agrupa as métricas de fraude por categoria de estabelecimento e calcula o risk score médio, permitindo que o painel identifique rapidamente setores de alto risco sistêmico.
