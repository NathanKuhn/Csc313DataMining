
from typing import Union, Optional
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

MAIN_TABLE = "dataset/Data/MainTable.csv"
CODE_STATES = "dataset/Data/CodeStates/CodeStates.csv"
SUBJECT_TABLE = "dataset/Data/LinkTables/Subject.csv"


def process_data(problem_attempts):
    

    X = []
    y = []

    for problem in list(problem_attempts.keys()):
        X.append(problem)
        y.append(problem_attempts[problem])
    
    X = np.array(X, dtype=np.int16).reshape(-1, 1)
    y = np.array(y, dtype=np.int16)

    model = LinearRegression().fit(X, y)

    print(f"R^2: {model.score(X, y)}")
    print(f"Intercept: {model.intercept_}")
    print(f"Slope: {model.coef_}")

    plt.figure(figsize=(6, 4))
    plt.title("Attempts per problem")
    plt.scatter(X, y)
    plt.xlabel("Problem")
    plt.ylabel("Attempts")
    plt.show()
    return


def process_row():
    """Function to process a single row and return its AST depth if applicable"""
    
    df = pd.read_csv(MAIN_TABLE)
    problem_attempts = {}
    for row in range(0, len(df)):
        problem_id = df['ProblemID'][row]
        if problem_id not in problem_attempts:
            problem_attempts[problem_id] = 0
        problem_attempts[problem_id] += 1

    return problem_attempts

if __name__ == "__main__":
    problem_attempts = process_row()
    process_data(problem_attempts)