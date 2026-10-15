import pandas as pd

# Load the datasets
emails = pd.read_csv(
    "data/student_emails_merged.csv",
    low_memory=False,
    encoding="cp1252"
)

labels = pd.read_csv(
    "data/student_email_review_all_10574_fully_labeled.csv",
    low_memory=False,
    encoding="cp1252"
)

# Dataset dimensions
print("Original shape:", emails.shape)
print("Label shape:", labels.shape)

# Inspect column names
print("\nOriginal columns:")
print(emails.columns.tolist())

print("\nLabel columns:")
print(labels.columns.tolist())

# Preview some email metadata
print("\nFirst five emails:")
print(
    emails[["from_domain", "subject"]].head()
)

# Missing values
print("\nMissing values:")
print(
    emails[
        ["subject", "body", "from_domain"]
    ].isna().sum()
)

# Priority distribution
print("\nPriority labels:")
print(labels["YOUR priority"].value_counts())

# Source of labels
print("\nLabel sources:")
print(
    labels["Priority label source"].value_counts()
)

# Check unique emails
print("\nDuplicate IDs:")
print(emails["email_uid"].duplicated().sum())
