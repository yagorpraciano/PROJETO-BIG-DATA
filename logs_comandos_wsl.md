# 💻 Logs de Comandos do Terminal (WSL)

Abaixo está o registro histórico de todos os comandos executados no ambiente Linux (Ubuntu via WSL) durante o desenvolvimento deste projeto. Este log evidencia a configuração do ambiente, inicialização do ecossistema Hadoop/Hive, ativação de ambientes virtuais, execução de scripts e versionamento com Git.

---
  326  hive
  327  history
  328  cd ~
  329  git clone https://github.com/yagorpraciano/PROJETO-BIG-DATA.git
  330  cd PROJETO-BIG-DATA/
  331  ls -la
  332  python3 -m venv venv
  333  source venv/bin/activate
  334  pip install pandas numpy
  335  python3 gerar_base.py
  336  ls -la
  337  hdfs dfs -mkdir -p /user/bigdata/avaliacao/raw/
  338  start-all.sh
  339  jps
  340  hdfs dfs -mkdir -p /user/bigdata/avaliacao/raw/
  341  hdfs dfs -put avaliacao_transactions.csv /user/bigdata/avaliacao/raw/
  342  hdfs dfs -ls /user/bigdata/avaliacao/raw/
  343  mkdir -p avaliacao_final/etapa2_bigdata/
  344  nano avaliacao_final/etapa2_bigdata/bronze.sql
  345  hive -f avaliacao_final/etapa2_bigdata/bronze.sql
  346  rm -rf metastore_db
  347  schematool -dbType derby -initSchema
  348  hive -f avaliacao_final/etapa2_bigdata/bronze.sql
  349  git add .
  350  git commit -m "Cria a tabela transations_bronze no Hive"
  351  git config --global user.name "Haroldo Soares"
  352  git config --global user.email "haroldo22fin@gmail.com"
  353  git commit -m "Cria a tabela transations_bronze no Hive"
  354  git push origin main
  355  nano avaliacao_final/etapa2_bigdata/silver.sql
  356  hive -f avaliacao_final/etapa2_bigdata/silver.sql
  357  git add .
  358  git commit -m "Cria a camada Silver em Parquet com particionamento"
  359  git push origin main
  360  git pull origin main --no-edit
  361  git config pull.rebase false
  362  git pull origin main --no-edit
  363  git push origin main
  364  ls
  365  cd PROJETO-BIG-DATA/
  366  ls
  367  start-all.sh
  368  jps
  369  nano avaliacao_final/etapa2_bigdata/gold.sql
  370  hive -f avaliacao_final/etapa2_bigdata/gold.sql
  371  git add .
  372  git commit -m "Cria tabelas agregadas da Camada Gold para o painel de BI"
  373  git push origin main
  374  nano avaliacao_final/etapa2_bigdata/explicacao.md
  375  git add .
  376  git commit -m "Corrige explicacao.md para refletir exatamente os scripts SQL executados"
  377  git push origin main
  378  mkdir -p avaliacao_final/etapa3_analise/
  379  pip install pandas plotly
  380  source venv/bin/activate
  381  pip install pandas plotly
  382  hive -e 'set hive.cli.print.header=true; select * from techpay_db.gold_risk_channel_segment;' | tr '\t' ',' > avaliacao_final/etapa3_analise/risk_channel.csv
  383  hive -e 'set hive.cli.print.header=true; select * from techpay_db.gold_risk_merchant;' | tr '\t' ',' > avaliacao_final/etapa3_analise/risk_merchant.csv
  384  ls
  385  mkdir -p ~/lab_pipeline_bigdata/{scripts,notebooks,docs,dados}
  386  cd lab_pipeline_bigdata/
  387  python3 -m venv .venv
  388  source .venv/bin/activate
  389  git init
  390  cat << 'EOF' > .gitignore
  391  .venv/
  392  __pycache__/
  393  *.pyc
  394  .ipynb_checkpoints/
  395  derby.log
  396  metastore_db/
  397  EOF
  398  cat << 'EOF' > scripts/lab02_sqoop_ingestion.sh
  399  #!/bin/bash
  400  # Lab 02: Ingestão MySQL -> HDFS via Apache Sqoop
  401  sqoop import \
  402    --connect jdbc:mysql://localhost:3306/bigdata_db \
  403    --username root -P \
  404    --table customers \
  405    --target-dir /user/bigdata/raw/customers \
  406    --delete-target-dir \
  407    -m 1
  408  sqoop import \
  409    --connect jdbc:mysql://localhost:3306/bigdata_db \
  410    --username root -P \
  411    --table transactions \
  412    --target-dir /user/bigdata/raw/transactions \
  413    --delete-target-dir \
  414    --split-by transaction_id \
  415    -m 4
  416  EOF
  417  cat << 'EOF' > scripts/lab03_raw_tables.sql
  418  -- Lab 03: Criação de Tabelas Raw no Hive (External vs Managed)
  419  CREATE EXTERNAL TABLE IF NOT EXISTS raw_customers (
  420    customer_id INT,
  421    name STRING,
  422    cpf STRING,
  423    email STRING,
  424    segment STRING,
  425    credit_score INT,
  426    created_at STRING
  427  )
  428  ROW FORMAT DELIMITED 
  429  FIELDS TERMINATED BY ','
  430  STORED AS TEXTFILE
  431  LOCATION '/user/bigdata/raw/customers';
  432  -- Demonstração de Managed Table e teste de ciclo de vida (DROP)
  433  CREATE TABLE IF NOT EXISTS teste_managed (
  434    id INT,
  435    valor STRING
  436  );
  437  INSERT INTO teste_managed VALUES (1, 'teste_ciclo_de_vida');
  438  DROP TABLE teste_managed;
  439  EOF
  440  cat << 'EOF' > scripts/lab04_partitioning.sql
  441  -- Lab 04: Otimização com Tabela Particionada (Year/Month)
  442  CREATE EXTERNAL TABLE IF NOT EXISTS raw_transactions (
  443    transaction_id INT,
  444    customer_id INT,
  445    transaction_type STRING,
  446    amount FLOAT,
  447    status STRING,
  448    ts STRING,
  449    risk_score FLOAT,
  450    is_fraud BOOLEAN
  451  )
  452  ROW FORMAT DELIMITED 
  453  FIELDS TERMINATED BY ','
  454  STORED AS TEXTFILE
  455  LOCATION '/user/bigdata/raw/transactions';
  456  CREATE TABLE IF NOT EXISTS transactions_particionada (
  457    transaction_id INT,
  458    customer_id INT,
  459    transaction_type STRING,
  460    amount FLOAT,
  461    status STRING,
  462    risk_score FLOAT,
  463    is_fraud BOOLEAN
  464  )
  465  PARTITIONED BY (year INT, month INT)
  466  STORED AS TEXTFILE;
  467  SET hive.exec.dynamic.partition = true;
  468  SET hive.exec.dynamic.partition.mode = nonstrict;
  469  INSERT OVERWRITE TABLE transactions_particionada PARTITION(year, month)
  470  SELECT 
  471    transaction_id,
  472    customer_id,
  473    transaction_type,
  474    amount,
  475    status,
  476    risk_score,
  477    is_fraud,
  478    YEAR(ts) AS year,
  479    MONTH(ts) AS month
  480  FROM raw_transactions;
  481  EOF
  482  cat << 'EOF' > scripts/lab05_bronze.sql
  483  -- Lab 05: Camada Bronze em Parquet com Deduplicação via ROW_NUMBER()
  484  CREATE TABLE IF NOT EXISTS bronze_customers (
  485    customer_id INT,
  486    name STRING,
  487    cpf STRING,
  488    email STRING,
  489    segment STRING,
  490    credit_score INT,
  491    created_at DATE
  492  )
  493  STORED AS PARQUET;
  494  INSERT OVERWRITE TABLE bronze_customers
  495  SELECT DISTINCT
  496    customer_id,
  497    name,
  498    cpf,
  499    email,
  500    segment,
  501    CAST(credit_score AS INT) AS credit_score,
  502    CAST(created_at AS DATE) AS created_at
  503  FROM raw_customers
  504  WHERE customer_id IS NOT NULL;
  505  CREATE TABLE IF NOT EXISTS bronze_transactions (
  506    transaction_id INT,
  507    customer_id INT,
  508    transaction_type STRING,
  509    amount FLOAT,
  510    status STRING,
  511    risk_score FLOAT,
  512    is_fraud BOOLEAN,
  513    ts TIMESTAMP
  514  )
  515  STORED AS PARQUET;
  516  INSERT OVERWRITE TABLE bronze_transactions
  517  SELECT 
  518    transaction_id,
  519    customer_id,
  520    transaction_type,
  521    amount,
  522    status,
  523    risk_score,
  524    is_fraud,
  525    ts
  526  FROM (
  527    SELECT 
  528      transaction_id,
  529      customer_id,
  530      transaction_type,
  531      CAST(amount AS FLOAT) AS amount,
  532      status,
  533      CAST(risk_score AS FLOAT) AS risk_score,
  534      CAST(is_fraud AS BOOLEAN) AS is_fraud,
  535      CAST(ts AS TIMESTAMP) AS ts,
  536      ROW_NUMBER() OVER (PARTITION BY transaction_id ORDER BY CAST(ts AS TIMESTAMP) DESC) AS rn
  537    FROM raw_transactions
  538    WHERE amount > 0 AND customer_id IS NOT NULL
  539  ) sub
  540  WHERE rn = 1;
  541  EOF
  542  cat << 'EOF' > scripts/lab06_silver.sql
  543  -- Lab 06: Camada Silver com Enriquecimento e Otimização MapJoin
  544  CREATE TABLE IF NOT EXISTS silver_transactions (
  545    transaction_id INT,
  546    customer_id INT,
  547    amount FLOAT,
  548    transaction_type STRING,
  549    status STRING,
  550    risk_score FLOAT,
  551    is_fraud BOOLEAN,
  552    ts TIMESTAMP,
  553    segment STRING,
  554    credit_score INT,
  555    year INT,
  556    month INT,
  557    day INT,
  558    day_of_week INT,
  559    amount_band STRING
  560  )
  561  STORED AS PARQUET;
  562  INSERT OVERWRITE TABLE silver_transactions
  563  SELECT /*+ MAPJOIN(c) */
  564    t.transaction_id,
  565    t.customer_id,
  566    t.amount,
  567    t.transaction_type,
  568    t.status,
  569    t.risk_score,
  570    t.is_fraud,
  571    t.ts,
  572    c.segment,
  573    c.credit_score,
  574    YEAR(t.ts)  AS year,
  575    MONTH(t.ts) AS month,
  576    DAY(t.ts)   AS day,
  577    DAYOFWEEK(t.ts) AS day_of_week,
  578    CASE
  579      WHEN t.amount < 100  THEN 'baixo'
  580      WHEN t.amount < 1000 THEN 'medio'
  581      ELSE 'alto'
  582    END AS amount_band
  583  FROM bronze_transactions t
  584  JOIN bronze_customers c ON t.customer_id = c.customer_id;
  585  EOF
  586  cat << 'EOF' > scripts/lab07_gold.sql
  587  -- Lab 07: Camada Gold com Agregações de Negócio e Métricas de Fraude
  588  CREATE TABLE IF NOT EXISTS gold_fraud_risk (
  589    segment STRING,
  590    total_transacoes BIGINT,
  591    valor_total DOUBLE,
  592    ticket_medio DOUBLE,
  593    qtd_fraudes BIGINT,
  594    taxa_fraude_pct DOUBLE,
  595    valor_em_risco DOUBLE
  596  )
  597  STORED AS PARQUET;
  598  INSERT OVERWRITE TABLE gold_fraud_risk
  599  SELECT
  600    segment,
  601    COUNT(*) AS total_transacoes,
  602    SUM(amount) AS valor_total,
  603    ROUND(AVG(amount), 2) AS ticket_medio,
  604    SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS qtd_fraudes,
  605    ROUND(100.0 * SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) / COUNT(*), 2) AS taxa_fraude_pct,
  606    SUM(CASE WHEN is_fraud THEN amount ELSE 0 END) AS valor_em_risco
  607  FROM silver_transactions
  608  GROUP BY segment;
  609  CREATE TABLE IF NOT EXISTS gold_daily_metrics (
  610    year INT,
  611    month INT,
  612    day INT,
  613    transacoes BIGINT,
  614    fraudes BIGINT
  615  )
  616  STORED AS PARQUET;
  617  INSERT OVERWRITE TABLE gold_daily_metrics
  618  SELECT
  619    year,
  620    month,
  621    day,
  622    COUNT(*) AS transacoes,
  623    SUM(CASE WHEN is_fraud THEN 1 ELSE 0 END) AS fraudes
  624  FROM silver_transactions
  625  GROUP BY year, month, day;
  626  EOF
  627  # 1. Cria o README detalhando os labs
  628  cat << 'EOF' > README.md
  629  # Pipeline Big Data — Hadoop, Sqoop & Hive
  630  Repositório de entrega dos laboratórios práticos de Engenharia de Dados (Labs 02 ao 07).
  631  ## 📌 Escopo dos Laboratórios
  632  * **Lab 02 — Ingestão com Apache Sqoop:** Extração das tabelas relacionais (`customers` e `transactions`) do MySQL diretamente para o HDFS em `/user/bigdata/raw/`.
  633  * **Lab 03 — Tabelas Raw no Hive:** Mapeamento de tabelas externas desacopladas do HDFS e validação do ciclo de vida de tabelas gerenciadas (*Managed Tables*).
  634  * **Lab 04 — Particionamento Dinâmico:** Implementação de particionamento por `year` e `month` com validação de *Partition Pruning*.
  635  * **Lab 05 — Camada Bronze:** Sanitização de tipos, conversão para formato colunar Parquet e deduplicação estrita via janela analítica (`ROW_NUMBER()`).
  636  * **Lab 06 — Camada Silver:** Enriquecimento dimensional via `MAPJOIN` (Broadcast Join) unindo transações e clientes com derivação de métricas temporais e faixas de valor.
  637  * **Lab 07 — Camada Gold:** Agregações analíticas e consolidação de KPIs de risco de fraude por segmento e métricas diárias.
  638  ## 📁 Estrutura de Arquivos
  639  * `scripts/`: Código-fonte DDL e DML de cada estágio do pipeline.
  640  * `docs/`: Documentação e evidências de execução.
  641  EOF
  642  # 2. Adiciona os arquivos ao rastreamento do Git
  643  git add .
  644  # 3. Cria a branch main e faz o commit inicial
  645  git branch -M main
  646  git commit -m "feat: documentacao e scripts dos labs 02 ao 07"
  647  git remote add origin https://github.com/HaroldoSoares/lab_pipeline_bigdata.git
  648  git push -u origin main
  649  hdfs dfs -cat /user/bigdata/raw/customers/part-m-00000 | head -n 3
  650  start-dfs.sh
  651  start-yarn.sh
  652  jps
  653  hdfs dfs -cat /user/bigdata/raw/customers/part-m-00000 | head -n 3
  654  hive
  655  ls
  656  cd PROJETO-BIG-DATA/
  657  ls
  658  source venv/bin/activate
  659  start-all.sh
  660  jps
  661  pip install pandas plotly
  662  hive -e 'set hive.cli.print.header=true; select * from techpay_db.gold_risk_channel_segment;' | tr '\t' ',' > avaliacao_final/etapa3_analise/risk_channel.csv
  663  hive -e 'set hive.cli.print.header=true; select * from techpay_db.gold_risk_merchant;' | tr '\t' ',' > avaliacao_final/etapa3_analise/risk_merchant.csv
  664  nano avaliacao_final/etapa3_analise/gerar_dashboard.py
  665  python avaliacao_final/etapa3_analise/gerar_dashboard.py
  666  git add .
  667  git commit -m "Cria painel interativo de BI em HTML via Python"
  668  git push origin main
  669  nano avaliacao_final/etapa3_analise/gerar_dashboard.py
  670  python avaliacao_final/etapa3_analise/gerar_dashboard.py
  671  mkdir -p avaliacao_final/etapa3_analise/evidencias
  672  explorer.exe avaliacao_final/etapa3_analise/
  673  git add .
  674  git commit -m "Upgrade do Dashboard: Adiciona cartoes de KPI, grafico donut e print de evidencia"
  675  git push origin main
  676  git pull origin main --no-edit
  677  git push origin main
  678  pip install pyspark
  679  nano avaliacao_final/etapa4_ml/modelo_fraude.py
  680  python avaliacao_final/etapa4_ml/modelo_fraude.py
  681  pip uninstall -y pyspark
  682  pip install pyspark==3.4.1
  683  python avaliacao_final/etapa4_ml/modelo_fraude.py
  684  pip uninstall -y pyspark
  685  pip install pyspark==3.5.1
  686  python avaliacao_final/etapa4_ml/modelo_fraude.py
  687  pip install setuptools
  688  python avaliacao_final/etapa4_ml/modelo_fraude.py
  689  nano avaliacao_final/etapa4_ml/explicacao.md
  690  git add .
  691  git commit -m "Finaliza Etapa 4: Treina modelo PySpark e adiciona justificativa de ML"
  692  git push origin main
  693  nano README.md
  694  git add README.md
  695  git commit -m "Docs: Atualiza README com a documentacao executiva do projeto completo"
  696  git push origin main
  697  nano avaliacao_final/etapa3_analise/relatorio_achados.md
  698  nano avaliacao_final/etapa4_ml/explicacao.md
  699  git add .
  700  git commit -m "Docs: Adiciona framework Finding-Insight-Action na Etapa 3 e interpretação do modelo na Etapa 4"
  701  git push origin main
  702  nano avaliacao_final/etapa3_analise/ideia_bi.md
  703  git add avaliacao_final/etapa3_analise/ideia_bi.md
  704  git commit -m "Docs: Adiciona descricao da ideia do BI respondendo as 4 perguntas do edital"
  705  git push origin main
  706  nano avaliacao_final/etapa3_analise/ideia_bi.md
  707  nano avaliacao_final/etapa3_analise/relatorio_achados.md
  708  nano avaliacao_final/etapa4_ml/explicacao.md
  709  nano DIARIO_DE_BORDO_ERROS.md
  710  git add DIARIO_DE_BORDO_ERROS.md
  711  git commit -m "Docs: Adiciona logs reais de terminal no diario de erros para maior veracidade"
  712  git push origin main
  713  ls
  714  cd PROJETO-BIG-DATA/
  715  history
  716  history | tail -n 200 > HISTORICO_COMANDOS.md
  717  nano HISTORICO_COMANDOS.md
  718  history | tail -n 322 > logs_comandos_wsl.md
  719  nano logs_comandos_wsl.md 
  720  history | tail -n 400 > logs_comandos_wsl.md
