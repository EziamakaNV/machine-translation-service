FROM python:3.6

RUN sudo apt-get update && sudo apt-get install espeak ffmpeg libespeak1

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app

CMD python app.py