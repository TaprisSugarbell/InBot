FROM python:3.10.0
RUN apk add --no-cache \
    zlib-dev \
    ffmpeg

WORKDIR /InBot

COPY requirements.txt .
RUN pip install -Ur requirements.txt

COPY . .
CMD python InBot/main.py
