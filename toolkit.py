import csv
import math
import sys


def is_numeric(argument):
    if not argument.strip():
        return None, True
    try:
        value = float(argument)
    except ValueError:
        return None, False
    if not math.isfinite(value):
        return None, True
    return value, True


def read_dataset(path):
    if not path.endswith(".csv"):
        print("error: dataset file must be .csv", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, encoding="utf-8", newline="") as f:
            reader = csv.reader(f)
            for header_line, header in enumerate(reader, start=1):
                if header:
                    break
            else:
                print("error: no header in dataset file", file=sys.stderr)
                sys.exit(1)
            fields = []
            for field in header:
                if not field or not field.strip():
                    print("error: at least one column does not have field "
                          "in header", file=sys.stderr)
                    sys.exit(1)
                fields.append(field.strip())
            if len(fields) != len(set(fields)):
                print("error, at least one duplicate value on header",
                      file=sys.stderr)
                sys.exit(1)
            columns = {}
            all_numeric = {}
            has_number = {}
            houses = []
            has_houses = False
            for feature in fields:
                columns[feature] = []
                all_numeric[feature] = True
                has_number[feature] = False
            for line_number, data in enumerate(reader, start=header_line+1):
                if not data:
                    continue
                if len(data) != len(fields):
                    print(f"error: discordance: {len(data)} data in "
                          f"{len(fields)} column on header_line {line_number}",
                          file=sys.stderr)
                    sys.exit(1)
                for column, text in zip(columns, data):
                    value, numeric = is_numeric(text)
                    if not numeric:
                        all_numeric[column] = False
                    if value is not None:
                        has_number[column] = True
                    columns[column].append(value)
                    if column == "Hogwarts House":
                        houses.append(text.strip())
                        if len(text.strip()) != 0:
                            has_houses = True
            if len(columns[feature]) == 0:
                print("error: no data in dataset file", file=sys.stderr)
                sys.exit(1)
            numeric_columns = {}
            for column in columns:
                if (not all_numeric[column] or not has_number[column] or
                        column == "Index"):
                    continue
                numeric_columns[column] = columns[column]
    except OSError as error:
        print(f"error: cannot read dataset {error}", file=sys.stderr)
        sys.exit(1)
    return numeric_columns, houses, has_houses
