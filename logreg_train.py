import sys
import json
from pathlib import Path
from toolkit import read_dataset
from toolkit import mean_calcul
from toolkit import std_calcul
import math
FEATURES = [
    # "Arithmancy",
    "Astronomy",
    "Herbology",
    # "Defense Against the Darks Arts",
    "Divination",
    "Muggle Studies",
    "Ancient Runes",
    "History of Magic",
    "Transfiguration",
    "Potions",
    # "Care of Magical Creatures",
    "Charms",
    "Flying",
]
ALPHA = 0.1
MAX_TURNS = 10000
TOLERANCE = 1e-6


def save_weight(theta, mean_std, features):
    model_path = Path(__file__).resolve().parent / "model_weight.json"
    try:
        with open(model_path, "w", encoding="utf-8") as f:
            json.dump({"theta": theta,
                       "mean_std": mean_std,
                       "features": features}, f)
    except OSError:
        print("error: impossible to save model weight", file=sys.stderr)
        sys.exit(1)


def y_by_house(houses):
    house_name = []
    in_the_house = {}
    for house in houses:
        if house != "" and house not in house_name:
            house_name.append(house)
    for house in house_name:
        in_the_house[house] = []
    for house in houses:
        for i, student_house in enumerate(house_name):
            if house == house_name[i]:
                y = 1
            else:
                y = 0
            in_the_house[student_house].append(y)
    return in_the_house


def remove_none(numeric_columns):
    clean_columns = {}
    for column in numeric_columns:
        clean_columns[column] = []
        for item in numeric_columns[column]:
            if item is None:
                continue
            clean_columns[column].append(item)
    return clean_columns


def mean_and_std(numeric_columns):
    clean_columns = remove_none(numeric_columns)
    mean_std = {}
    for course in clean_columns:
        total = len(clean_columns[course])
        mean = mean_calcul(clean_columns[course], total)
        std = std_calcul(clean_columns[course], total, mean)
        mean_std[course] = (mean, std)
    return mean_std


def normalize_values(numeric_columns, mean_std):
    normalize_columns = {}
    for course in numeric_columns:
        normalize_columns[course] = []
        for item in numeric_columns[course]:
            if item is None:
                grade = 0
            else:
                grade = (item - mean_std[course][0]) / mean_std[course][1]
            normalize_columns[course].append(grade)
    return normalize_columns


def sigmoid(z):
    return 1 / (1 + math.exp(-z))


def h_of_student(normalized, features, i, theta):
    z = theta[0]
    for j, course in enumerate(features, start=1):
        z = z + theta[j] * normalized[course][i]
    return sigmoid(z)


def h_calcul(normalized, features, theta):
    h_student = []
    students = len(normalized[features[0]])
    for index in range(students):
        h = h_of_student(normalized, features, index, theta)
        h_student.append(h)
    return h_student


def gradient_calcul(normalized, features, y_list, h_list):
    m = len(h_list)  # somme de tous les etudiants
    # on definit le nbr de listes dans gradient
    gradient = [0] * (1 + len(features))
    for i in range(m):
        dif = h_list[i] - y_list[i]
        gradient[0] = gradient[0] + dif
        for j, course in enumerate(features, start=1):
            # on remplit sans append les listes
            gradient[j] = gradient[j] + dif * normalized[course][i]
    for k in range(len(gradient)):
        # on divise par le nbr d'eleves chaque lite
        gradient[k] = gradient[k] / m
    return gradient  # on retourne les derives d'une maison ici, cette fonction est appele 4 fois pour 4 maisosn


def update_theta(theta, alpha, gradient):
    update_theta = []
    for j in range(len(theta)):
        update_theta.append(theta[j] - alpha * gradient[j])
    return update_theta


def cost_calcul(h_list, y_list):
    eps = 1e-15
    penalty = 0
    for j in range(len(h_list)):
        h = h_list[j]
        if h < eps:
            h = eps
        if h >= (1 - eps):
            h = 1 - eps
        y = y_list[j]
        penalty = penalty + (y * math.log(h) + (1 - y) * math.log(1 - h))
    cost = - penalty / len(h_list)
    return cost


def gradient_loop(normalized, y_list, features, alpha, max_turns, tolerance):
    theta = [0] * (1 + len(features))
    cost = float('inf')
    for turn in range(max_turns):
        h_list = h_calcul(normalized, features, theta)
        gradient = gradient_calcul(normalized, features, y_list, h_list)  # etape 1, la liste des 11 derives
        theta = update_theta(theta, alpha, gradient)
        current_cost = cost_calcul(h_list, y_list)
        if current_cost > cost:  # si le cout augmente on stoppe critere d'arret
            return theta, True, False, turn
        if cost - current_cost < tolerance:
            return theta, False, True, turn
        cost = current_cost
    return theta, False, False, turn


def main():
    if len(sys.argv) != 2:
        print("usage: python3 logreg_train.py <file.csv>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    numeric_columns, houses, has_houses = read_dataset(path)
    if not has_houses:
        print("error: no house in dataset file", file=sys.stderr)
        sys.exit(1)
    for house in houses:
        if house == '':
            print("error: a student has no house", file=sys.stderr)
            sys.exit(1)
    mean_std = mean_and_std(numeric_columns)
    normalized = normalize_values(numeric_columns, mean_std)
    y_lists = y_by_house(houses)
    theta = {}
    for house in y_lists:
        theta[house], diverged, converged, turn = gradient_loop(normalized, y_lists[house], FEATURES, ALPHA, MAX_TURNS, TOLERANCE)
        if diverged:
            print("error: divergence detected: alpha too big for house "
                  f" {houses[house]} => try smaller value", file=sys.stderr)
            sys.exit(1)
        if converged:
            print(f"information, model converged for house {house}"
                  f" at turn: {turn}")
        else:
            print(f"warning: max turns ({MAX_TURNS}) reached before "
                  f" convergence for house {house}", file=sys.stderr)
    save_weight(theta, mean_std, FEATURES)


if __name__ == "__main__":
    main()
