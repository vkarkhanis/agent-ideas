import re

SOFTWARE_KEYWORDS = [
    "software", "programming", "developer", "engineering",
    "java", "python", "javascript", "react", "node",
    "spring", "microservices", "architecture", "system design",
    "api", "database", "concurrency", "performance",
    "testing", "devops", "cloud", "aws", "kubernetes"
]

BANNED_KEYWORDS = [
    "violence", "kill", "hate", "abuse",
    "politics", "election", "religion",
    "crypto", "stock", "trading",
    "medical", "drug", "illegal", "porn"
]

def validate_subject(subject: str) -> tuple[bool, str]:
    s = subject.lower()

    if any(word in s for word in BANNED_KEYWORDS):
        return False, (
            "This app is strictly for software engineering topics. "
            "Please enter a professional software development subject."
        )

    if not any(word in s for word in SOFTWARE_KEYWORDS):
        return False, (
            "Please enter a topic related to software development "
            "(e.g. Java, system design, performance, architecture)."
        )

    return True, ""
