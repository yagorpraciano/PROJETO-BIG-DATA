# Arquitetura de Big Data — TechPay

## 1. Visão Geral da Solução e Fluxo Arquitetural

A arquitetura proposta para a TechPay atende ao processamento analítico de transações financeiras com foco em auditoria e detecção de padrões de fraude. O pipeline adota o padrão de arquitetura Medalhão (Bronze, Silver e Gold), garantindo linhagem, governança e conformidade analítica.

* **Origem dos Dados:** Bancos relacionais operacionais OLTP da TechPay (PostgreSQL/MySQL), responsáveis pelo registro em tempo real das transações de compras, transferências e pagamentos nos canais app e web.
* **Camada de Ingestão:** Executada via Apache Sqoop em lotes programados (batch) durante janelas de menor carga operacional, realizando a extração direta das tabelas transacionais para o cluster.
* **Armazenamento Bruto (Bronze Layer):** Localizado no Apache HDFS sob `/user/bigdata/avaliacao/raw/`, persistindo os arquivos em formato CSV bruto sem qualquer transformação, garantindo imutabilidade e integridade para auditorias futuras.
* **Processamento e Refinamento (Silver Layer):** Implementado via Apache Spark/Hive, convertendo os dados brutos para formato colunar Parquet particionado. Realiza limpeza de tipos, tratamento de registros corrompidos e padronização das dimensões operacionais.
* **Modelagem Analítica (Gold Layer):** Agregações analíticas e métricas de risco consolidadas via Spark SQL, calculando taxas de fraude por canal, volume financeiro por segmento de cliente e scores consolidados, persistidas em Parquet otimizado com estatísticas de cabeçalho.
* **Camada de Serving e BI:** Disponibilização dos dados agregados da camada Gold para ferramentas analíticas de negócio (Metabase e dashboards HTML/Python interativos via DuckDB/Spark JDBC), entregando visualizações diretas aos analistas de risco e comitês executivos.

---

## 2. Escolha e Justificativa da Ferramenta de Ingestão

Para a ingestão dos dados transacionais, a tecnologia selecionada foi o **Apache Sqoop**, operando em regime de lotes (batch). O Sqoop aproveita o paralelismo nativo do MapReduce para fatiar consultas SQL contra o banco relacional de produção e gravar os blocos paralelizados diretamente nos DataNodes do HDFS.

A principal alternativa considerada foi o **Apache Kafka** integrado com **Kafka Connect**. A decisão por não adotá-lo no desenho base decorre do escopo do problema proposto pela TechPay: análises de fechamento diário, consolidação de métricas regulatórias e retreinamento periódico de modelos de machine learning não demandam complexidade de streaming sub-segundo. A manutenção de um cluster Kafka imporia custos operacionais elevados de zookeeper/KRaft, gerenciamento de offsets, buffer em disco e garantia de entrega (*exactly-once semantics*), sem que houvesse benefício prático imediato para um pipeline cujo objetivo de negócio é o fechamento analítico em D-1.

---

## 3. Estrutura de Armazenamento e Formatos de Arquivo

* **Camada Bronze (CSV):** Mantido em CSV exclusivamente porque espelha o formato original de despejo ou extração bruta dos sistemas legados. Permite rastreabilidade histórica pura e reprocessamento completo do zero caso regras de negócio sofram alterações.
* **Camadas Silver e Gold (Apache Parquet):** A adoção mandatória de Parquet nestas camadas decorre de ganhos massivos em consultas analíticas OLAP:
  * **Armazenamento Colunar com Snappy:** O algoritmo de compressão reduz o consumo de disco no HDFS em até 70% quando comparado ao CSV bruto.
  * **Column Pruning:** Consultas que filtram apenas canais e taxas de fraude leem unicamente os blocos binários dessas variáveis, ignorando colunas pesadas de texto ou IDs não solicitados.
  * **Predicate Pushdown:** O cabeçalho do Parquet armazena valores mínimos e máximos por bloco de dados, permitindo ao mecanismo de consulta (Spark/Hive) pular blocos inteiros de disco que não atendam às cláusulas de filtro (`WHERE`).

