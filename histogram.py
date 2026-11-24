import sys
import matplotlib.pyplot as plt
from toolkit import read_dataset


def notes_of_house(notes, houses, house):
    house_note = []
    for note, house_student in zip(notes, houses):
        if note is None or house_student != house:
            continue
        house_note.append(note)
    return house_note


def min_max_value(hogwarts_course):
    min_value = None
    max_value = None
    for item in hogwarts_course:
        if item is None:
            continue
        if min_value is None or item < min_value:
            min_value = item
        if max_value is None or item > max_value:
            max_value = item
    return min_value, max_value


def draw_histogram(numeric_columns, houses):
    line = 4
    column = 4
    fig, axes = plt.subplots(line, column, figsize=(16, 10))
    house_name = []
    for house in houses:
        if house != "" and house not in house_name:
            house_name.append(house)
    for i, course in enumerate(numeric_columns):
        ax = axes[i // column][i % column]
        min_value, max_value = min_max_value(numeric_columns[course])
        for house in house_name:
            house_note = notes_of_house(numeric_columns[course], houses, house)
            n = len(house_note)
            if n == 0:
                continue
            ax.hist(house_note, bins=10, range=(min_value, max_value),
                    weights=[100 / n] * n, histtype="step", label=house)
        ax.set_title(course)
    for i in range(len(numeric_columns), line * column):
        axes[i // column][i % column].axis("off")
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower right")
    fig.supylabel("% students from the house")
    fig.tight_layout()
    plt.show()


def main():
    if len(sys.argv) != 2:
        print("usage: python3 histogram.py <file.csv>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    numeric_columns, houses, has_houses = read_dataset(path)
    if not has_houses:
        print("error: no house in dataset file", file=sys.stderr)
        sys.exit(1)
    draw_histogram(numeric_columns, houses)


if __name__ == "__main__":
    main()
