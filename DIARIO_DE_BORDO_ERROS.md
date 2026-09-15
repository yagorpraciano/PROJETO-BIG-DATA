# 📓 Diário de Bordo e Solução de Problemas

Como montamos toda a nossa infraestrutura de Big Data do zero rodando no WSL (Ubuntu Linux), nós esbarramos em alguns problemas bem reais de ambiente durante o projeto. 

Resolvemos criar este Diário de Bordo para documentar os principais erros (com os logs reais que o terminal nos retornou) e explicar como conseguimos contornar cada um deles sem quebrar o nosso Data Lake.

---

## 1. Bloqueio do Ubuntu ao instalar Python (Etapa 3)
* **O Problema:** Quando fomos instalar as bibliotecas do dashboard (`pandas` e `plotly`), o Ubuntu simplesmente bloqueou o comando `pip install`. Descobrimos que as versões mais novas do Linux bloqueiam instalações globais para não corromper pacotes do próprio sistema.
* **Log de Erro que recebemos:**
```text
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.

    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
* **Como nós resolvemos: Seguimos a recomendação do próprio erro e criamos um ambiente virtual isolado só para o nosso projeto. Toda vez que abríamos o terminal, rodávamos source venv/bin/activate. Depois disso, o pip install funcionou perfeitamente.
