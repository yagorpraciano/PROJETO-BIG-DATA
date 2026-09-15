# Relatório de Machine Learning (Etapa 4)

## 1. Escolha da Ferramenta e Algoritmo
Para a construção do modelo preditivo de fraudes, optamos pela utilização do framework PySpark. Essa escolha se justifica pela capacidade do Apache Spark de processar grandes volumes de dados de forma distribuída, aderindo aos princípios de Big Data estabelecidos nas etapas anteriores. O algoritmo escolhido foi o Random Forest Classifier (Floresta Aleatória), devido à sua robustez em lidar com dados desbalanceados e sua excelente capacidade de capturar padrões não-lineares complexos.

## 2. Preparação dos Dados (Feature Engineering)
Como o algoritmo exige entradas matemáticas, aplicamos transformações (String Indexing) nos dados categóricos (como canal, segmento e setor do estabelecimento) para convertê-los em índices numéricos. Em seguida, todas as variáveis explicativas (incluindo o valor transacionado e o score de risco) foram vetorizadas, e a coluna alvo de fraude foi convertida para um formato binário padrão.

## 3. Treinamento e Resultados
A base de dados foi dividida utilizando a proporção de 80% dos dados para o treinamento da inteligência artificial e 20% para a validação. Após o treinamento, o modelo foi avaliado com a métrica Área sob a Curva ROC (AUC-ROC), padrão para problemas de classificação de risco. 

O nosso modelo obteve um score sólido de **0.7774**, indicando uma forte capacidade preditiva de distinguir entre transações legítimas e ataques fraudulentos com base no comportamento de captura e histórico de crédito do usuário. Isso conclui e valida a utilidade de todo o pipeline de dados construído.
