FROM python:3.8.13-slim-buster

WORKDIR /app

COPY es_CO.aff /app/

COPY es_CO.dic /app/

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "Cipher_bot.py"]

