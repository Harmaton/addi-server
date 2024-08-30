FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

ARG API_URL
ENV API_URL=$API_URL

ARG BUCKET_NAME
ENV BUCKET_NAME=$BUCKET_NAME
ARG PROJECT_ID
ENV PROJECT_ID=$PROJECT_ID

# Install gunicorn
RUN pip install gunicorn

# Use gunicorn to run the app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 run:app