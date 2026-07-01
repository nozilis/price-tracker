FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

ARG SECRET_KEY=dummy-secret-key-for-build
ARG DB_HOST=localhost
ARG DB_PORT=5432
ARG DB_NAME=dummy
ARG DB_USER=dummy
ARG DB_PASSWORD=dummy

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]