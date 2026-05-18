def migration_readiness(metrics):

    score = 100

    issues = []

    suggestions = []

    # Heading checks
    if metrics["heading_count"] == 0:

        score -= 30

        issues.append(
            "No headings detected"
        )

        suggestions.append(
            "Add structured headings"
        )

    # Large paragraph checks
    if metrics["large_paragraphs"] > 3:

        score -= 20

        issues.append(
            "Large paragraphs detected"
        )

        suggestions.append(
            "Split large paragraphs"
        )

    # Dense content
    if metrics[
        "average_words_per_paragraph"
    ] > 120:

        score -= 20

        issues.append(
            "Dense content structure"
        )

        suggestions.append(
            "Improve readability"
        )

    # Duplicate headings
    if len(
        metrics["duplicate_headings"]
    ) > 0:

        score -= 10

        issues.append(
            "Duplicate headings found"
        )

        suggestions.append(
            "Standardize section titles"
        )

    # Final readiness
    if score >= 80:

        readiness = "Ready for Migration"

    elif score >= 60:

        readiness = "Needs Minor Cleanup"

    else:

        readiness = (
            "Requires Restructuring"
        )

    return {
        "migration_score": score,
        "migration_readiness": readiness,
        "issues": issues,
        "suggestions": suggestions
    }