FROM python:3.9-slim

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создание и переход в рабочую директорию
WORKDIR /app

# Копирование requirements.txt
COPY requirements.txt .

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove build-essential && \
    rm -rf /var/lib/apt/lists/*

# Копирование остальных файлов
COPY . .

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]