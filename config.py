from sqlalchemy import create_engine

DB_URL = "postgresql://postgres:postgres@localhost:5432/biteback_analytics"
engine = create_engine(DB_URL)

API_BASE_URL = "http://127.0.0.1:8000"