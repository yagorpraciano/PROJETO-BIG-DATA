# Relatório de Execução do Pipeline de Dados — Etapa 2

## 1. Descrição das Etapas do Pipeline

### Etapa 1: Ingestão
A etapa de ingestão realizou o carregamento dos dados transacionais a partir do arquivo bruto em disco local e HDFS para a memória de processamento. A leitura validou o cabeçalho e assegurou a integridade dos 30.000 registros originais da TechPay, disponibilizando o volume completo para as etapas subsequentes sem perda de dados.

### Etapa 2: Criação da Tabela Raw e Definição de Esquema
Nesta etapa, os tipos de dados foram formalizados para evitar erros de truncamento ou inferência. As variáveis de valor financeiro e score de risco foram fixadas em ponto flutuante, os identificadores e pontuação de crédito em números inteiros, e a estampa temporal foi convertida para formato nativo de data e hora com granularidade em segundos, garantindo precisão nos cálculos temporais.

### Etapa 3: Particionamento
Aplicou-se a estratégia arquitetural definida na Etapa 1, derivando as dimensões temporais de ano e mês a partir da data da transação. Essa organização física e lógica permite podas eficientes de partição em consultas analíticas e auditorias de conformidade, evitando varreduras completas no armazenamento bruto.

### Etapa 4: Camada Bronze (Limpeza e Saneamento)
A camada Bronze atuou como barreira de qualidade de dados. Foram implementadas validações para conferir unicidade de transação, assegurar valores monetários estritamente positivos e conferir se os scores de crédito estavam na faixa regulatória de 300 a 900. Todos os 30.000 registros atenderam aos critérios de qualidade, sendo promovidos integralmente para a camada seguinte.

### Etapa 5: Camada Silver (Enriquecimento de Negócio)
Na camada Silver, o conjunto de dados foi enriquecido com variáveis analíticas derivadas para subsidiar o diagnóstico de risco. Foram criadas a faixa de valor transacionado (segmentada em tíquetes baixos, médios, altos e críticos), a classificação do período do dia da operação (madrugada, manhã, tarde e noite) e uma marcação de alta suspeita combinando risco elevado com montantes expressivos. As dimensões de canal e categoria mercantil foram preservadas e integradas para viabilizar análises setoriais.

### Etapa 6: Camada Gold (Agregações para BI e Serving)
A camada Gold consolidou duas tabelas analíticas para consumo direto na Etapa 3. A primeira cruzou canal de atendimento com categoria mercantil, extraindo o volume transacionado, a quantidade absoluta de sinistros e a taxa percentual de fraude por setor. A segunda cruzou o perfil do cliente com o período do dia, evidenciando variações comportamentais e revelando picos críticos de fraude em horários de menor monitoramento (madrugadas).

---

## 2. Respostas às Perguntas do Enunciado

### Linhas que sobreviveram da camada Bronze em diante
Entraram no pipeline 30.000 registros e exatamente 30.000 registros sobreviveram até as camadas Silver e Gold. Nenhuma linha foi descartada porque a base não apresentou duplicatas de identificador, registros nulos ou valores impossíveis (como montantes negativos ou scores de crédito fora da faixa de 300 a 900).

### Uso das colunas channel e merchant_category na camada Silver
As colunas `channel` e `merchant_category` foram mantidas e utilizadas ativamente na camada Silver. Em análise de fraudes em pagamentos, essas variáveis são fundamentais para explicar a vulnerabilidade do negócio: descartá-las impediria a identificação de fraudes concentradas em canais digitais específicos (como app ou web) e estabelecimentos de liquidez rápida (como compras eletrônicas e varejo).

### Agregações criadas na camada Gold e utilidade na Etapa 3
Foram geradas duas visões agregadas na camada Gold:
* **Tabela Gold 1 (Canal e Categoria):** Consolida métricas de volume, tíquete médio e percentual de fraude por canal e ramo comercial. Fornece os indicadores para os gráficos de calor e dispersão no dashboard da Etapa 3, apontando quais frentes comerciais exigem reforço em travas de segurança.
* **Tabela Gold 2 (Segmento e Período do Dia):** Revela a distribuição de sinistros e score de crédito ao longo dos turnos diários. Aponta empiricamente que o segmento de alto risco atinge seu ápice de sinistralidade na madrugada (13,14% de fraudes contra 1,21% no perfil premium), servindo como base para as regras de negócio e acionamentos propostos no BI da Etapa 3.
