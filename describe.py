import sys
from toolkit import read_dataset


def main():
    if len(sys.argv) != 2:
        print("usage: python3 describe.py <file.csv>", file=sys.stderr)
        sys.exit(1)
    path = sys.argv[1]
    numeric_columns, houses, has_houses = read_dataset(path)


if __name__ == "__main__":
    main()
