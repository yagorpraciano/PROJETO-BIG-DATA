# Relatório de Achados e Análises (Etapa 3)

Com base nas agregações da camada Gold e visualizações do Dashboard, aplicamos o framework estratégico para traduzir dados em ações de negócio focadas na mitigação de risco.

## Análise 1: Risco por Canal e Segmento
* **Finding (Achado):** O cruzamento de dados no painel revela que o maior volume financeiro fraudado se concentra no canal `Web`, com forte impacto no segmento `Premium`.
* **Insight (Entendimento):** Isso indica que os fraudadores estão focando em contas com limites altos (Premium) explorando vulnerabilidades específicas de navegadores (como phishing ou roubo de sessão/cookies), onde a fricção de segurança é menor do que no aplicativo mobile (que costuma exigir biometria ou token atrelado ao aparelho).
* **Ação (O que fazer):** A área de risco deve implementar imediatamente o bloqueio preventivo e a exigência de Autenticação Multifator (MFA) rigorosa via aplicativo móvel para todas as transações `Web` do segmento `Premium` que ultrapassem a média histórica de gastos do cliente.

## Análise 2: Risco por Categoria de Estabelecimento
* **Finding (Achado):** A visualização de Score de Risco Médio aponta a categoria `Eletrônicos` no topo do ranking de transações suspeitas, destoando fortemente de categorias como `Alimentação` ou `Saúde`.
* **Insight (Entendimento):** Produtos eletrônicos possuem alto valor agregado e extrema facilidade de revenda no mercado paralelo. Eles são o vetor clássico de "cash-out" (transformar o limite roubado em dinheiro real) após o comprometimento de uma conta.
* **Ação (O que fazer):** A equipe de engenharia do motor de regras deve reduzir o teto de aprovação automática e adicionar uma etapa de checagem humana (fricção alta) especificamente para compras na categoria `Eletrônicos`, caso a conta do usuário tenha registrado troca recente de senha ou de dispositivo (device ID).
