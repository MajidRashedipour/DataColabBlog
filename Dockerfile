FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt 

COPY . .

RUN mkdir ./app/migrations/versions
RUN alembic revision --autogenerate
RUN alembic upgrade head

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]