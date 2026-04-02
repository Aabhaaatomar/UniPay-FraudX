
# Payment Fraud Detection Project
# Baseline Model: Logistic Regression
# Main Model: Random Forest

# 1. Import Libraries
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from imblearn.over_sampling import SMOTE


# 2. Load Dataset

#  Dataset path
df = pd.read_csv("fraud_dataset.csv")

print("Dataset Shape:", df.shape)
print(df.head())


# 3. Define Features and Target


# Assuming target column name is 'Class'
# 0 = Normal Transaction
# 1 = Fraud Transaction

X = df.drop("Class", axis=1)
y = df["Class"]


# 4. Feature Scaling


scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)


# 5. Train Test Split


X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ==========================================
# 6. Handle Imbalanced Data using SMOTE
# ==========================================

smote = SMOTE(random_state=42)

X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)

print("After SMOTE:", np.bincount(y_train_smote))


# ==========================================
# 7. Baseline Model - Logistic Regression
# ==========================================

log_model = LogisticRegression(max_iter=1000)

log_model.fit(X_train_smote, y_train_smote)

log_pred = log_model.predict(X_test)

print("\n========== Logistic Regression Results ==========")

print("Accuracy:", accuracy_score(y_test, log_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, log_pred))

print("\nClassification Report:")
print(classification_report(y_test, log_pred))


# ==========================================
# 8. Main Model - Random Forest
# ==========================================

rf_model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

rf_model.fit(X_train_smote, y_train_smote)

rf_pred = rf_model.predict(X_test)

print("\n========== Random Forest Results ==========")

print("Accuracy:", accuracy_score(y_test, rf_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, rf_pred))

print("\nClassification Report:")
print(classification_report(y_test, rf_pred))