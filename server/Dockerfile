# Выкачиваем из dockerhub образ с python версии 3.9
FROM ubuntu:20.04
# Устанавливаем рабочую директорию для проекта в контейнере
RUN apt-get update && apt-get install -y python3-pip
WORKDIR /server
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY ./server/requirements.txt /server
RUN pip3 install --upgrade pip -r requirements.txt
# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . /server