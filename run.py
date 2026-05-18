from app.main import process_document

import os
import json


INPUT_FOLDER = "input_docs"

OUTPUT_FOLDER = "outputs"


# ---------------------------------------------------
# CREATE OUTPUT FOLDER
# ---------------------------------------------------

os.makedirs(
    OUTPUT_FOLDER,
    exist_ok=True
)


# ---------------------------------------------------
# STORE ALL REPORTS
# ---------------------------------------------------

all_reports = []


# ---------------------------------------------------
# PROCESS FILES
# ---------------------------------------------------

for file_name in os.listdir(INPUT_FOLDER):

    file_path = os.path.join(
        INPUT_FOLDER,
        file_name
    )

    try:

        report = process_document(
            file_path
        )

        all_reports.append(
            report
        )

        # ---------------------------------------------------
        # SAVE INDIVIDUAL REPORT
        # ---------------------------------------------------

        output_file = os.path.join(

            OUTPUT_FOLDER,

            f"{file_name}.json"
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(

                report,

                f,

                indent=4,

                ensure_ascii=False
            )

        print(
            f"\nProcessed: {file_name}"
        )

        print(
            f"Saved: {output_file}"
        )

    except Exception as e:

        print(
            f"\nError processing {file_name}: {e}"
        )


# ---------------------------------------------------
# SAVE SUMMARY REPORT
# ---------------------------------------------------

summary_file = os.path.join(
    OUTPUT_FOLDER,
    "summary_report.json"
)

with open(
    summary_file,
    "w",
    encoding="utf-8"
) as f:

    json.dump(

        all_reports,

        f,

        indent=4,

        ensure_ascii=False
    )


print(
    "\nAll reports generated successfully!"
)

print(
    f"Summary saved: {summary_file}"
)