from app.parser import parse_document

from app.metrics import calculate_metrics

from app.analyzer import analyze_document

from app.groq_analyzer import (
    analyze_document_with_groq
)

import os


def process_document(file_path):

    parsed_data = parse_document(
        file_path
    )

    text = parsed_data["text"]

    headings = parsed_data[
        "headings"
    ]

    paragraphs = parsed_data[
        "paragraphs"
    ]

    total_pages = parsed_data[
        "total_pages"
    ]

    image_count = parsed_data[
        "image_count"
    ]

    # -----------------------------------
    # METRICS
    # -----------------------------------

    metrics = calculate_metrics(

        text=text,

        headings=headings,

        paragraphs=paragraphs,

        total_pages=total_pages,
        
        image_count=image_count
    )

    # -----------------------------------
    # HEURISTIC ANALYSIS
    # -----------------------------------

    ai_analysis = analyze_document(
        metrics
    )

    # -----------------------------------
    # MIGRATION ASSESSMENT
    # -----------------------------------

    migration_assessment = {

        "migration_score":
        ai_analysis[
            "migration_score"
        ],

        "migration_readiness":
        ai_analysis[
            "migration_readiness"
        ],

        "issues":
        ai_analysis[
            "issues"
        ],

        "suggestions":
        ai_analysis[
            "suggestions"
        ]
    }

    # -----------------------------------
    # GROQ AI ANALYSIS
    # -----------------------------------

    llm_analysis = (
        analyze_document_with_groq(
            text,
            metrics
        )
    )

    # -----------------------------------
    # FINAL REPORT
    # -----------------------------------

    report = {

        "file_name":
        os.path.basename(
            file_path
        ),

        "metrics":
        metrics,

        "ai_analysis":
        {

            "readability":
            ai_analysis[
                "readability"
            ],

            "structure_quality":
            ai_analysis[
                "structure_quality"
            ],

            "content_clarity":
            ai_analysis[
                "content_clarity"
            ]
        },

        "migration_assessment":
        migration_assessment,

        "llm_deep_analysis":
        llm_analysis
    }

    return report