# 🚀 Projeto Big Data: TechPay - Prevenção a Fraudes

Bem-vindo ao repositório do projeto final de Big Data. Este projeto simula um ambiente real de Engenharia de Dados e Machine Learning de ponta a ponta, projetado para uma fintech (TechPay) com o objetivo de identificar e monitorar transações fraudulentas.

## 🛠️ Stack Tecnológica
* **Ecossistema Hadoop:** HDFS (Armazenamento Distribuído) e Apache Hive (Processamento SQL / Data Lake).
* **Processamento e ML:** Apache Spark (PySpark) e Random Forest.
* **Análise e BI:** Python, Pandas, Plotly (HTML interativo).
* **Infraestrutura:** Linux (WSL), Git e GitHub.

---

## 📁 Estrutura do Repositório e Etapas do Projeto

O pipeline foi construído seguindo as melhores práticas da arquitetura Medallion (Bronze, Silver, Gold):

### 📌 Etapa 1: Arquitetura (`/etapa1_arquitetura`)
Contém o desenho lógico e conceitual do ecossistema de dados, justificando a escolha técnica de cada componente, desde a ingestão (HDFS) até o consumo visual e analítico.

### 🗄️ Etapa 2: Pipeline de Big Data (`/etapa2_bigdata`)
Scripts SQL executados no Apache Hive para a construção do nosso Data Lake:
* **Bronze:** Ingestão dos dados brutos a partir do arquivo CSV original.
* **Silver:** Limpeza de dados nulos, conversão para o formato colunar otimizado (`Parquet`) e particionamento inteligente por data (`dt_transacao`).
* **Gold:** Criação de visões analíticas agregadas (risco por setor, fraudes por canal e segmento) prontas para consumo da área de negócios.

### 📊 Etapa 3: Business Intelligence e Dashboard (`/etapa3_analise`)
Consumo dos dados da camada Gold para a geração de um painel executivo de monitoramento de risco.
* Utilizamos um script Python (`gerar_dashboard.py`) para consumir os dados exportados do Hive.
* O resultado é um **Dashboard em HTML 100% interativo** (com cartões de KPI e gráficos Plotly), dispensando a necessidade de conexões complexas de banco de dados para o usuário final.

### 🤖 Etapa 4: Machine Learning (`/etapa4_ml`)
Desenvolvimento de um modelo preditivo utilizando **PySpark** para rodar em modo distribuído.
* Realizamos *Feature Engineering* e vetorização dos dados (transformando categorias em índices).
* Treinamos um modelo **Random Forest Classifier** dividindo a base em treino (80%) e teste (20%).
* O modelo obteve uma Área sob a Curva ROC (AUC-ROC) de aproximadamente **78%**, validando a eficácia do pipeline na identificação de padrões de fraude.

---
*Projeto acadêmico desenvolvido para consolidar conhecimentos em Engenharia de Dados, Processamento Distribuído e Machine Learning.*

## 🚨 Troubleshooting e Evidências Práticas

Como a infraestrutura de Big Data deste projeto foi configurada do zero em ambiente **Linux (WSL)**, documentamos todos os desafios de infraestrutura e os comandos executados para dar total transparência ao trabalho:

- [📓 Diário de Bordo e Solução de Problemas](DIARIO_DE_BORDO_ERROS.md): Registro dos principais conflitos de ambiente (como incompatibilidade de Java vs PySpark) e as soluções de contorno aplicadas.
- [💻 Logs do Terminal WSL](logs_comandos_wsl.md): Histórico bruto de comandos executados, evidenciando a subida do cluster Hadoop/Hive, ativação de ambientes virtuais e versionamento.
