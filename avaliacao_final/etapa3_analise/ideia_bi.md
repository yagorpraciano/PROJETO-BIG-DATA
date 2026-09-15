# Descrição da Ideia do BI (Etapa 3)

Neste documento, explicamos a ideia por trás do Dashboard de Risco da TechPay e como ele deve ser usado na prática pelo negócio:

**1. Para quem é esse dashboard?**
O painel foi pensado para a equipe de Prevenção a Fraudes, que atua na linha de frente analisando os alertas, e também para a Diretoria de Operações acompanhar o impacto financeiro geral.

**2. Que decisão ele ajuda a tomar?**
Ele ajuda a equipe a calibrar o motor de regras. Por exemplo, se o dashboard mostrar que as fraudes estão disparando no canal Web ou em compras de Eletrônicos, a equipe pode agir rápido e exigir autenticação em dois fatores (2FA) ou baixar os limites de aprovação automática para essas transações.

**3. Por que esses KPIs e não outros?**
Nós escolhemos mostrar o Valor Total Fraudado, as Transações Suspeitas e o Risco Médio porque esses números mostram o prejuízo real e a saúde do negócio. Deixamos de lado métricas de infraestrutura (como tempo de resposta do sistema) ou dados genéricos do cliente, porque eles não ajudam a barrar um ataque na hora que ele está acontecendo.

**4. Quem seria o dono desse painel?**
O "dono" do painel seria o Gerente de Risco. É ele quem vai olhar esses números todo dia ou toda semana e pedir para o time de Engenharia ajustar o sistema sempre que for necessário para evitar mais perdas.
