import csv
from collections import Counter
import numpy as np
import sklearn
import matplotlib.pyplot as plt

CODE_STATE_FILE = "dataset/code_state.csv"
EARLY_FILE = "dataset/early.csv"
LATE_FILE = "dataset/late.csv"

def parse_row(row):
    return row[2], int(row[3]), row[4] == "True"


def get_difficulty_stats():
    total_attempts_per_problem = Counter()
    total_successes_per_problem = Counter()
    total_students_per_problem = Counter()

    with open(EARLY_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            problem_id, attempts, success = parse_row(row)

            total_students_per_problem[problem_id] += 1
            total_attempts_per_problem[problem_id] += attempts
            if success:
                total_successes_per_problem[problem_id] += 1
    
    with open(LATE_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            problem_id, attempts, success = parse_row(row)

            total_students_per_problem[problem_id] += 1
            total_attempts_per_problem[problem_id] += attempts
            if success:
                total_successes_per_problem[problem_id] += 1
    
    avg_attempts = {k: total_attempts_per_problem[k] / total_students_per_problem[k] for k in total_students_per_problem}
    avg_successes = {k: total_successes_per_problem[k] / total_students_per_problem[k] for k in total_students_per_problem}

    problems = list(total_students_per_problem.keys())
    
    X = np.array([avg_attempts[k] for k in problems])
    y = np.array([avg_successes[k] for k in problems])


    linear_model = sklearn.linear_model.LinearRegression()
    linear_model.fit(X.reshape(-1, 1), y)
    print(f"R^2:       {linear_model.score(X.reshape(-1, 1), y):.4f}")
    print(f"Intercept: {linear_model.intercept_:.4f}")
    print(f"Slope:    {linear_model.coef_[0]:.4f}")
    
    plt.plot(X, linear_model.predict(X.reshape(-1, 1)), color="red")
    plt.scatter(X, y)
    plt.xlabel("Log of average attempts")
    plt.ylabel("Average successes")
    plt.title("Successes vs Attempts")
    plt.show()


if __name__ == "__main__":
    get_difficulty_stats()
