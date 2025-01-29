import csv
from collections import Counter

MAIN_TABLE = "dataset/Data/MainTable.csv"


def max_compiler_errors():
    errors_counter = Counter()

    with open(MAIN_TABLE, "r") as main_file:
        main_reader = csv.reader(main_file)
        next(main_reader)  # Skip header line

        for row in main_reader:
            problem_id = row[8]
            has_compiler_error = row[11] == "Compile" and row[13] == "Error"

            if has_compiler_error:
                errors_counter[problem_id] += 1

    max_problem = max(errors_counter, key=errors_counter.get)
    max_count = errors_counter[max_problem]

    return max_problem, max_count


if __name__ == "__main__":
    max_problem, max_count = max_compiler_errors()
    print(f"Problem with maximum compiler errors: {max_problem} with {max_count} errors")