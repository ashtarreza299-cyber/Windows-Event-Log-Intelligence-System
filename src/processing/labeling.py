

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from processing.data_preprocessing import data_processing
from sklearn.preprocessing import LabelEncoder

def encode_columns():

    # 1. Load the dataframe
    df = data_processing()

    # 2. Extranct time features
    df['Hour'] = df['TimeGenerated'].dt.hour
    df['DayOfWeek'] = df['TimeGenerated'].dt.dayofweek # 0: monday 6: Sunday
    df['IsWeekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    df['IsNightTime'] = df["Hour"].apply(lambda x: 1 if x < 6 or x >= 22 else 0)

    # 3. Encode Categorical Data


    df['ComputerName_enc'] = LabelEncoder().fit_transform(df['ComputerName'].astype('str'))
    df['UserName_enc'] = LabelEncoder().fit_transform(df['UserName'].astype(str))
    df['SourceName_enc'] = LabelEncoder().fit_transform(df['SourceName'].astype(str))

    # 4. MESSAGE FEATURE: length and keyword

    df['Message'] = df['Message'].fillna("")
    df['MessageLength'] = df["Message"].apply(len)

    suspicious_keywords = ['failed', 'error', 'malware', 'denied', 'threat', 'unauthorized', 'attack', 'brute', 'suspicious']

    df["HasSuspiciousKeyword"] = df["Message"].apply(lambda msg: 1 if any(kw in msg.lower() for kw in suspicious_keywords) else 0)

    # 5. Labeling Events

    df['Label'] = df.apply(label_event, axis = 1)

    return df

def label_event(row):

    # Event type meaning in windows
    # 1 = error
    # 2 = Warning
    # 3 = Information
    # 4 = Security Audit Success
    # 5 = Security Audit Failure

    # Specific condition MUST come before the general condition!
    if row['EventType'] == 5 and row['IsNightTime'] == 1:
        return 4  # Assuming night-time failures are the MOST suspicious (Level 4)
        
    if row['EventType'] == 5:
        return 3  # Standard Audit Failure
        
    if row['EventType'] in [1, 2]:
        return 2  # Errors and Warnings
        
    if row['HasSuspiciousKeyword'] == 1:
        return 1  # Suspicious text in an otherwise normal even

    # default return value for normal events
    return 0 


if __name__ == "__main__":

    df = encode_columns()