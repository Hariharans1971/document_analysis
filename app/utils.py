import os
import re


def clean_text(text):
    """
    Cleans extracted text by removing
    extra spaces and unwanted characters.
    """

    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def get_file_extension(file_path):
    """
    Returns lowercase file extension.
    """

    return os.path.splitext(file_path)[1].lower()


def validate_file(file_path):
    """
    Validates supported file types.
    """

    allowed_extensions = [".pdf", ".docx"]

    ext = get_file_extension(file_path)

    if ext not in allowed_extensions:
        raise Exception(
            f"Unsupported file format: {ext}"
        )

    return True


def safe_divide(a, b):
    """
    Prevent division by zero.
    """

    if b == 0:
        return 0

    return round(a / b, 2)


def count_large_paragraphs(paragraphs, limit=120):
    """
    Counts paragraphs exceeding word limit.
    """

    count = 0

    for para in paragraphs:

        if len(para.split()) > limit:
            count += 1

    return count


def detect_duplicate_headings(headings):
    """
    Detect duplicate headings.
    """

    seen = set()

    duplicates = []

    for heading in headings:

        clean_heading = heading.lower().strip()

        if clean_heading in seen:
            duplicates.append(heading)

        else:
            seen.add(clean_heading)

    return duplicates