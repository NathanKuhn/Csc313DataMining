import csv
from collections import Counter
import matplotlib.pyplot as plt
import sklearn
import numpy as np

CODE_STATE_FILE = "dataset/Data/CodeStates/CodeStates.csv"
MAIN_TABLE = "dataset/Data/MainTable.csv"
GRADE_TABLE = "dataset/Data/LinkTables/Subject.csv"


def count_whitespace(code):
    return code.count(" ")


def whitespace_dataset():
    with open(CODE_STATE_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header line

        whitespace_by_id = {k: count_whitespace(v) for k, v in reader}

    with open(GRADE_TABLE, "r") as file:
        reader = csv.reader(file)
        next(reader)

        grade_by_id = {row[0]: row[1] for row in reader}

    with open(MAIN_TABLE, "r") as file:
        reader = csv.reader(file)
        next(reader)

        attempts_by_student = Counter()
        whitespace_by_student = Counter()
        problem_set_by_student = {}

        for row in reader:
            student_id = row[1]
            problem_id = row[8]
            code_state_id = row[9]

            attempts_by_student[student_id] += 1
            whitespace_by_student[student_id] += whitespace_by_id[code_state_id]

            if student_id not in problem_set_by_student:
                problem_set_by_student[student_id] = set()

            problem_set_by_student[student_id].add(problem_id)

        avg_whitespace_by_student = {
            k: whitespace_by_student[k] / attempts_by_student[k]
            for k in attempts_by_student
        }
        avg_attempts_by_student = {
            k: attempts_by_student[k] / len(problem_set_by_student[k])
            for k in problem_set_by_student
        }

        X = []
        y = []

        for student_id in avg_whitespace_by_student:
            if student_id not in grade_by_id or float(grade_by_id[student_id]) <= 0.1:
                continue
            X.append(avg_whitespace_by_student[student_id])
            y.append(grade_by_id[student_id])

        X = np.array(X, dtype=np.float32).reshape(-1, 1)
        y = np.array(y, dtype=np.float32)

        model = sklearn.linear_model.LinearRegression().fit(X, y)
        print("Grade vs Whitespace Model Results:")
        print(f"R^2:       {model.score(X, y):.4f}")
        print(f"Intercept: {model.intercept_:.4f}")
        print(f"Slope:     {model.coef_[0]:.4f}")

        plt.scatter(X, y)
        plt.plot(X, model.predict(X), color="red")
        plt.title("Grade vs Whitespace")
        plt.xlabel("Average Whitespace")
        plt.ylabel("Grade")
        plt.show()


if __name__ == "__main__":
    whitespace_dataset()
