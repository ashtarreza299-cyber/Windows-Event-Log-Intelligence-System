
import sys
import os
import pandas as pd


# Add the project root to sys.path so we can import from sibling folders
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Now you can import db_connection
from db.db_connection import get_sqlalchemy_engine


def data_processing():
    
    # 1. Load data from database
    connection = get_sqlalchemy_engine()

    query = "SELECT * FROM EventLog"

    df = pd.read_sql(query, connection)

    # 2. Handle Missing Values
    df['UserName'] = df['UserName'].fillna("Unknown")
    df['Message'] = df['Message'].fillna("")
    df.dropna(subset=['EventID', 'TimeGenerated', 'EventType'], inplace=True)

    # 3. Convert Time Stamp
    df["TimeGenerated"] = pd.to_datetime(df["TimeGenerated"])

    return df

if __name__ == "__main__":

    data_processing()