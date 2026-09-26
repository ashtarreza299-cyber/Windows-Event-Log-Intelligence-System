# Windows Event Log Intelligence System

A Python-based machine learning project for **collecting, storing, analyzing, and classifying Windows Event Logs**.

The project combines **Windows Event Logs, Python, Microsoft SQL Server, Pandas, and Machine Learning** to build a pipeline that can eventually identify unusual or suspicious Windows activity.

> 🚧 **Project Status:** In Development

---

## 📌 Overview

Windows continuously generates events related to system activity, applications, security, services, errors, and user actions.

Examples include:

* System events
* Application errors
* Login attempts
* Failed authentication
* Service failures
* Windows Defender events
* PowerShell activity
* Driver and hardware events

This project collects those events from Windows, stores them in **Microsoft SQL Server**, processes them with **Pandas**, and uses machine learning to classify events.

### Project Pipeline

```text
Windows Event Logs
        │
        ▼
Python Event Collector
        │
        ▼
Microsoft SQL Server
        │
        ▼
Pandas / Data Processing
        │
        ▼
Feature Engineering
        │
        ▼
Machine Learning Model
        │
        ▼
Prediction & Evaluation
        │
        ▼
Streamlit Dashboard
```

---

# 🎯 Project Objectives

The main objectives of this project are:

1. Collect Windows Event Logs using Python.
2. Store collected events in Microsoft SQL Server.
3. Retrieve event data using Pandas.
4. Clean and preprocess the collected data.
5. Extract useful features from Windows events.
6. Create labels for machine learning.
7. Train a classification model.
8. Evaluate model performance.
9. Detect potentially suspicious events.
10. Visualize event activity through a dashboard.

---

# 🛠️ Technologies

| Technology               | Purpose                      |
| ------------------------ | ---------------------------- |
| **Python**               | Main programming language    |
| **PyWin32**              | Access Windows Event Logs    |
| **Microsoft SQL Server** | Store collected events       |
| **PyODBC**               | Connect Python to SQL Server |
| **Pandas**               | Data processing and analysis |
| **NumPy**                | Numerical operations         |
| **Scikit-learn**         | Machine learning             |
| **Matplotlib**           | Data visualization           |
| **Streamlit**            | Interactive dashboard        |

---

# 📂 Project Structure

The project can be organized as follows:

```text
Windows-Event-ML/
│
├── collector/
│   └── event_collector.py
│
├── database/
│   ├── database.py
│   └── schema.sql
│
├── data/
│   └── README.md
│
├── preprocessing/
│   └── preprocessing.py
│
├── model/
│   ├── train.py
│   ├── predict.py
│   └── evaluate.py
│
├── dashboard/
│   └── app.py
│
├── notebooks/
│   └── analysis.ipynb
│
├── requirements.txt
│
└── README.md
```

---

# 1. 📥 Collect Windows Events

Windows stores system information in the **Windows Event Log**.

Python can access these logs using the `pywin32` package.

## Installation

```bash
pip install pywin32
```

## Basic Event Collector

```python
import win32evtlog

server = "localhost"
log_type = "System"

hand = win32evtlog.OpenEventLog(server, log_type)

flags = (
    win32evtlog.EVENTLOG_BACKWARDS_READ
    | win32evtlog.EVENTLOG_SEQUENTIAL_READ
)

events = win32evtlog.ReadEventLog(hand, flags, 0)

for event in events:
    print(event.EventID)
    print(event.SourceName)
    print(event.TimeGenerated)
```

### What does `log_type = "System"` mean?

Windows has multiple Event Logs.

For example:

```python
log_type = "System"
```

means that the program is reading the **System Event Log**.

Other logs include:

```text
System
Application
Security
Setup
```

The project can initially focus on one log and later expand to additional Windows logs.

---

# 2. 🗄️ Store Events in SQL Server

The collected events need to be stored somewhere so that they can be analyzed later.

This project uses **Microsoft SQL Server** as the database.

SQL Server is useful because it provides:

* Structured storage
* SQL querying
* Indexing
* Filtering
* Aggregation
* Integration with Python
* A good foundation for larger datasets

## Example Database Table

```sql
CREATE TABLE WindowsEvents (
    EventID INT,
    SourceName VARCHAR(255),
    EventType INT,
    TimeGenerated DATETIME,
    ComputerName VARCHAR(255)
);
```

The schema can be expanded as more useful event information is identified.

---

# 3. 🔌 Connect Python to SQL Server

Install the Python SQL Server driver:

```bash
pip install pyodbc
```

Example connection:

```python
import pyodbc

conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=localhost;"
    "DATABASE=WindowsLogs;"
    "Trusted_Connection=yes;"
)

cursor = conn.cursor()
```

---

# 4. 💾 Insert Events into SQL Server

After collecting an event, its information can be inserted into the database.

```python
cursor.execute(
    """
    INSERT INTO WindowsEvents
    (EventID, SourceName, TimeGenerated)
    VALUES (?, ?, ?)
    """,
    event_id,
    source_name,
    time_generated
)

conn.commit()
```

