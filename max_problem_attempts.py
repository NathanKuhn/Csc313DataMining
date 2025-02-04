import csv
from collections import Counter

EARLY_FILE = "dataset/early.csv"
LATE_FILE = "dataset/late.csv"


def max_problem_attempts():
    attempts_counter = Counter()
    students_per_problem = {}

    with open(EARLY_FILE, "r") as early_file:
        early_reader = csv.reader(early_file)
        next(early_reader)  # Skip header line

        for row in early_reader:
            student_id = row[0]
            assignment_id = row[1]
            problem_id = row[2]
            attempts = int(row[3])

            attempts_counter[problem_id] += attempts

            if problem_id not in students_per_problem:
                students_per_problem[problem_id] = set()
            
            students_per_problem[problem_id].add(student_id)

    with open(LATE_FILE, "r") as late_file:
        late_reader = csv.reader(late_file)
        next(late_reader)  # Skip header line

        for row in late_reader:
            student_id = row[0]
            assignment_id = row[1]
            problem_id = row[2]
            attempts = int(row[3])

            attempts_counter[problem_id] += attempts

            if problem_id not in students_per_problem:
                students_per_problem[problem_id] = set()
            
            students_per_problem[problem_id].add(student_id)

    max_problem = None
    max_avg = None
    for problem in attempts_counter.keys():
        avg = attempts_counter[problem] / len(students_per_problem[problem])

        if not max_problem or max_avg < avg:
            max_problem = problem
            max_avg = avg

    return max_problem, max_avg


if __name__ == "__main__":
    max_problem, max_count = max_problem_attempts()
    print(f"Problem with maximum attempts: {max_problem} with {max_count:0.2f} attempts")
