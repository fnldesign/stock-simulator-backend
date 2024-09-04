# Use uma imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o arquivo de requisitos para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todos os arquivos da aplicação para o diretório de trabalho
COPY . .

# Exponha a porta que o Flask usará
EXPOSE 5000

# Defina a variável de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV FLASK_DEBUG=True

# Comando para rodar o servidor Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
