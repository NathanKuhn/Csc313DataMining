import csv
from collections import Counter

EARLY_FILE = "dataset/early.csv"
LATE_FILE = "dataset/late.csv"


def max_problem_attempts():
    attempts_counter = Counter()

    with open(EARLY_FILE, "r") as early_file:
        early_reader = csv.reader(early_file)
        next(early_reader)  # Skip header line

        for row in early_reader:
            assignment_id = row[1]
            problem_id = row[2]
            attempts = int(row[3])

            attempts_counter[problem_id] += attempts

    with open(LATE_FILE, "r") as late_file:
        late_reader = csv.reader(late_file)
        next(late_reader)  # Skip header line

        for row in late_reader:
            assignment_id = row[1]
            problem_id = row[2]
            attempts = int(row[3])

            attempts_counter[problem_id] += attempts

    max_problem = max(attempts_counter, key=attempts_counter.get)
    max_count = attempts_counter[max_problem]

    return max_problem, max_count


if __name__ == "__main__":
    max_problem, max_count = max_problem_attempts()
    print(f"Problem with maximum attempts: {max_problem} with {max_count} attempts")
