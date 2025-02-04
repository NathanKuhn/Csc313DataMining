import csv
from collections import Counter

MAIN_TABLE = "dataset/Data/MainTable.csv"


def max_compiler_errors():
    errors_counter = Counter()
    students_per_problem = {}

    with open(MAIN_TABLE, "r") as main_file:
        main_reader = csv.reader(main_file)
        next(main_reader)  # Skip header line

        for row in main_reader:
            student_id = row[1]
            problem_id = row[8]
            has_compiler_error = row[11] == "Compile" and row[13] == "Error"

            if has_compiler_error:
                errors_counter[problem_id] += 1

                if problem_id not in students_per_problem:
                    students_per_problem[problem_id] = set()
                
                students_per_problem[problem_id].add(student_id)


    max_problem = None
    max_avg = None
    for problem in errors_counter.keys():
        avg = errors_counter[problem] / len(students_per_problem[problem])

        if not max_problem or max_avg < avg:
            max_problem = problem
            max_avg = avg

    return max_problem, max_avg


if __name__ == "__main__":
    max_problem, max_count = max_compiler_errors()
    print(f"Problem with maximum compiler errors: {max_problem} with {max_count:0.2f} errors")