FROM python:3.10.0

WORKDIR /InBot

COPY requirements.txt .
RUN pip install -Ur requirements.txt

COPY . .
CMD python3 /InBot/main.py
