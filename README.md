# DataColabBlog

## Run

1. Clone the repository.

   ```
   git clone https://github.com/MajidRashedipour/DataColabBlog.git
   ```

2. Navigate to the project directory.

   ```
   cd DataColabBlog
   ```

3. Setup environment.

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

4. Create python environment and activate.

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

5. Install packages.

   ```
   pip install -r requirements.txt
   ```

6. Run this command for database migrations

   ```
   alembic revision --autogenerate
   alembic upgrade head
   ```

7. Run application.

   ```
   fastapi run app/main.py
   ```

7. Open api document on: (http://127.0.0.0:8000/docs)

## Run with Docker.

1. Install docker.

   Download docker from (https://www.docker.com) and install.

   **OR**

   Install with commnad:

   Linux:

   ```
   apt update && apt upgrade -y
   apt install docker.io -y
   apt install docker-compose -y
   ```

2. Build the Docker containers.

   ```
   docker-compose build
   ```

3. Run application.

   ```
   docker-compose up
   ```

   on background

   ```
   docker-compose up -d
   ```