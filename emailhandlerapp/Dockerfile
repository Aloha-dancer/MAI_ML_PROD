# Выкачиваем из dockerhub образ с python версии 3.9
FROM python:3.10
# Устанавливаем рабочую директорию для проекта в контейнере
WORKDIR /emailhandlerapp
# Скачиваем/обновляем необходимые библиотеки для проекта 
COPY ./emailhandlerapp/requirements.txt /emailhandlerapp
RUN pip3 install --upgrade pip -r requirements.txt
# |ВАЖНЫЙ МОМЕНТ| копируем содержимое папки, где находится Dockerfile, 
# в рабочую директорию контейнера
COPY . /emailhandlerapp