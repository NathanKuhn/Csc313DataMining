import csv
import numpy as np
import sklearn
import matplotlib.pyplot as plt

# change numpy print formatting
np.set_printoptions(formatter={"float": "{: 0.2f}".format})

CODE_STATE_FILE = "dataset/Data/CodeStates/CodeStates.csv"
MAIN_TABLE = "dataset/Data/MainTable.csv"
GRADE_TABLE = "dataset/Data/LinkTables/Subject.csv"
EARLY_FILE = "dataset/early.csv"
LATE_FILE = "dataset/late.csv"


def process_file(file, func):
    result = {}

    with open(file, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            key, value = func(row)
            result[key] = value

    return result


def get_dataset():
    grades = process_file(GRADE_TABLE, lambda row: (row[0], float(row[1])))
    early_stats = process_file(
        EARLY_FILE, lambda row: ((row[0], row[2]), (int(row[3]), row[4] == "True"))
    )
    late_stats = process_file(
        LATE_FILE, lambda row: ((row[0], row[2]), (int(row[3]), row[4] == "True"))
    )

    student_ids = list(grades.keys())
    early_attempts_by_student = {k: 0 for k in student_ids}
    early_successes_by_student = {k: 0 for k in student_ids}
    early_problems_by_student = {k: 0 for k in student_ids}

    late_attempts_by_student = {k: 0 for k in student_ids}
    late_successes_by_student = {k: 0 for k in student_ids}
    late_problems_by_student = {k: 0 for k in student_ids}

    for student_id, problem_id in early_stats:
        attempts, success = early_stats[(student_id, problem_id)]
        early_attempts_by_student[student_id] += attempts
        early_successes_by_student[student_id] += success
        early_problems_by_student[student_id] += 1

    for student_id, problem_id in late_stats:
        attempts, success = late_stats[(student_id, problem_id)]
        late_attempts_by_student[student_id] += attempts
        late_successes_by_student[student_id] += success
        late_problems_by_student[student_id] += 1

    X = []
    y = []
    for student_id in student_ids:
        if (
            early_problems_by_student[student_id] == 0
            or late_problems_by_student[student_id] == 0
        ):
            continue

        mean_early_attempts = (
            early_attempts_by_student[student_id]
            / early_problems_by_student[student_id]
        )
        mean_early_successes = (
            early_successes_by_student[student_id]
            / early_problems_by_student[student_id]
        )
        mean_late_attempts = (
            late_attempts_by_student[student_id] / late_problems_by_student[student_id]
        )
        mean_late_successes = (
            late_successes_by_student[student_id] / late_problems_by_student[student_id]
        )

        X.append(
            (
                mean_early_attempts,
                mean_early_successes,
                mean_late_attempts,
                mean_late_successes,
            )
        )

        y.append(grades[student_id])

    y = [1 if grade > 0.60 else 0 for grade in y]

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.float32)


def main():
    X, y = get_dataset()

    # Shuffle the dataset
    indices = np.arange(len(X))
    np.random.seed(412411)
    np.random.shuffle(indices)
    X = X[indices]
    y = y[indices]

    train_size = int(0.8 * len(X))
    X_train, y_train = X[:train_size], y[:train_size]
    X_test, y_test = X[train_size:], y[train_size:]

    model = sklearn.linear_model.LogisticRegression()
    model.fit(X_train, y_train)
    print(f"Accuracy: {model.score(X_test, y_test)}")
    print(f"Coefficients:")
    print(f"  Early Attempts:  {model.coef_[0][0]:.2f}")
    print(f"  Early Successes: {model.coef_[0][1]:.2f}")
    print(f"  Late Attempts:   {model.coef_[0][2]:.2f}")
    print(f"  Late Successes:  {model.coef_[0][3]:.2f}")
    print(f"Intercept:         {model.intercept_[0]}")


if __name__ == "__main__":
    main()
