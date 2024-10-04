FROM ubuntu:20.04 as SSLBuilder
    USER root
    RUN apt-get update && apt-get install -y openssl --no-install-recommends
    RUN mkdir -p /etc/ssl/certs
    RUN openssl req -newkey rsa:2048 -x509 -nodes -keyout /etc/ssl/certs/privat.key -out /etc/ssl/certs/app.crt -days 365 -subj "/C=US/ST=State/L=Locality/O=event/CN=controle-interno.com"
    
FROM python:3.12.3-slim

    RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

    COPY --from=SSLBuilder /etc/ssl/certs/privat.key /etc/ssl/certs/privat.key
    COPY --from=SSLBuilder /etc/ssl/certs/app.crt /etc/ssl/certs/app.crt

    WORKDIR /app

    COPY requirements.txt .

    RUN pip install -r requirements.txt

    COPY . .

    ENV PYTHONPATH=/app/src

    CMD ["gunicorn", "-c", "gunicorn_config.py", "src.application:app"]