FROM --platform=linux/amd64 python:3.11.6-buster as build

WORKDIR /app

COPY requirements.txt .

RUN apt update
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]