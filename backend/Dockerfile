FROM python:3.12-slim

WORKDIR /fastapi

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8000
EXPOSE 5432
