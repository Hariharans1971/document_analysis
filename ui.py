import streamlit as st
import os
import json
import tempfile

from app.main import process_document


st.set_page_config(
    page_title="Document Migration Analyzer",
    layout="wide"
)


st.title(
    "📄 Document Analysis & Migration Readiness Tool"
)

st.markdown(
    """
Analyze PDF and DOCX documents for migration readiness using:

- Heuristic document analysis
- AI semantic analysis
- Migration readiness scoring
- Structural quality evaluation
"""
)


uploaded_files = st.file_uploader(
    "Upload PDF or DOCX files",
    type=["pdf", "docx"],
    accept_multiple_files=True
)


if uploaded_files:

    all_reports = []

    progress_bar = st.progress(0)

    total_files = len(uploaded_files)

    for index, uploaded_file in enumerate(uploaded_files):

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=os.path.splitext(
                uploaded_file.name
            )[1]
        ) as temp_file:

            temp_file.write(
                uploaded_file.read()
            )

            temp_path = temp_file.name

        try:

            report = process_document(
                temp_path
            )

            all_reports.append(report)

            st.success(
                f"Processed: {uploaded_file.name}"
            )

            st.subheader(
                uploaded_file.name
            )

            metrics = report.get(
                "metrics",
                {}
            )

            heuristic_ai = report.get(
                "ai_analysis",
                {}
            )

            migration = report.get(
                "migration_assessment",
                {}
            )

            llm_analysis = report.get(
                "llm_deep_analysis",
                {}
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Pages",
                    metrics.get(
                        "total_pages",
                        0
                    )
                )

                st.metric(
                    "Words",
                    metrics.get(
                        "word_count",
                        0
                    )
                )

            with col2:
                
                st.metric(
                    "Headings",
                    metrics.get(
                        "heading_count",
                        0
                    )
                )

                st.metric(
                    "Paragraphs",
                    metrics.get(
                        "paragraph_count",
                        0
                    )
                )
                
                st.metric(
                    "Images",
                    metrics.get(
                        "image_count",
                        0
                    )
                )

            with col3:

                st.metric(
                    "Readability",
                    heuristic_ai.get(
                        "readability",
                        "N/A"
                    )
                )

                st.metric(
                    "Migration Score",
                    migration.get(
                        "migration_score",
                        "N/A"
                    )
                )

            st.divider()

            st.markdown(
                "## Heuristic Analysis"
            )

            st.write(
                f"**Structure Quality:** "
                f"{heuristic_ai.get('structure_quality', 'N/A')}"
            )

            st.write(
                f"**Content Clarity:** "
                f"{heuristic_ai.get('content_clarity', 'N/A')}"
            )

            st.write(
                f"**Migration Readiness:** "
                f"{migration.get('migration_readiness', 'N/A')}"
            )

            issues = migration.get(
                "issues",
                []
            )

            if issues:

                st.markdown(
                    "### Issues Found"
                )

                for issue in issues:

                    st.error(issue)

            suggestions = migration.get(
                "suggestions",
                []
            )

            if suggestions:

                st.markdown(
                    "### Suggestions"
                )

                for suggestion in suggestions:

                    st.info(suggestion)

            st.divider()

            st.markdown(
                "## AI Semantic Analysis"
            )

            st.write(
                f"**Readability Level:** "
                f"{llm_analysis.get('readability_level', 'N/A')}"
            )

            st.write(
                f"**Structure Quality:** "
                f"{llm_analysis.get('structure_quality', 'N/A')}"
            )

            st.write(
                f"**Content Clarity:** "
                f"{llm_analysis.get('content_clarity', 'N/A')}"
            )

            st.write(
                f"**Migration Readiness:** "
                f"{llm_analysis.get('migration_readiness', 'N/A')}"
            )

            st.write(
                f"**AI Migration Score:** "
                f"{llm_analysis.get('migration_score', 'N/A')}"
            )

            ai_issues = llm_analysis.get(
                "issues_found",
                []
            )

            if ai_issues:

                st.markdown(
                    "### AI Issues Found"
                )

                for issue in ai_issues:

                    st.warning(issue)

            ai_suggestions = llm_analysis.get(
                "improvement_suggestions",
                []
            )

            if ai_suggestions:

                st.markdown(
                    "### AI Improvement Suggestions"
                )

                for suggestion in ai_suggestions:

                    st.info(suggestion)

            deep_analysis = llm_analysis.get(
                "deep_analysis",
                {}
            )

            if deep_analysis:

                with st.expander(
                    "🔍 View Deep Semantic Analysis"
                ):

                    st.markdown(
                        "### Heading Analysis"
                    )

                    st.write(
                        deep_analysis.get(
                            "heading_analysis",
                            "N/A"
                        )
                    )

                    st.markdown(
                        "### Paragraph Analysis"
                    )

                    st.write(
                        deep_analysis.get(
                            "paragraph_analysis",
                            "N/A"
                        )
                    )

                    st.markdown(
                        "### Content Consistency"
                    )

                    st.write(
                        deep_analysis.get(
                            "content_consistency",
                            "N/A"
                        )
                    )

                    st.markdown(
                        "### Migration Risks"
                    )

                    st.write(
                        deep_analysis.get(
                            "migration_risks",
                            "N/A"
                        )
                    )

                    st.markdown(
                        "### Overall Summary"
                    )

                    st.write(
                        deep_analysis.get(
                            "overall_summary",
                            "N/A"
                        )
                    )

            st.markdown("---")

        except Exception as e:

            st.error(
                f"Error processing "
                f"{uploaded_file.name}: {e}"
            )

        progress = (
            (index + 1) / total_files
        )

        progress_bar.progress(progress)

    st.success(
        "All documents processed successfully!"
    )

    st.download_button(
        label="📥 Download Summary Report",
        data=json.dumps(
            all_reports,
            indent=4
        ),
        file_name="summary_report.json",
        mime="application/json"
    )
    