For a production version, the collector should also handle:

* Duplicate events
* Connection failures
* Missing fields
* Database errors
* Large numbers of events

---

# 5. 🐼 Load Data with Pandas

Once events are stored in SQL Server, Pandas can be used to retrieve and analyze them.

Install Pandas:

```bash
pip install pandas
```

Example:

```python
import pandas as pd

query = """
SELECT *
FROM WindowsEvents
"""

df = pd.read_sql(query, conn)

print(df.head())
```

The result becomes a Pandas DataFrame:

```text
   EventID          SourceName       TimeGenerated
0     1000  Application Error   ...
1     4625  Microsoft Windows   ...
2     7036  Service Control...  ...
```

---

# 6. 🧹 Data Cleaning & Preprocessing

Raw Windows events are not immediately suitable for machine learning.

The data needs to be cleaned and transformed.

For example, timestamps can be converted using:

```python
df["TimeGenerated"] = pd.to_datetime(
    df["TimeGenerated"]
)
```

Useful time-based features can then be extracted:

```python
df["Hour"] = df["TimeGenerated"].dt.hour
df["Day"] = df["TimeGenerated"].dt.day
df["Month"] = df["TimeGenerated"].dt.month
df["DayOfWeek"] = df["TimeGenerated"].dt.dayofweek
```

These features allow the model to work with numerical information extracted from event timestamps.

---

# 7. 🏷️ Create Machine Learning Labels

A supervised machine learning model needs labeled data.

For example:

| Event ID | Description                     | Label |
| -------: | ------------------------------- | ----: |
|     4624 | Successful logon                |     0 |
|     4625 | Failed logon                    |     1 |
|     7031 | Service terminated unexpectedly |     1 |
|     1000 | Application error               |     1 |

A simple initial labeling strategy could be:

```python
if event_id == 4625:
    label = 1
else:
    label = 0
```

Where:

```text
0 = Normal
1 = Suspicious
```

### ⚠️ Important

These labels are only an initial example.

An event being associated with an error or failed login does **not automatically mean malicious activity**.

As the project develops, the labeling strategy should become more carefully defined and validated.

---

# 8. 🤖 Train a Machine Learning Model

The first machine learning model for this project can be **Logistic Regression**.

Install Scikit-learn:

```bash
pip install scikit-learn
```

Example:

```python
from sklearn.linear_model import LogisticRegression

model = LogisticRegression()

model.fit(X_train, y_train)
```

The model can then make predictions:

```python
prediction = model.predict(X_test)
```

Example concept:

```text
Event ID: 4625
Hour: 03
Day: 6

Prediction:
Suspicious
```

The model should be evaluated using appropriate metrics rather than relying only on accuracy.

---

# 9. 📊 Evaluate the Model

Example:

```python
from sklearn.metrics import accuracy_score

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("Accuracy:", accuracy)
```

Additional metrics are useful for classification problems:

```python
from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

print(classification_report(y_test, predictions))

print(confusion_matrix(y_test, predictions))
```

Potential evaluation metrics include:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

For security-related classification, **precision and recall can be particularly important**, because false positives and false negatives have different consequences.

---

# 10. 📈 Data Visualization

Before relying on machine learning, the collected events should be explored visually.

Matplotlib can be used to analyze patterns.

Example:

```python
import matplotlib.pyplot as plt

df.groupby("Hour").size().plot()

plt.xlabel("Hour")
plt.ylabel("Number of Events")
plt.title("Windows Events by Hour")

plt.show()
```

Possible visualizations include:

* Events per hour
* Events per day
* Events by Event ID
* Events by source
* Error frequency
* Failed login frequency
* Model predictions

---

# 11. 🖥️ Build a Dashboard

The final stage can include an interactive dashboard using **Streamlit**.

Install Streamlit:

```bash
pip install streamlit
```

Example:

```python
import streamlit as st

st.title("Windows Event ML")

st.metric(
    "Total Events",
    len(df)
)

st.line_chart(
    df.groupby("Hour").size()
)
```

The dashboard can eventually display:

```text
┌──────────────────────────────────────┐
│         Windows Event ML             │
├──────────────┬──────────────┬────────┤
│ Total Events │ Errors       │ Alerts │
│    125,430   │    2,351     │  483   │
├──────────────┴──────────────┴────────┤
│                                      │
│       Events Over Time               │
│          📈 Chart                    │
│                                      │
├──────────────────────────────────────┤
│ Event ID     Prediction              │
│ 4624         Normal                  │
│ 4625         Suspicious              │
│ 7036         Normal                  │
└──────────────────────────────────────┘
```

---

# 🔄 Complete Data Pipeline

The complete system can eventually work like this:

```text
┌─────────────────────┐
│   Windows Machine   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Windows Event Logs  │
│ System / Security   │
│ Application / etc.  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Python Collector    │
│       PyWin32       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   SQL Server        │
│   Event Database    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       Pandas        │
│ Cleaning & Analysis │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Feature Engineering │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Machine Learning    │
│ Logistic Regression │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Prediction &        │
│ Model Evaluation    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Streamlit Dashboard │
└─────────────────────┘
```