---

## 4. Estratégia de Particionamento

A estratégia de particionamento adotada na camada Silver baseia-se na coluna **`timestamp`** truncada na granularidade de **Ano e Mês (`ano=YYYY/mes=MM`)**, combinada com a partição secundária por **`status`** da transação (`approved`, `denied`).

### Cenário de Consulta Real
Em auditorias de conformidade e investigações forenses, o analista de risco financeiro avalia rotineiramente o comportamento de transações recusadas ou em análise no fechamento do mês anterior. Uma consulta para auditar transações de status `denied` ocorridas no mês de agosto de 2026 aproveita o particionamento via *partition pruning*, acessando exclusivamente a pasta física `/ano=2026/mes=08/status=denied/`. Dessa forma, mais de 90% dos dados históricos de outros meses e transações regulares aprovadas são ignorados fisicamente no disco, eliminando varreduras globais (*full table scans*) e otimizando o consumo de memória do cluster.

Evitou-se o particionamento por alta cardinalidade (como `customer_id` ou `transaction_id`), pois criaria o problema de *small files* (milhares de pequenos arquivos sobrecarregando a memória Heap do NameNode).

---

## 5. Análise Crítica e Pontos de Falha

Se o volume diário da TechPay multiplicar por 100 (passando de milhares para dezenas de milhões de transações diárias), os principais gargalos e estratégias de mitigação identificados são:

* **Sobrecarga do Banco Relacional Operacional:** Uma extração via Sqoop multiplicada por 100 concorreria diretamente por conexões, I/O e locks no banco transacional de produção. 
  * *Mitigação:* Isolar as leituras do Sqoop apontando-as exclusivamente para réplicas de leitura (*read replicas*) do banco de dados operacional, ou adotar Change Data Capture (CDC via Debezium) lendo diretamente os logs binários (*wal/binlog*) do banco sem onerar o mecanismo transacional.
* **Gargalo de Heap no NameNode do HDFS:** Milhões de transações geradas continuamente podem resultar em arquivos pequenos caso as gravações sejam frequentes. O NameNode armazena todos os metadados de blocos em memória RAM, o que levaria ao esgotamento de recursos (*OutOfMemoryError*).
  * *Mitigação:* Compactação periódica de arquivos via rotinas MapReduce/Spark para consolidar partições em blocos padrão de 128MB/256MB e transição para arquiteturas de Lakehouse (Apache Iceberg ou Delta Lake) que gerenciam metadados via arquivos manifestos no armazenamento.

---

## 6. Evolução para Detecção de Fraude em Tempo Real

Caso a TechPay altere o requisito de negócio para bloquear transações fraudulentas durante o checkout (tempo de resposta inferior a 200 milissegundos), o desenho arquitetural sofreria as seguintes adaptações:

* **Substituição da Ingestão Batch:** O Sqoop seria substituído por uma mensageria distribuída com **Apache Kafka**, recebendo eventos de autorização disparados diretamente pela API de pagamentos no momento do clique do usuário.
* **Processamento Contínuo de Fluxo:** Implementação de **Spark Structured Streaming** ou **Apache Flink**, consumindo o tópico do Kafka, calculando variáveis comportamentais em janelas deslizantes (ex.: mais de 3 transações no mesmo cartão em 2 minutos) e executando a inferência de Machine Learning em tempo real.
* **Armazenamento de Baixa Latência (Feature Store / Serving):** O HDFS não atende a consultas com latência de milissegundos. Adotar-se-ia um banco NoSQL em memória (como **Redis** ou **Apache Cassandra**) para armazenar os scores de risco e o histórico imediato do cliente, permitindo à API de checkout aprovar ou declinar a transação antes da finalização. O HDFS/Data Lake continuaria existindo em paralelo (Arquitetura Lambda/Kappa), recebendo o dump contínuo do Kafka para análises históricas e retreinamento do modelo.
