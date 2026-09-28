
import pyodbc as db
from sqlalchemy import create_engine

SERVER = 'localhost,1533'
DATABASE = 'WindowsLogIntelligence'
USERNAME = 'sa'
PASSWORD = '0000'

connection_string = (

    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"UID={USERNAME};"
    f"PWD={PASSWORD};"
    f"TrustServerCertificate=yes;" # Crucial for Driver 18 to avoid SSL errors
)

def connect_db():
    """Returns a raw pyodbc connection (for store_events.py)"""
    return db.connect(connection_string)

def get_sqlalchemy_engine():
    """Returns a SQLAlchemy engine (for Pandas data_preprocessing.py)"""
    # SQLAlchemy connection string format: mssql+pyodbc://user:pass@host:port/db?driver=...
    engine_string = f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
    return create_engine(engine_string)