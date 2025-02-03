import javalang
import csv
from typing import Union, Optional
import pandas as pd
#import sklearn
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt


MAIN_TABLE = "dataset/Data/MainTable.csv"
CODE_STATES = "dataset/Data/CodeStates/CodeStates.csv"
SUBJECT_TABLE = "dataset/Data/LinkTables/Subject.csv"

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


def student_attempts():
    """
    Returns a hashtable where the key is the SubjectID and the value is a list containing the number of
    attempts the subject took on each problem
    """

    subject_attempts = {}
    #student_depth = {}
    df = pd.read_csv(MAIN_TABLE)
    code_state_df = pd.read_csv(CODE_STATES)

    problem_id = 0
    attempts = 0

    for row in range(0, len(df)):
        temp_problem_id = df['ProblemID'][row]
        subject_id = df['SubjectID'][row]

        if subject_id not in subject_attempts:
                subject_attempts[subject_id] = []


        if problem_id == 0:
            problem_id = df['ProblemID'][row]

        if problem_id == temp_problem_id:
            attempts += 1
        
        elif problem_id != temp_problem_id:
            subject_id = df['SubjectID'][row-1]
            codestate_id = df['CodeStateID'][row-1]
    
            # Look up java code using codestate_id from MaintTable
            java_code = code_state_df.loc[code_state_df['CodeStateID'] == codestate_id, 'Code'].values[0]

            # Parse Java Code and return tree depth
            depth = batch_parser(java_code)

            # Update list with problem id, attempts, and ast depth of last successful attempt
            subject_attempts[subject_id].append((problem_id, attempts+1, depth))
            problem_id = df['ProblemID'][row]
            attempts = 0

    return subject_attempts


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
    # if depth is not None:
    #     print(f"AST Depth: {depth}")
    # else:
    #     print(f"Error: {error}")

    return depth

def get_grades():
    student_grades = {}
    grades = pd.read_csv(SUBJECT_TABLE)
    for row in range(0, len(grades)):
        subject_id = grades['SubjectID'][row]

        if subject_id not in student_grades:
                student_grades[subject_id] = grades['X-Grade'][row]
    
    return student_grades



def analysis(student_grades, PAA):

    # Organized: key = StudentID, data = [problem #, attempts, AST]

    # AST is of the last attempt of every problem
    # Could get ast depth per problem per student, or maybe 
    # Get average number attempts per problem
    # Look at correlation between AST depth and attempts
    # Look at correlation between AST depth and grades

    students = list(PAA.keys())
    total_depth = 0
    total_attempts = 0
    student_totals = {}

    for student in students:
        for data in PAA[student]:
            if data[2] != None and data[1] != None:
                total_depth += data[2]
                total_attempts += data[1]

        # Calculate total attempts per student, and average AST depth per student
        if student not in student_totals:
            ave_depth = total_depth / len(PAA[student])
            ave_attempts = total_attempts /len(PAA[student])
            student_totals[student] = [ave_attempts, ave_depth]
            total_depth = 0
            total_attempts = 0
        
        # print(
        #     f"Student {student} had on average an AST depth of {ave_depth:.2f} per problem"
        # )

    X = []
    y = []

    for student in students:
        X.append(student_totals[student][0])
        y.append(student_totals[student][1])
    
    X = np.array(X, dtype=np.float32).reshape(-1, 1)
    y = np.array(y, dtype=np.float32)

    model = LinearRegression().fit(X, y)
    print(f"R^2: {model.score(X, y)}")
    print(f"Intercept: {model.intercept_}")
    print(f"Slope: {model.coef_}")

    plt.figure(figsize=(6, 4))
    plt.title("Average attempts vs. Average AST Depth")
    plt.scatter(X, y)
    plt.xlabel("Average Attempts")
    plt.ylabel("Average AST Depth")

    X = []
    y = []

    print("Model two:")
    for student in students:
        X.append(student_grades[student])
        y.append(student_totals[student][1])
    
    X = np.array(X, dtype=np.float32).reshape(-1, 1)
    y = np.array(y, dtype=np.float32)

    model = LinearRegression().fit(X, y)
    print(f"R^2: {model.score(X, y)}")
    print(f"Intercept: {model.intercept_}")
    print(f"Slope: {model.coef_}")

    plt.figure(figsize=(6, 4))
    plt.title("Grade vs. AST Depth")
    plt.scatter(X, y)
    plt.xlabel("Class Grade")
    plt.ylabel("Average AST Depth")

    plt.show()

    return

if __name__ == "__main__":

# Next step:
    # Thinking about using a linear classifier to classifty students above or below a certain threshold.
    # Threshold could be the average or median number of attempts per problem?
    student_attempts_ast = student_attempts()
    grades = get_grades()
    analysis(grades, student_attempts_ast)
