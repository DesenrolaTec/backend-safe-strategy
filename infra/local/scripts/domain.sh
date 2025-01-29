#!/bin/bash

# Adicionar entrada ao /etc/hosts para o domínio local
echo "127.0.0.1 api-local.safestrategy.com.br" >> /etc/hosts
echo "::1 api-local.safestrategy.com.br" >> /etc/hosts

# Iniciar o serviço Nginx temporariamente para o Certbot
service nginx start

# Instalar o certificado SSL com o Certbot
# certbot certonly --standalone --http-01-port 8081 -d api-local.safestrategy.com.br --register-unsafely-without-email --agree-tos
mkdir -p /etc/letsencrypt/live/api-local.safestrategy.com.br

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/letsencrypt/live/api-local.safestrategy.com.br/privkey.pem \
    -out /etc/letsencrypt/live/api-local.safestrategy.com.br/fullchain.pem \
    -subj "/CN=api-local.safestrategy.com.br"

# Parar o serviço Nginx após instalar o certificado
service nginx stop

# Reiniciar o Nginx e iniciar o container
service nginx start