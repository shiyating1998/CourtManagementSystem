FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn courtManagementSystem.wsgi:application --bind 0.0.0.0:$PORT