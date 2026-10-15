from pathlib import Path
import pandas as pd

from features import make_text

DATA = Path("data")

# Load both files
emails = pd.read_csv(
    DATA / "student_emails_merged.csv",
    low_memory=False,
    encoding="cp1252"
)

labels = pd.read_csv(
    DATA / "student_email_review_all_10574_fully_labeled.csv",
    low_memory=False,
    encoding="cp1252"
)

# Select the label columns we need
labels = labels[
    [
        "Email UID",
        "YOUR priority",
        "Priority label source"
    ]
]

# Combine both datasets using email ID
df = emails.merge(
    labels,
    left_on="email_uid",
    right_on="Email UID",
    how="left",
    validate="one_to_one",
    indicator=True
)

# Ensure every email matched
if not (df["_merge"] == "both").all():
    raise ValueError("Some emails have no label")

# Handle missing fields
for col in ["from_domain", "subject", "body"]:
    df[col] = df[col].fillna("")

# Get priority labels
df["priority"] = (
    df["YOUR priority"]
    .fillna("")
    .astype(str)
    .str.strip()
    .str.title()
)

# Validate labels
valid = {"High", "Medium", "Low"}

if not df["priority"].isin(valid).all():
    raise ValueError("Invalid priority label found")

# Preserve whether the label was auto-assigned
df["label_source"] = (
    df["Priority label source"]
    .fillna("unverified")
)

# Create the text input for ML
df["text"] = [
    make_text(sender, subject, body)
    for sender, subject, body in zip(
        df["from_domain"],
        df["subject"],
        df["body"]
    )
]

# Save the training dataset
output = DATA / "training_data.csv"

df[
    ["email_uid", "text", "priority", "label_source"]
].to_csv(output, index=False)

print("Dataset created successfully!")
print("Total records:", len(df))
print(df["priority"].value_counts())
print(df["label_source"].value_counts())
