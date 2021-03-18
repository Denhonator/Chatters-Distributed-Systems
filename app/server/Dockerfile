FROM python:3.9.2-alpine3.13

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 7500/udp
EXPOSE 7500/tcp

ENTRYPOINT ["python3", "main.py"]
