# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY requirements.txt ./
COPY app/ ./app/
COPY test.db ./
COPY . .

# Устанавливаем зависимости
RUN pip install --upgrade --no-cache-dir -r requirements.txt

# Указываем команду для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
