FROM python:3.12.3

RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-dev \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app/src

CMD ["gunicorn", "-c", "gunicorn_config.py", "src.application:app"]