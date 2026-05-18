import json
import os


def save_report(file_name, report):

    safe_name = file_name.replace(
        " ",
        "_"
    )

    output_path = os.path.join(
        "outputs",
        f"report_{safe_name}.json"
    )

    with open(output_path, "w") as f:

        json.dump(report, f, indent=4)

    return output_path