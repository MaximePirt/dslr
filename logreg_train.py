import sys
from toolkit import read_dataset
from toolkit import mean_calcul
from toolkit import std_calcul


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
    in_the_house = y_by_house(houses)
    mean_std = mean_and_std(numeric_columns)
    normalize_column = normalize_values(numeric_columns, mean_std)


if __name__ == "__main__":
    main()


# prend data.csv en parametre
# enleve les eleves sans maisons
# technique gradient descent
# genere un fichier qui contient les poids
