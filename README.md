
# FastAPI Solar Forecasting Backend

This project provides the main backend services for a solar energy forecasting platform, built with FastAPI and PostgreSQL.

> **Note:**  
> This repository is actively being developed as part of my personal learning.  
> For the version submitted for the final university project, please refer to commit [`514c445`](https://github.com/entl/evolyte-backend/tree/514c445be265d1cb040a724db322553006c8ff1b).


## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/entl/evolyte-ml-backend
cd evolyte-ml-backend
```

### 2. Create a virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install required dependencies

```bash
pip install -r requirements.txt
```
### 4. Create a .env file
Create a .env file in the project root directory and add the following environment variables:

```env
PG_DATABASE_HOSTNAME
PG_DATABASE_PORT
PG_DATABASE_PASSWORD
PG_DATABASE_NAME
PG_DATABASE_USERNAME

JWT_SECRET_KEY
JWT_ALGORITHM
jwt_token_expire_minutes

ML_API_URL

CORS_ORIGINS= (list format)
```

**Note:**  
- Update `PG_DATABASE_PASSWORD`, `PG_DATABASE_NAME`, and other variables if needed.
- Make sure your PostgreSQL server is running.

### 5. Apply database migrations

Run Alembic migrations to upgrade the database schema:

```bash
alembic upgrade head
```

### 6. Populate the database

After running the migrations, populate the `solar_panels` table by importing the provided CSV file into your PostgreSQL database.

The `solar_panels.csv` file is located in the project root directory.

Example command using `psql`:

```bash
psql -h <HOST> -U <USERNAME> -d <DATABASE> -c "\COPY solar_panels(column1, column2, ...) FROM './solar_panels.csv' DELIMITER ',' CSV HEADER;"
```

- Replace `<HOST>`, `<USERNAME>`, and `<DATABASE>` with your database details.
- Make sure the columns match your database schema.

Alternatively, you can use your preferred PostgreSQL client (like DBeaver, pgAdmin, etc.) to import the file.

### 7. Run the FastAPI ML service

```bash
uvicorn src.main:app --reload --port=8001
```

### 8. Access the API documentation

Once the server is running:

- Open **Swagger UI** (interactive API docs):  
  [http://localhost:8001/docs](http://localhost:8001/docs)

- Open **ReDoc** documentation (alternative style):  
  [http://localhost:8001/redoc](http://localhost:8001/redoc)
