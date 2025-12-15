from typing_stuff import GradeList, ProcessedGradeList, GradeItem, ProcessedGrade
import json
import os


def load_data() -> GradeList:
    with open("raw.json", "r") as file:
        return json.load(file)


def process_grade(grade: GradeItem) -> ProcessedGrade:
    subject: str = grade["Column"]["Subject"]["Name"][:20]
    edited: int = grade["DateModify"]["Timestamp"]
    value: int = grade["Value"]
    content: str = grade["Content"]
    weight: int = grade["Column"]["Weight"]
    return {
        "subject": subject,
        "edited": edited,
        "value": value,
        "content": content,
        "weight": weight,
    }


def process_grades(grade_list: GradeList) -> ProcessedGradeList:
    processed_grades: ProcessedGradeList = []
    for grade in grade_list:
        processed_grades.append(process_grade(grade))
    return processed_grades


def save_lessons(processed_grades: ProcessedGradeList):
    with open("grades.json", "w") as file:
        json.dump(processed_grades, file)


def main():
    os.system("cd js_stuff; node main.js")
    save_lessons(process_grades(load_data()))


if __name__ == "__main__":
    main()
