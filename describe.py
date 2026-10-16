import sys
import subprocess
from toolkit import read_dataset


def print_statistics(sorted_columns, stat_values):
    length_stats_columns = []
    length_column = 0
    for stat in stat_values:
        if len(stat) > length_column:
            length_column = len(stat)
    length_stats_columns.append(length_column)
    for i, name in enumerate(sorted_columns):
        length_column = len(name)
        for j in stat_values:
            text = f"{stat_values[j][i]:.6f}"
            if len(text) > length_column:
                length_column = len(text)
        length_stats_columns.append(length_column)
        line = " " * length_stats_columns[0]
    for i, name in enumerate(sorted_columns):
        line = line + f"  {name:>{length_stats_columns[i+1]}}"
    line = line + "\n"
    for stat in stat_values:
        line = line + f"{stat:<{length_stats_columns[0]}}"
        for j, value in enumerate(stat_values[stat]):
            line = line + f"  {value:>{length_stats_columns[j+1]}.6f}"
        line = line + "\n"

    if sys.stdout.isatty():
        try:
            subprocess.run(["less", "-S"], input=line, text=True)
        except FileNotFoundError:
            print(line, end="")
    else:
        print(line, end="")


def percentile_calcul(x, total, column):
    if total == 1:
        return column[0]
    percentile = x * (total - 1)
    position = int(percentile)
    decimal = percentile - position
    position_value = column[position]
    decimal_value = decimal * (column[position + 1] - column[position])
    percentile_value = position_value + decimal_value
    return percentile_value


def statistics(sorted_columns):
    stat_values = {"Count": [],
                   "Mean": [],
                   "Std": [],
                   "Min": [],
                   "25%": [],
                   "50%": [],
                   "75%": [],
                   "Max": []}
    for column in sorted_columns:
        total = 0
        for index in sorted_columns[column]:
            total = total + 1
        stat_values["Count"].append(total)
        stat_values["Min"].append(sorted_columns[column][0])
        stat_values["Max"].append(sorted_columns[column][total-1])
        sum_values = 0
        for value in sorted_columns[column]:
            sum_values = sum_values + value
        mean = sum_values/total
        stat_values["Mean"].append(mean)
        total_square = 0
        if total <= 1:
            std_value = float("nan")
        else:
            for value in sorted_columns[column]:
                total_square = total_square + (value - mean) * (value - mean)
            variance = total_square / (total - 1)
            std_value = variance ** 0.5
        stat_values["Std"].append(std_value)
        percentile_25 = percentile_calcul(0.25, total, sorted_columns[column])
        stat_values["25%"].append(percentile_25)
        percentile_50 = percentile_calcul(0.50, total, sorted_columns[column])
        stat_values["50%"].append(percentile_50)
        percentile_75 = percentile_calcul(0.75, total, sorted_columns[column])
        stat_values["75%"].append(percentile_75)
    return stat_values


def sorted_list(numeric_columns):
    sorted_columns = {}
    for column in numeric_columns:
        sorted_columns[column] = []
        for item in numeric_columns[column]:
            if item is None:
                continue
            for position, value in enumerate(sorted_columns[column]):
                if item < value:
                    sorted_columns[column].insert(position, item)
                    break
            else:
                sorted_columns[column].append(item)
    return sorted_columns


def main():
    if len(sys.argv) != 2:
        print("usage: python3 describe.py <file.csv>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    numeric_columns, houses, has_houses = read_dataset(path)
    sorted_columns = sorted_list(numeric_columns)
    stat_values = statistics(sorted_columns)
    print_statistics(sorted_columns, stat_values)


if __name__ == "__main__":
    main()
