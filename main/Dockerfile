FROM python:3.13-slim

WORKDIR /app

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Копирование requirements
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Открытие порта
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]