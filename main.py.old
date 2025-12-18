import json
from statistics import mean
from typing_stuff import ProcessedGradeList, ProcessedGrade, VizGrades


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
    viz_grades: list[VizGrades] = []  # subject, grades, average
    for grade_key in grades.keys():
        subject_str: str = grade_key

        grades_str_list: list[str] = []
        for grade in sorted(grades[grade_key], key=lambda g: g["edited"], reverse=True):
            grades_str_list.append(str(grade["content"]))

        grade_values: list[float] = []
        for grade in grades[grade_key]:
            if grade["value"] is not None:
                for _ in range(grade["weight"]):
                    grade_values.append(grade["value"])

        average_str: str = str(round(mean(grade_values), 3))
        viz_grades.append(
            {"subject": subject_str, "grades": grades_str_list, "average": average_str}
        )

    max_subject_len: int = max(
        (len(viz_grade["subject"]) for viz_grade in viz_grades), default=0
    )

    max_grades_len: int = max(
        (len(" ".join(viz_grade["grades"])) for viz_grade in viz_grades), default=0
    )
    max_average_len: int = max(
        (len(viz_grade["average"]) for viz_grade in viz_grades), default=0
    )

    lines: list[str] = []
    for i, viz_grade in enumerate(viz_grades):
        viz_grades[i]["subject"] = viz_grade["subject"].center(max_subject_len)
        viz_grades[i]["average"] = viz_grade["average"].center(max_average_len)

    for viz_grade in viz_grades:
        lines.append(
            f"| {viz_grade['subject']} | {' '.join(viz_grade['grades']).ljust(max_grades_len)} | {viz_grade['average']} |"
        )

    separator: str = f"+{'-' * (max_subject_len + 2)}+{'-' * (max_grades_len + 2)}+{'-' * (max_average_len + 2)}+"

    for line in lines:
        print(separator)
        print(line)
    print(separator)


if __name__ == "__main__":
    ugr = load_grades()
    sgr = sort_grades(ugr)
    vizualize_grades(sgr)
