import fitz
from docx import Document
import os


# ---------------------------------------------------
# PDF PARSER
# ---------------------------------------------------

def parse_pdf(file_path):

    doc = fitz.open(file_path)

    text = ""

    headings = []

    paragraphs = []

    image_count = 0

    total_pages = len(doc)

    for page in doc:

        # Extract text

        page_text = page.get_text()

        text += page_text + "\n"

        # Count images

        images = page.get_images(
            full=True
        )

        image_count += len(images)

        # Process lines

        lines = page_text.split("\n")

        for line in lines:

            clean_line = line.strip()

            if not clean_line:
                continue

            paragraphs.append(
                clean_line
            )

            # Heading detection logic

            if (

                len(clean_line.split()) <= 8

                and (
                    clean_line.isupper()
                    or clean_line.istitle()
                )

                and len(clean_line) > 3
            ):

                headings.append(
                    clean_line
                )

    doc.close()

    return {

        "text": text,

        "headings": headings,

        "paragraphs": paragraphs,

        "total_pages": total_pages,

        "image_count": image_count
    }


# ---------------------------------------------------
# DOCX PARSER
# ---------------------------------------------------

def parse_docx(file_path):

    doc = Document(file_path)

    text = ""

    headings = []

    paragraphs = []

    image_count = 0

    # Count images

    for rel in doc.part.rels.values():

        if "image" in rel.target_ref:

            image_count += 1

    # Extract text

    for para in doc.paragraphs:

        para_text = para.text.strip()

        if not para_text:
            continue

        text += para_text + "\n"

        paragraphs.append(
            para_text
        )

        # Heading detection

        if para.style.name.startswith(
            "Heading"
        ):

            headings.append(
                para_text
            )

    # Approximate page count

    word_count = len(
        text.split()
    )

    total_pages = max(
        1,
        round(word_count / 300)
    )

    return {

        "text": text,

        "headings": headings,

        "paragraphs": paragraphs,

        "total_pages": total_pages,

        "image_count": image_count
    }


# ---------------------------------------------------
# MAIN DOCUMENT ROUTER
# ---------------------------------------------------

def parse_document(file_path):

    if not os.path.exists(file_path):

        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension == ".pdf":

        return parse_pdf(
            file_path
        )

    elif extension == ".docx":

        return parse_docx(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported file format. Only PDF and DOCX are supported."
        )