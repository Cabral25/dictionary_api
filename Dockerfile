FROM python:3.12-slim

# VARIÁVEIS DE AMBIENTE DO PYTHON


# Python não irá tentar escrever arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Desativa o buffer de saída do python, ou seja,
# o python imprime tudo em tempo real. Sem essa
# variável, logs podem demorar a aparecer no terminal,
# pois normalmente o python não os envia imediatamente,
# ele guarda temporariamente na memória e solta em blocos.
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1


# Se /dictionary_api não existir, o docker cria
# Define /dictionary_api como diretório atual
# É equivalente a mkdir /dictionary_api | cd /dictionary_api
WORKDIR /dictionary_api


# Instala dependências
# COPY <origem> <destino> -->  COPY <requirements.txt> <.>
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Faz uma cópia do diretório no meu computador dentro do diretório principal da imagem do container
# COPY <origem> <destino> --> COPY <dictionary_api/> </dictionary_api>
COPY . .


CMD [ "uvicorn", "main:app", "--reload", "--port", "8003" ]