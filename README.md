
# FastAPI Solar Forecasting Backend

This project provides the main backend services for a solar energy forecasting platform, built with FastAPI and PostgreSQL.

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://your-repo-url.git
cd your-repo-folder
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

### 4. Create a `.env` file

Create a `.env` file in the project root directory and add the following environment variables:

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

### 5. Run the FastAPI application

```bash
uvicorn src.main:app --reload --port=8001
```

### 6. Access the API documentation

Once the server is running locally:

- Open **Swagger UI** (Interactive API docs):  
  [http://localhost:8000/docs](http://localhost:8000/docs)

- Open **ReDoc** documentation (alternative style):  
  [http://localhost:8000/redoc](http://localhost:8000/redoc)
