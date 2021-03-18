FROM python:3.9.2-alpine3.13

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 7500/udp
EXPOSE 7500/tcp

EXPOSE 7501/udp
EXPOSE 7501/tcp

EXPOSE 7502/udp
EXPOSE 7502/tcp

EXPOSE 7503/udp
EXPOSE 7503/tcp


ENTRYPOINT ["python3", "main.py"]
