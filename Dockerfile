FROM python:3.6.14-buster
MAINTAINER COCOBLUE "cocoblue@kakao.com"
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install libgl1-mesa-glx -y
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["discord_bot_ver2.py"]