import re

def sender_domain(sender):
    sender = sender.strip().lower()

    if "@" in sender:
        return sender.rsplit("@", 1)[-1]

    return sender


def is_classroom(sender):
    return sender_domain(sender) == "classroom.google.com"


def priority_override(sender, subject):

    domain = sender_domain(sender)
    title = subject.lower()

    # All Google Classroom notifications
    if is_classroom(sender):
        return "High", "Google Classroom notification"

    # University domain
    college = (
        domain == "kiit.ac.in"
        or domain.endswith(".kiit.ac.in")
    )

    important = re.search(
        r"\b(exam|examination|admit card|"
        r"time\s*table|timetable|assignment|quiz|"
        r"placement drive|campus recruitment|"
        r"interview schedule|semester result|"
        r"registration deadline)\b",
        title
    )

    if college and important:
        return "High", "College academic/placement notice"

    # Important certification events
    certification = re.search(
        r"\b(certificate|certification)\b",
        title
    )

    urgent = re.search(
        r"\b(issued|result|expiry|expires|deadline)\b",
        title
    )

    if certification and urgent:
        return "High", "Certification result or deadline"

    return None, None


def guess_topic(sender, subject, body):

    if is_classroom(sender):
        return "Google Classroom"

    text = (subject + " " + body[:400]).lower()

    if any(word in text for word in [
        "internship", "intern ", "job opening"
    ]):
        return "Internship / Career"

    if any(word in text for word in [
        "placement drive", "campus recruitment"
    ]):
        return "Placement"

    if any(word in text for word in [
        "certificate", "certification"
    ]):
        return "Certification"

    if any(word in text for word in [
        "exam", "assignment", "quiz"
    ]):
        return "Academics"

    if sender_domain(sender).endswith(".ac.in"):
        return "University / Other"

    return "Other"


def scam_warnings(subject, body):

    text = (subject + " " + body).lower()

    warning_phrases = {
        "registration fee": "Asks for a registration fee",
        "security deposit": "Asks for a security deposit",
        "pay to confirm": "Asks for payment to confirm an offer",
        "guaranteed internship": "Promises a guaranteed internship",
        "guaranteed selection": "Promises guaranteed selection",
        "share your otp": "Requests an OTP",
        "share your password": "Requests a password"
    }

    warnings = []

    for phrase, reason in warning_phrases.items():
        if phrase in text:
            warnings.append(reason)

    return warnings
