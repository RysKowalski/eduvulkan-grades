import json
from data_stuff import ProcessedGradeList, ProcessedGrade


def load_grades() -> ProcessedGradeList:
    with open("grades.json", "r") as file:
        return json.load(file)


def sort_grades(grade_list: ProcessedGradeList) -> dict[str, list[ProcessedGrade]]:
    sorted_grades: dict[str, list[ProcessedGrade]] = {}
    for grade in grade_list:
        if grade["subject"] not in sorted_grades.keys():
            sorted_grades[grade["subject"]] = []
        sorted_grades[grade["subject"]].append(grade)
    return sorted_grades


def vizualize_grades(grades: dict[str, list[ProcessedGrade]]):
    viz_grdes: list[str] = []
    for grade_key in grades.keys():
        grade_str: str = grade_key + " "


if __name__ == "__main__":
    print(sort_grades(load_grades()))
