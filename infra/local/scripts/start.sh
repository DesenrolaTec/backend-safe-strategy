#!/bin/bash

# Reiniciar o Nginx e iniciar o container
service nginx reload
service nginx start
cd /var/www/backend
gunicorn3 --name=backend --pythonpath=/var/www/backend/app --bind unix:/var/www/backend/gunicorn.socket --config /etc/gunicorn.d/gunicorn.py --certfile=/etc/letsencrypt/live/api-local.safestrategy.com.br/fullchain.pem --keyfile=/etc/letsencrypt/live/api-local.safestrategy.com.br/privkey.pem -b 0.0.0.0:8081 wsgi:app