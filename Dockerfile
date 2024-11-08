
FROM python:3.12.3-slim
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
ENV FLASK_APP=wsgi.py

EXPOSE 7400
CMD ["python", "src/Application.py"]
