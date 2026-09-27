
import pyodbc as db


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

    return db.connect(connection_string)