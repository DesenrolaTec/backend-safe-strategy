# Usar a imagem base com Python 3.10 pré-instalado
FROM python:3.10-slim-bullseye

# Atualizar pacotes e instalar dependências essenciais
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    nginx \
    certbot \
    python3-certbot-nginx \
    default-libmysqlclient-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar dependências Python para Flask, Gunicorn e MySQL
RUN pip3 install --no-cache-dir \
    gunicorn==20.1.0 \
    flask==3.0.0 \
    mysql-connector-python \
    pymysql \
    gevent && \
    pip3 install --upgrade certbot certbot-nginx cryptography pyOpenSSL

# Renomear Gunicorn para gunicorn3
RUN mv /usr/local/bin/gunicorn /usr/local/bin/gunicorn3

# Copiar um script para adicionar o host e instalar o certificado
COPY /infra/local/scripts/domain.sh /usr/local/bin/domain.sh
RUN chmod +x /usr/local/bin/domain.sh
RUN /usr/local/bin/domain.sh

COPY /infra/local/scripts/start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Configurar o diretório de trabalho
WORKDIR /

# Criar diretórios necessários para o projeto Flask
RUN mkdir -p /var/www/backend /var/www/backend/static

# Copiar aplicação para o container
COPY . /var/www/backend
RUN pip3 install --no-cache-dir -r /var/www/backend/app/requirements.txt

COPY ./infra/local/services/options-ssl-nginx.conf /etc/letsencrypt/options-ssl-nginx.conf
COPY ./infra/local/services/ssl-dhparams.pem /etc/letsencrypt/ssl-dhparams.pem

# Copiar arquivos de configuração do Nginx
COPY ./infra/local/nginx/backend /etc/nginx/sites-available/backend
RUN ln -s /etc/nginx/sites-available/backend /etc/nginx/sites-enabled/backend


# Copiar arquivo de configuração do Gunicorn
COPY ./infra/local/services/gunicorn.py /etc/gunicorn.d/gunicorn.py


# Expor as portas necessárias
EXPOSE 80 443

# Configurar o CMD para iniciar Nginx e Gunicorn
CMD ["/bin/bash","-C","/usr/local/bin/start.sh"]
