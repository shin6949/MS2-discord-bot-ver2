FROM python:3.6.15-slim-buster
LABEL org.opencontainers.image.source='https://github.com/shin6949/MS2-discord-bot-ver2'
COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "discord_bot_ver2.py"]