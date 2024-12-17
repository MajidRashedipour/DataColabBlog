FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y netcat

COPY . .

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN chmod +x /app/entrypoint.sh

ENTRYPOINT [ "/app/entrypoint.sh" ]

CMD ["fastapi", "run", "/app/app/main.py", "--port", "80"]