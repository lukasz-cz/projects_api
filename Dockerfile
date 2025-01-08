FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY projects_api projects_api
COPY config config

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=projects_api
ENV FLASK_ENV=development
ENV CONFIG_PATH=config/development.yaml

CMD ["flask", "run", "--host=0.0.0.0"]
