FROM python:3.10.0

WORKDIR /InBot

COPY requirements.txt .
RUN pip install -r requirements.txt

CMD python /InBot/main.py
