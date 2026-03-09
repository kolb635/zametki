# Жестко фиксируем 11-ю версию Debian (bullseye), чтобы драйверы MS SQL встали без ошибок
FROM python:3.10-slim-bullseye

# Установка системных утилит
RUN apt-get update && apt-get install -y curl apt-transport-https gnupg2 unixodbc-dev

# Добавление ключей и репозитория Microsoft для Debian 11
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

# Установка драйвера с автоматическим принятием лицензии (EULA)
RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Настройка рабочей директории и установка Python-библиотек
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Запуск сервера FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]