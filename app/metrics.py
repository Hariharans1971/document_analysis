from collections import Counter


def calculate_metrics(
    text,
    headings,
    paragraphs,
    total_pages,
    image_count
):

    words = text.split()

    word_count = len(words)

    paragraph_count = len(
        paragraphs
    )

    heading_count = len(
        headings
    )

    average_words_per_paragraph = 0

    if paragraph_count > 0:

        average_words_per_paragraph = round(

            word_count / paragraph_count,

            2
        )

    # Large paragraphs

    large_paragraphs = 0

    for para in paragraphs:

        if len(para.split()) > 100:

            large_paragraphs += 1

    # Duplicate headings

    heading_counter = Counter(
        headings
    )

    duplicate_headings = [

        heading

        for heading, count in heading_counter.items()

        if count > 1
    ]

    return {

        "total_pages":
        total_pages,

        "word_count":
        word_count,

        "paragraph_count":
        paragraph_count,

        "heading_count":
        heading_count,

        "average_words_per_paragraph":
        average_words_per_paragraph,

        "large_paragraphs":
        large_paragraphs,

        "duplicate_headings":
        duplicate_headings,

        "image_count":
        image_count
    }