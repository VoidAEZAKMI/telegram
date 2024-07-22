FROM python:3.8-slim

# Обновляем pip
RUN pip install --upgrade pip

# Копируем файл requirements.txt и устанавливаем зависимости
COPY ./app/requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Копируем файл bot.py в контейнер
COPY ./app/bot.py /app/bot.py

# Устанавливаем рабочую директорию
WORKDIR /app

# Запускаем bot.py
CMD ["python", "bot.py"]