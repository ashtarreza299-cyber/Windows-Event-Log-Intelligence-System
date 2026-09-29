

import sys
import os

import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from processing.labeling import encode_columns
from sklearn.metrics import classification_report, ConfusionMatrixDisplay # <-- Added these


# 1. Load the prepared data frame
df = encode_columns()

# 2. Feature Selection

FEATURES = [
    'EventID', 
    'EventType', 
    'Hour', 
    'DayOfWeek', 
    'IsWeekend', 
    'IsNightTime', 
    'SourceName_enc', 
    'ComputerName_enc', 
    'UserName_enc', 
    'MessageLength', 
    'HasSuspiciousKeyword']

X = df[FEATURES]
Y = df['Label']

# 3. Split data to training set (80%) and testing set (20%)
x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=50)

# 4. Applying Normalization
scaler = StandardScaler()
xtrain_norm = scaler.fit_transform(x_train)
xtest_norm = scaler.transform(x_test)

# 5. Create model 
model = LogisticRegression(random_state=42, max_iter=1000)
model.fit(xtrain_norm, y_train)

# 6. Predict and Evaluate
y_predict = model.predict(xtest_norm)

# 7. Visualize and Evaluate Results (Corrected)

# A. Print the mathematical report
print("--- Classification Report ---")
print(classification_report(y_test, y_predict, zero_division=0))

# B. Plot the Confusion Matrix
# This shows exactly how many times the model predicted the right/wrong class
fig, ax = plt.subplots(figsize=(8, 6))
ConfusionMatrixDisplay.from_predictions(y_test, y_predict, ax=ax, cmap='Blues')
plt.title("Confusion Matrix: Predicted vs Actual Labels")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.tight_layout()
plt.show()