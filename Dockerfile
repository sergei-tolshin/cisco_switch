FROM python:3.10.2-alpine3.15

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt .

RUN pip install netports --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir

COPY ./src/ .

CMD ["python", "./main.py"]