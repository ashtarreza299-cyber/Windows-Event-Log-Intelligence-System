

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from data_preprocessing import data_processing
from sklearn.preprocessing import LabelEncoder

def encode_columns():

    # 1. Load the dataframe
    df = data_processing()

    # 2. Extranct time features
    df['Hour'] = df['TimeGenerated'].dt.hour
    df['DayOfWeek'] = df['TimeGenerated'].dt.day_of_week # 0: monday 6: Sunday
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    df['IsNightTime'] = df["Hour"].apply(lambda x: 1 if x < 6 & x >= 22 else 0)

    # 3. Encode Categorical Data

    le = LabelEncoder()

    df['ComputerName_enc'] = le.fit_transform(df['ComputerName'].astype(str))
    df['UserName_enc'] = le.fit_transform(df['UserName'].astype(str))
    df['SourceName_enc'] = le.fit_transform(df['SourceName'].astype(str))

    # 4. MESSAGE FEATURE: length and keyword

    df['MessageLength'] = df["Message"].apply(len)

    suspicious_keywords = ['failed', 'error', 'malware', 'denied', 'threat', 'unautherized', 'attack', 'brute', 'suspicious']

    df["HasSuspiciousKeyword"] = df["Message"].apply(lambda msg: 1 if any(kw in msg for kw in suspicious_keywords) else 0)

    return df


if __name__ == "__main__":

    encode_columns()