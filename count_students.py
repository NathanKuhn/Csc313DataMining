import csv

MAIN_TABLE = "dataset/Data/MainTable.csv"
SUBJECT_TABLE = "dataset/Data/LinkTables/Subject.csv"


def count_students():
    subject_ids = set()

    with open(MAIN_TABLE, "r") as main_file:
        main_reader = csv.reader(main_file)
        next(main_reader)  # Skip header line

        for row in main_reader:
            subject_id = row[1]
            subject_ids.add(subject_id)

    with open(SUBJECT_TABLE, "r") as subject_file:
        subject_reader = csv.reader(subject_file)
        next(subject_reader)  # Skip header line

        for row in subject_reader:
            subject_id = row[0]
            subject_ids.add(subject_id)

    return len(subject_ids)


if __name__ == "__main__":
    student_count = count_students()
    print(f"Total number of students: {student_count}")
