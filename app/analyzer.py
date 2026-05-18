def analyze_document(metrics):

    readability = "Easy"

    structure_quality = "Well Organized"

    content_clarity = "Clear"

    migration_readiness = (
        "Ready for Migration"
    )

    migration_score = 100

    issues = []

    suggestions = []

    # -----------------------------------
    # READABILITY ANALYSIS
    # -----------------------------------

    avg_words = metrics[
        "average_words_per_paragraph"
    ]

    if avg_words > 20:

        readability = "Complex"

        content_clarity = (
            "Needs Improvement"
        )

        migration_score -= 10

        issues.append(
            "Paragraphs are too dense"
        )

        suggestions.append(
            "Split long paragraphs"
        )

    elif avg_words > 12:

        readability = "Medium"

        migration_score -= 5

    # -----------------------------------
    # HEADING ANALYSIS
    # -----------------------------------

    if metrics[
        "heading_count"
    ] < 3:

        structure_quality = (
            "Fragmented"
        )

        migration_score -= 10

        issues.append(
            "Insufficient headings"
        )

        suggestions.append(
            "Add more section headings"
        )

    # -----------------------------------
    # DUPLICATE HEADINGS
    # -----------------------------------

    if metrics[
        "duplicate_headings"
    ]:

        migration_score -= 10

        issues.append(
            "Duplicate headings found"
        )

        suggestions.append(
            "Standardize section titles"
        )

    # -----------------------------------
    # LARGE PARAGRAPHS
    # -----------------------------------

    if metrics[
        "large_paragraphs"
    ] > 5:

        migration_score -= 10

        issues.append(
            "Too many large paragraphs"
        )

        suggestions.append(
            "Break large paragraphs into smaller sections"
        )

    # -----------------------------------
    # FINAL READINESS
    # -----------------------------------

    if migration_score >= 85:

        migration_readiness = (
            "Ready for Migration"
        )

    elif migration_score >= 70:

        migration_readiness = (
            "Needs Minor Cleanup"
        )

    else:

        migration_readiness = (
            "Requires Restructuring"
        )

    # -----------------------------------
    # RETURN
    # -----------------------------------

    return {

        "readability":
        readability,

        "structure_quality":
        structure_quality,

        "content_clarity":
        content_clarity,

        "migration_score":
        migration_score,

        "migration_readiness":
        migration_readiness,

        "issues":
        issues,

        "suggestions":
        suggestions
    }