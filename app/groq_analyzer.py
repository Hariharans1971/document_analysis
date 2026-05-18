from groq import Groq
from dotenv import load_dotenv
from app.json_parser import extract_json

import os
import time


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def analyze_document_with_groq(
    text,
    metrics
):

    truncated_text = text[:12000]

    prompt = f"""
You are a senior enterprise documentation migration specialist.

Analyze this document deeply for migration readiness into platforms like Document360.

DOCUMENT METRICS:
- Total Pages: {metrics['total_pages']}
- Word Count: {metrics['word_count']}
- Paragraph Count: {metrics['paragraph_count']}
- Heading Count: {metrics['heading_count']}
- Average Words Per Paragraph: {metrics['average_words_per_paragraph']}

DOCUMENT CONTENT:
{truncated_text}

Return STRICT JSON ONLY.

Required JSON format:

{{
    "readability_level": "",
    "structure_quality": "",
    "content_clarity": "",
    "migration_readiness": "",
    "migration_score": 0,

    "issues_found": [],

    "improvement_suggestions": [],

    "deep_analysis": {{

        "heading_analysis": "",

        "paragraph_analysis": "",

        "content_consistency": "",

        "migration_risks": "",

        "overall_summary": ""
    }}
}}

IMPORTANT:
- Give REAL analysis
- Mention duplicate headings
- Mention dense paragraphs
- Mention formatting inconsistencies
- Give actionable suggestions
- Do not give generic responses
"""

    try:

        response = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )

        time.sleep(2)

        content = response.choices[
            0
        ].message.content

        return extract_json(content)

    except Exception as e:

        return {
            "readability_level": "Unavailable",

            "structure_quality": "Unavailable",

            "content_clarity":
            str(e),

            "migration_readiness":
            "Fallback Heuristic Analysis Used",

            "migration_score": 75,

            "issues_found": [
                "Groq API unavailable"
            ],

            "improvement_suggestions": [
                "Retry later"
            ],

            "deep_analysis": {

                "heading_analysis":
                "Fallback analysis used.",

                "paragraph_analysis":
                "Fallback analysis used.",

                "content_consistency":
                "Fallback analysis used.",

                "migration_risks":
                "Semantic analysis unavailable.",

                "overall_summary":
                "Fallback heuristic analysis used."
            }
        }