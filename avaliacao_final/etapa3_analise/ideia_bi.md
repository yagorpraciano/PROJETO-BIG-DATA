# Descrição da Ideia do BI (Etapa 3)

Conforme exigido pelos critérios de avaliação do projeto, detalhamos abaixo a concepção do Dashboard de Risco da TechPay como um produto de dados:

**1. Para quem é esse dashboard?**
O painel foi desenhado para a **Equipe de Prevenção a Fraudes (Risk & Compliance)** na linha de frente analítica, e para a **Diretoria de Operações** que acompanha o impacto financeiro macro.

**2. Que decisão ele ajuda a tomar?**
Ele direciona a tomada de decisão sobre **calibragem do motor de regras**. Ao ver que fraudes estão disparando na Web ou em Eletrônicos, a equipe pode decidir aumentar a fricção (exigir 2FA/token) ou reduzir limites de aprovação automática instantaneamente para esses nichos.

**3. Por que esses KPIs e não outros?**
Selecionamos *Valor Total Fraudado*, *Transações Suspeitas* e *Risco Médio* porque eles representam o **dano financeiro direto** e a saúde da carteira. Descartamos KPIs puramente técnicos (como latência de aprovação ou uptime) ou demográficos (idade do cliente), pois não são acionáveis no curtíssimo prazo para barrar um ataque em andamento.

**4. Quem seria o dono desse painel?**
O dono (Product Owner / Sponsor) seria o **Gerente de Risco (Fraud Manager)**. Ele seria responsável por acompanhar esses indicadores diariamente/semanalmente e coordenar com o time de Engenharia as alterações sistêmicas necessárias para estancar perdas.
