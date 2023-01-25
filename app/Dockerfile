FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt
COPY ./app ./app
ADD ./alembic ./alembic
ADD ./alembic.ini .
ADD ./.env .
EXPOSE 8080
