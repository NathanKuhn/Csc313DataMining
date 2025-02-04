import javalang
import csv
from typing import Union, Optional
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing as mp

MAIN_TABLE = "dataset/Data/MainTable.csv"
CODE_STATES = "dataset/Data/CodeStates/CodeStates.csv"
SUBJECT_TABLE = "dataset/Data/LinkTables/Subject.csv"

# def ave_ast_per_problem():
#     #df
#     code_state_df = pd.read_csv(CODE_STATES)
#     problem_ast = {}
    
#     # for row in range(0, len(df)):
#     problem_id = df['ProblemID'][row]

#     if problem_id not in problem_ast:
#         problem_ast[problem_id] = []

#     # ADD AND NO ERROR
#     if df['Compile.Result'][row] != 'Error' and df['EventType'][row] != "Compile.Error":
#         codestate_id = df['CodeStateID'][row]
#         java_code = str(code_state_df.loc[code_state_df['CodeStateID'] == codestate_id, 'Code'].values[0])
#         depth = batch_parser(java_code)
#         problem_ast[problem_id].append(depth)

#     return problem_ast


def process_data(problem_ast):
    problem_ids = list(problem_ast.keys())
    ave_depth = {}
    depth = 0
    for i in problem_ids:
        total = 0
        length = len(problem_ast[i])
        for depth in problem_ast[i]:
            if depth is not None:
                total += depth
        mean = total / length
        if i not in ave_depth:
            ave_depth[i] = mean

    X = []
    y = []

    for problem in list(ave_depth.keys()):
        X.append(problem)
        y.append(ave_depth[problem])
    
    X = np.array(X, dtype=np.int16).reshape(-1, 1)
    y = np.array(y, dtype=np.float32)

    model = LinearRegression().fit(X, y)

    print(f"R^2: {model.score(X, y)}")
    print(f"Intercept: {model.intercept_}")
    print(f"Slope: {model.coef_}")

    plt.figure(figsize=(6, 4))
    plt.title("Average AST Depth per Problem")
    plt.scatter(X, y)
    plt.xlabel("Problem")
    plt.ylabel("Average AST Depth")
    return

def process_row(row, code_state_df):
    """Function to process a single row and return its AST depth if applicable"""
    problem_id = row['ProblemID']
    
    # Skip rows with errors
    if row['Compile.Result'] == 'Error' or row['EventType'] == "Compile.Error":
        return None  # Skip processing
    
    codestate_id = row['CodeStateID']
    
    # Get the Java code corresponding to the CodeStateID
    java_code = str(code_state_df.loc[code_state_df['CodeStateID'] == codestate_id, 'Code'].values[0])
    
    # Compute AST depth
    depth = batch_parser(java_code)
    
    return (problem_id, depth)

def ave_ast_per_problem():
    df = pd.read_csv(MAIN_TABLE)
    code_state_df = pd.read_csv(CODE_STATES)

    # Convert DataFrame rows to dictionaries for parallel processing
    rows = df.to_dict(orient="records")

    # Use multiprocessing to process rows in parallel
    with mp.Pool(mp.cpu_count()) as pool:
        results = pool.starmap(process_row, [(row, code_state_df) for row in rows])

    # Collect results in a dictionary
    problem_ast = {}
    for result in results:
        if result: 
            problem_id, depth = result
            if problem_id not in problem_ast:
                problem_ast[problem_id] = []
            problem_ast[problem_id].append(depth)

    return problem_ast


def calculate_ast_depth(node: Union[javalang.ast.Node, list, tuple], current_depth: int = 0) -> int:
    if node is None:
        return current_depth
    
    # Handle lists and tuples of nodes
    if isinstance(node, (list, tuple)):
        if not node:
            return current_depth
        return max(calculate_ast_depth(item, current_depth) for item in node)
    
    # If not a javalang Node, return current depth
    if not isinstance(node, javalang.ast.Node):
        return current_depth
    
    # Get all children of the current node
    max_child_depth = current_depth
    
    # Directly access children of the node
    for child in node.children:
        child_depth = calculate_ast_depth(child, current_depth + 1)
        max_child_depth = max(max_child_depth, child_depth)
    
    return max_child_depth


def analyze_java_code(java_code: str) -> tuple[Optional[int], str]:
    """
    Analyzes Java code and returns its AST depth.
    
    Args:
        java_code: String containing Java code
    
    Returns:
        tuple: (depth of AST or None if parsing fails, error message if any)
    """
    try:
        tree = javalang.parse.parse(java_code)
        depth = calculate_ast_depth(tree)
        
        return depth, ""
    except javalang.parser.JavaSyntaxError as e:
        return None, f"Syntax error: {str(e)}"
    except Exception as e:
        return None, f"Error analyzing code: {str(e)}"

def batch_parser(java_code):
    """
    Formats java code, parses it into an ast and calculates tree depth.
    Returns tree depth
    """

    complete_code = """
        class Test {
            """ + java_code + """
        }
        """
 
    depth, error = analyze_java_code(complete_code)
    
    return depth

if __name__ == "__main__":
    process_data(ave_ast_per_problem())