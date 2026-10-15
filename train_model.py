import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

from sklearn.metrics import (
    classification_report,
    confusion_matrix
)

# STEP 1: Load the processed dataset
df = pd.read_csv("data/training_data.csv")

# STEP 2: Define inputs and outputs
X = df["text"].fillna("")
y = df["priority"]

# STEP 3: Split training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# STEP 4: Build TF-IDF + SVM pipeline
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=15000,
            min_df=2,
            sublinear_tf=True
        )
    ),
    (
        "svm",
        LinearSVC(
            C=1.0,
            class_weight="balanced",
            dual=True,
            random_state=42
        )
    )
])

# STEP 5: Train the model
model.fit(X_train, y_train)

# STEP 6: Predict on test data
y_pred = model.predict(X_test)

# STEP 7: Evaluate the model
print("Classification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("Confusion Matrix:")
print(
    confusion_matrix(
        y_test,
        y_pred,
        labels=["High", "Medium", "Low"]
    )
)

# STEP 8: Train final model on entire dataset
model.fit(X, y)

# STEP 9: Save trained model
Path("models").mkdir(exist_ok=True)

joblib.dump(
    model,
    "models/priority_model.joblib"
)

print("Model trained and saved successfully!")
