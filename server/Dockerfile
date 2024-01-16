# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.10
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /server
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY ./server/requirements.txt /server
RUN pip3 install --upgrade pip -r requirements.txt
# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . /server