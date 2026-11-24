import sys
from toolkit import read_dataset


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
            if house == '':
                break
            if house == house_name[i]:
                y = 1
            else:
                y = 0
            in_the_house[student_house].append(y)
    return in_the_house


def main():
    if len(sys.argv) != 2:
        print("usage: python3 logreg_train.py <file.csv>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    numeric_columns, houses, has_houses = read_dataset(path)
    if not has_houses:
        print("error: no house in dataset file", file=sys.stderr)
        sys.exit(1)
    y_by_house(houses)


if __name__ == "__main__":
    main()


# prend data.csv en parametre
# enleve les eleves sans maisons
# technique gradient descent
# genere un fichier qui contient les poids
