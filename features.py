import re

def make_text(sender, subject, body):

    # Normalize sender information
    sender = str(sender or "").strip().lower()

    if "@" in sender:
        sender = sender.rsplit("@", 1)[-1]

    # Normalize subject and body
    subject = str(subject or "").strip()
    body = str(body or "")[:2500]

    # Replace URLs
    body = re.sub(
        r"https?://\S+|www\.\S+",
        " URL ",
        body
    )

    # Replace email addresses in the body
    body = re.sub(
        r"[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}",
        " EMAIL ",
        body
    )

    # Replace long numbers
    body = re.sub(
        r"\b\d{4,}\b",
        " NUMBER ",
        body
    )

    # Remove extra whitespace
    body = re.sub(r"\s+", " ", body).strip()

    # Combine features into one text string
    text = (
        f"sender {sender} "
        f"subject {subject} "
        f"subject {subject} "
        f"body {body}"
    )

    return text
