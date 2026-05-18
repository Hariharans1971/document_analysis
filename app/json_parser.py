import json
import re


def extract_json(text):

    cleaned_text = re.sub(
        r"```json|```",
        "",
        text
    ).strip()

    return json.loads(cleaned_text)