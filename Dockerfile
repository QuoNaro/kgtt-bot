### BUILD STAGE
FROM python:3.11.7-alpine as builder

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# Копируем локальные пакеты Python и зависимости для проекта
COPY ./source/packages ./packages/
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt


### INSTALL STAGE 
FROM python:3.11.7-alpine

ARG NAME
ENV NAME=${NAME}

# Создаем и устанавливаем рабочую директорию
WORKDIR /app

#Устанавливаем зависимости
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Копируем проект в образ
COPY ./source/services/$NAME/ .

# Токен для бота
ENV TOKEN=vk1.a.gkzceCkCbU-0fcihGLpsxKZfei8iMR9ZmjuWFJXgHCkVVO5SbdA3CmpBVCoOBnUUedGfzqv6Xz9B7r4TEj_OdXW8x4mLRJXqgXj-f-VCSbfXsmJRFqn0k90LZRQkM7gK9_l0pdBsgOxyrAG2XSAFy-nSI1a7R1mQwmz5lblR_XeOC7cBjCYqwW3XWr3TzfSdnUBLfjCGXlChTURSXPI3rw
