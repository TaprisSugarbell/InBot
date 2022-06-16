FROM python:3.10.0

WORKDIR /InBot

COPY requirements.txt .
RUN pip install -Ur requirements.txt

COPY . .
CMD ls
CMD python InBot/InBot/main.py
