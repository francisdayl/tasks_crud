FROM --platform=linux/amd64 python:3.11.6-buster as build

WORKDIR /app

COPY requirements.txt .

RUN apt update
RUN apt-get install -y poppler-utils
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "app.py"]