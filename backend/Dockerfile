FROM python:3.10
ENV PYTHONUNBUFFERED 1
WORKDIR /app/api

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY . ./

EXPOSE 8000
