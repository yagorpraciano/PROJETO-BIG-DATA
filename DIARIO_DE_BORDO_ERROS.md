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
```
* Solução de Contorno: Seguimos a recomendação do próprio erro e criamos um ambiente virtual isolado. Rodamos python3 -m venv venv e, toda vez que abríamos o terminal, ativávamos o ambiente com source venv/bin/activate. Após isso, o pip install fluiu perfeitamente.

## 2. Bloqueio do Ubuntu ao instalar Python (Etapa 3)
* O Problema: Ao rodar pip install pyspark, o sistema baixou a última versão do motor. Na hora de rodar o Machine Learning, o terminal estourou um erro de incompatibilidade de versão do Java e abortou a execução. Log de Erro Capturado:
  ```text
  Iniciando o cluster local do Spark...Error: A JNI error has occurred, please check your installation and try againException in thread "main" java.lang.UnsupportedClassVersionError: org/apache/spark/launcher/Main has been compiled by a more recent version of the Java Runtime (class file version 61.0), this version of the Java Runtime only recognizes class file versions up to 52.0
  ```
  * Solução de Contorno: Lendo o log, notamos que o PySpark novo exigia o Java 17 (versão 61.0), mas nosso Hadoop e Hive estavam rodando no Java 8 (versão 52.0). Para não quebrar o Data Lake atualizando o Java da máquina inteira, a solução de contorno foi fazer o downgrade do Spark. Desinstalamos a versão nova e rodamos pip install pyspark==3.5.1, que é 100% compatível com o Java 8.

## 3. Conflito de sincronização no Git (Documentação)
* O Problema: Apagamos um arquivo de rascunho direto pelo site do GitHub. Quando fomos usar o terminal para enviar a versão final (git push), o Git rejeitou o envio alegando dessincronia. Log de Erro Capturado:
 ```text
To https://github.com/.../PROJETO-BIG-DATA.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to 'https://github.com/.../PROJETO-BIG-DATA.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally.
  ```
* Solução de Contorno: Solução de Contorno: Como o repositório local não "sabia" da exclusão feita na nuvem, forçamos a mesclagem rodando git pull origin main --no-edit. Isso sincronizou as duas pontas e permitiu que o git push origin main final funcionasse de primeira.
