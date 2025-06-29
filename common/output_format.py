import platform
from pathlib import Path
import json
import csv
import sys
import textwrap



def get_default_output_path(output):
    if output is not None:
        return output
    else:
        if output is None:
            system = platform.system()
            if system == "Windows":
                output = str(Path.home() / "Documents")
            elif system in ("Linux", "Darwin"):
                output = str(Path.home() / "Documents")
            else:
                output = str(Path.home())


def process_output(result, output_format, output_path):
    if not output_path is None:
        output_destination = get_default_output_path(output_path)

    resource = None
    if output_format == "json":
        resource = result.to_json()
    elif output_format == "csv":
        resource = result.to_csv()
    elif output_format == "txt":
        resource = result.to_txt()
    else:
        raise ValueError(f"Unsupported output format: {output_format}")

    if output_destination:
        with open(output_destination, "w") as f:
            f.write(resource)
    else:
        if output_format == "json":
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        elif output_format == "csv":
            reader = result.to_csv().splitlines()
            writer = csv.reader(reader)
            for row in writer:
                print(", ".join(row))
        elif output_format == "txt":
            wrapped = textwrap.fill(resource, width=80)
            print(wrapped)
        else:
            print(resource)