---

# 🚀 Development Roadmap

The project will be developed incrementally.

### Phase 1 — Event Collection

* [x] Read Windows Event Logs
* [ ] Collect multiple log types
* [ ] Extract additional event fields
* [ ] Handle collection errors
* [ ] Implement continuous collection

### Phase 2 — Database

* [ ] Create SQL Server database
* [ ] Design event schema
* [ ] Insert events
* [ ] Prevent duplicate events
* [ ] Add indexes
* [ ] Optimize database queries

### Phase 3 — Data Analysis

* [ ] Load events with Pandas
* [ ] Clean the dataset
* [ ] Handle missing values
* [ ] Explore Event IDs
* [ ] Create visualizations
* [ ] Perform exploratory data analysis

### Phase 4 — Machine Learning

* [ ] Create labels
* [ ] Engineer features
* [ ] Split training/testing data
* [ ] Train Logistic Regression
* [ ] Evaluate the model
* [ ] Experiment with additional models

### Phase 5 — Dashboard

* [ ] Create Streamlit application
* [ ] Display event statistics
* [ ] Display event charts
* [ ] Display model predictions
* [ ] Add filtering and searching

### Phase 6 — Advanced Features

* [ ] Anomaly detection
* [ ] Real-time event monitoring
* [ ] Multiple machine support
* [ ] Automated alerts
* [ ] Model retraining
* [ ] Event correlation
* [ ] More advanced ML models

---

# 🎓 Learning Goals

This project is also designed as a practical learning project.

Through it, I will gain experience with:

### Python

* File and system interaction
* Windows APIs
* Database connectivity
* Data processing
* Project organization

### SQL Server

* Database design
* Tables
* Indexes
* Queries
* Data insertion
* Data analysis

### Pandas

* DataFrames
* Data cleaning
* Feature engineering
* Data analysis

### Machine Learning

* Classification
* Logistic Regression
* Training and testing
* Feature engineering
* Model evaluation

### Data Visualization

* Matplotlib
* Event analysis
* Charts and trends

### Deployment / Dashboard

* Streamlit
* Interactive data visualization
* ML prediction interfaces

---

# 🔐 Security & Privacy

Windows Event Logs can contain sensitive information.

This project should be used only on systems that you are authorized to monitor.

When sharing datasets publicly:

* Remove usernames where appropriate.
* Remove IP addresses if they identify private systems.
* Avoid publishing sensitive security events.
* Do not upload private Windows logs to public repositories.
* Review data before committing it to GitHub.

---

# 📦 Installation

Clone the repository:

```bash
git clone <repository-url>

cd Windows-Event-ML
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Example `requirements.txt`:

```text
pywin32
pyodbc
pandas
numpy
matplotlib
scikit-learn
streamlit
```

---

# ▶️ Running the Project

The project will eventually consist of several components.

### Start Event Collection

```bash
python collector/event_collector.py
```

### Run Data Analysis

```bash
python preprocessing/preprocessing.py
```

### Train the Model

```bash
python model/train.py
```

### Start the Dashboard

```bash
streamlit run dashboard/app.py
```

---

# 💡 Initial Focus

Instead of attempting to process every Windows event immediately, the first version of the project can focus on the **Security Event Log**.

For example:

```text
4624 → Successful Logon
4625 → Failed Logon
```

This provides a relatively clear starting point for understanding:

```text
Windows Events
       ↓
Data Collection
       ↓
SQL Server
       ↓
Pandas
       ↓
Feature Engineering
       ↓
Machine Learning
       ↓
Classification
```

After the pipeline works correctly, additional event sources can be added.

---

# 📌 Future Vision

The long-term goal is to transform this project from a simple event collector into a complete **Windows Event Analytics and Machine Learning Platform**.

Potential future architecture:

```text
             Windows Computers
              /      |      \
             /       |       \
            ▼        ▼        ▼
        Event     Event     Event
        Logs      Logs      Logs
           \        |        /
            \       |       /
             ▼      ▼      ▼
          Event Collection
                 │
                 ▼
             SQL Server
                 │
        ┌────────┴────────┐
        ▼                 ▼
   Data Analysis      ML Pipeline
        │                 │
        └────────┬────────┘
                 ▼
          Streamlit Dashboard
                 │
                 ▼
          Event Monitoring
```

The project will start simple and gradually evolve as more data, features, and machine learning techniques are added.

---

# 👨‍💻 Author

**Sayed Ashtar Reza Entezar**

This project is part of my journey in learning:

**Python → Data Analysis → Machine Learning → SQL Server → AI Engineering**

---

# ⭐ Project Status

**In Development 🚧**

The project is being developed incrementally, with the initial focus on building a reliable Windows Event collection and database pipeline before expanding into machine learning and real-time monitoring.
