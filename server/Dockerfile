FROM python:bullseye

RUN apt-get update -y
RUN apt-get upgrade -y
RUN pip install pip -U

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}
