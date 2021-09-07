FROM python:3.6.14-buster
RUN apt-get update && apt-get upgrade -y && apt-get install libgl1-mesa-glx -y
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
CMD python3 -u discord_bot_ver2.py