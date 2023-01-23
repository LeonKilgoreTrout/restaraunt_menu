FROM python:3.10-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app_tests
COPY ./app_tests/requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt
COPY ./app_tests ./app_tests
COPY ./app ./app
ADD ../.env .
EXPOSE 8000
CMD ["pytest", "-v"]
