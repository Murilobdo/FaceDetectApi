FROM python:3.12.3

RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7000


# Comando para rodar a aplicação Flask
CMD ["python", "./src/Application.py"]