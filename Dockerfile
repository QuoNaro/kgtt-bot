# Используйте официальный образ Python
FROM python:3.11.7-alpine
ARG NAME
ENV NAME=${NAME}

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создаем и устанавливаем рабочую директорию
WORKDIR /app

# Копируем проект в образ
COPY ./source/services/$NAME/ .

# Копируем локальные пакеты Python
COPY ./source/packages ./packages/
COPY ./requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

ENV TOKEN=vk1.a.gkzceCkCbU-0fcihGLpsxKZfei8iMR9ZmjuWFJXgHCkVVO5SbdA3CmpBVCoOBnUUedGfzqv6Xz9B7r4TEj_OdXW8x4mLRJXqgXj-f-VCSbfXsmJRFqn0k90LZRQkM7gK9_l0pdBsgOxyrAG2XSAFy-nSI1a7R1mQwmz5lblR_XeOC7cBjCYqwW3XWr3TzfSdnUBLfjCGXlChTURSXPI3rw