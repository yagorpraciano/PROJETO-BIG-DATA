from pyspark.sql import SparkSession
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml import Pipeline

print("Iniciando o cluster local do Spark...")

# 1. Iniciar Sessão Spark (Rodando em modo local utilizando todos os núcleos)
spark = SparkSession.builder \
    .appName("TechPay Fraud Detection") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR") # Para limpar os logs da tela

# 2. Carregar Dados
# Vamos ler o arquivo raw para o PySpark fazer todo o tratamento
print("Carregando base de dados...")
df = spark.read.csv("avaliacao_transactions.csv", header=True, inferSchema=True)

# 3. Preparação de Dados (Feature Engineering)
# O Spark MLlib exige que variáveis em texto (como canal e segmento) virem números
colunas_categoricas = ["transaction_type", "channel", "merchant_category", "segment"]
indexers = [
    StringIndexer(inputCol=coluna, outputCol=coluna+"_index").fit(df)
    for coluna in colunas_categoricas
]

# Montar o "Vetor de Features" (As variáveis que o modelo vai usar para prever a fraude)
assembler = VectorAssembler(
    inputCols=["amount", "risk_score", "credit_score", "transaction_type_index", 
               "channel_index", "merchant_category_index", "segment_index"],
    outputCol="features"
)

# O Spark precisa que a coluna alvo (is_fraud) seja um número inteiro (0 ou 1)
df = df.withColumn("label", df["is_fraud"].cast("integer"))

# 4. Divisão Treino e Teste (80% para treinar o robô, 20% para testá-lo)
treino, teste = df.randomSplit([0.8, 0.2], seed=42)

# 5. Configurar o Algoritmo (Random Forest)
rf = RandomForestClassifier(featuresCol="features", labelCol="label", numTrees=50, maxDepth=5)

# 6. Criar o Pipeline de Execução e Treinar o Modelo
print("Treinando o modelo Random Forest. Isso pode levar alguns segundos...")
pipeline = Pipeline(stages=indexers + [assembler, rf])
modelo = pipeline.fit(treino)

# 7. Avaliar o Modelo
print("Avaliando o modelo com os dados de teste...")
previsoes = modelo.transform(teste)
evaluator = BinaryClassificationEvaluator(labelCol="label", rawPredictionCol="rawPrediction", metricName="areaUnderROC")
auc = evaluator.evaluate(previsoes)

print("="*60)
print(f"✅ TREINAMENTO CONCLUÍDO COM SUCESSO!")
print(f"📊 Métrica de Acerto (Área sob a Curva ROC): {auc:.4f}")
print("   * Uma nota 1.0000 significa 100% de precisão perfeita.")
print("="*60)

# Opcional: Salvar o pipeline treinado
# modelo.save("avaliacao_final/etapa4_ml/modelo_rf_treinado")

spark.stop()
