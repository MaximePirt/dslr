import sys
import json
import csv
from pathlib import Path
from toolkit import read_dataset
from toolkit import h_calcul
from toolkit import normalize_values


def read_model_weight(path):
    if not path.endswith(".json"):
        print("error: model weight file must be .json", file=sys.stderr)
        sys.exit(1)
    try:
        with open(path, encoding="utf-8") as f:
            model = json.load(f)
    except OSError as error:
        print(f"error: cannot read model weight file: {error}", file=sys.stderr)
        sys.exit(1)
    except ValueError as error:
        print(f"error: invalid json in model weight file: {error}",
              file=sys.stderr)
        sys.exit(1)
    if not isinstance(model, dict):
        print("error: model weight file must contain an object",
              file=sys.stderr)
        sys.exit(1)
    for key in ("theta", "mean_std", "features"):
        if key not in model:
            print(f"error: no '{key}' in model weight file",
                  file=sys.stderr)
            sys.exit(1)
    return model["theta"], model["mean_std"], model["features"]


def save_predictions(predictions_house):
    houses_path = Path(__file__).resolve().parent / "houses.csv"
    try:
        with open(houses_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(["Index", "Hogwarts House"])
            for i in range(len(predictions_house)):
                writer.writerow([i, predictions_house[i]])
    except OSError:
        print("error: impossible to save houses predictions", file=sys.stderr)
        sys.exit(1)


def main():
    if len(sys.argv) != 3:
        print("usage: python3 logreg_predict.py <file.csv> <file.json>", file=sys.stderr)
        sys.exit(1)
    dataset = sys.argv[1]
    model_weight = sys.argv[2]
    theta, mean_std, features = read_model_weight(model_weight)
    numeric_columns, _, _ = read_dataset(dataset)
    normalized = normalize_values(numeric_columns, mean_std)
    h_by_house = {}
    for house in theta:
        h_by_house[house] = h_calcul(normalized, features, theta[house])
    predictions_house = []
    students = len(h_by_house[house])
    for student in range(students):
        h = 0
        for house in theta:
            h_tmp = h_by_house[house][student]
            if h_tmp > h:
                h = h_tmp
                prediction = house
        predictions_house.append(prediction)
    save_predictions(predictions_house)


if __name__ == "__main__":
    main()
