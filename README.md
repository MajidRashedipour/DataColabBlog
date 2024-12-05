# DataColabBlog

## Run

<details>
  <summary>Click for run application details</summary>

1. Clone the repository and navigate to the project directory.

   ```
   git clone https://github.com/MajidRashedipour/DataColabBlog.git
   cd DataColabBlog
   ```

2. Setup environment.

   MacOS and Linux:
   ```
   cp .env.example .env
   nano .env
   ```

   Windows:
   ```
   copy .env.example .env
   ```
   
   then open `.env` file and change variables value

3. Create python environment and active it.

   MacOS and Linux:
   ```
   python3 -m venv .venv
   source ./.venv/bin/activate
   ```

   Windows:
   ```
   python -m venv .venv
   ./.venv/Scripts/activate
   ```

4. Install packages and migrate database.

   ```
   pip install -r requirements.txt
   mkdir ./app/migrations/versions
   alembic revision --autogenerate
   alembic upgrade head
   ```

5. Run application.

   ```
   fastapi run app/main.py
   ```

   then open api document on: http://127.0.0.0:8000/docs

## Run with Docker.

<details>
  <summary>Click for run application with docker details</summary>

1. Install docker.

   Download docker from https://www.docker.com and install.

   **OR**

   Install with commnad:

   Linux:

   ```
   apt update && apt upgrade -y
   apt install docker.io -y
   apt install docker-compose -y
   ```

2. Build the Docker container.

   ```
   docker-compose build
   ```

3. Run application.

   ```
   docker-compose up
   ```

   run in the background

   ```
   docker-compose up -d
   ```