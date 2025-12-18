import json
from statistics import mean
from typing import Literal
from typing_stuff import (
    FormattedLine,
    ProcessedGrade,
    ProcessedGradeList,
    LineWork,
    SortedGrades,
    GradeInfo,
)


def rgb(
    mode: Literal["fg", "bg", "both"],
    fg: tuple[int, int, int] = (0, 0, 0),
    bg: tuple[int, int, int] = (0, 0, 0),
) -> str:
    fr, fg_, fb = fg
    br, bg_, bb = bg
    if mode == "both":
        return f"\033[38;2;{fr};{fg_};{fb}m\033[48;2;{br};{bg_};{bb}m"
    elif mode == "fg":
        return f"\033[38;2;{fr};{fg_};{fb}m"
    elif mode == "bg":
        return f"\033[48;2;{br};{bg_};{bb}m"


RESET_COLOR: str = "\033[0m"

SUBJECT_COLOR: str = rgb("fg", fg=(19, 255, 255))  # #14FFFF
VALUE_COLORS: dict[int, str] = {
    1: "",
    2: rgb("fg", (0, 255, 0)),  # #00FF00
    3: rgb("fg", (255, 0, 0)),  # #FF0000
}


def color_grade(raw_grades: list[LineWork]) -> list[LineWork]:
    grades: list[LineWork] = raw_grades.copy()
    for i, grade in enumerate(grades):
        grades[i]["subject"] = SUBJECT_COLOR + grade["subject"] + RESET_COLOR
        for i, grade_value_weight in enumerate(grade["grades"]):
            grade["grades"][i]["grade"] = (
                VALUE_COLORS[grade_value_weight["weight"]]
                + grade_value_weight["grade"]
                + RESET_COLOR
            )
    return grades


def load_grades() -> ProcessedGradeList:
    with open("grades.json", "r") as file:
        return json.load(file)


def sort_grades(grade_list: ProcessedGradeList) -> SortedGrades:
    sorted_grades: SortedGrades = {}
    for grade in grade_list:
        if grade["subject"] not in sorted_grades.keys():
            sorted_grades[grade["subject"]] = []
        sorted_grades[grade["subject"]].append(grade)
    return sorted_grades


def get_max_lenghts(
    sorted_grades: SortedGrades,
) -> tuple[int, int, int]:
    """
    takes sorted grades, outputs max lenghts of subjects, grades and averages after converting to str
    tuple[int: max_subject_len, int: max_grades_len, int: max_average_len]
    """
    subject_lenghts: list[int] = []
    grade_lenghts: list[int] = []
    for grade_key in sorted_grades.keys():
        subject_lenghts.append(len(grade_key))
        grades: list[str] = []
        for grade in sorted_grades[grade_key]:
            grades.append(grade["content"])
        grade_lenghts.append(len(" ".join(grades)) + 2)

    max_subject_len: int = max(subject_lenghts)
    max_grade_len: int = max(grade_lenghts)
    max_average_len: int = 5  # max len of average is 5, 2.125

    return (max_subject_len, max_grade_len, max_average_len)


def construct_LineWork(grades: SortedGrades) -> list[LineWork]:
    """constructs LineWork from SortedGrades"""
    constructed_grades: list[LineWork] = []
    for grade_list_key, grade_list in grades.items():
        item_subject: str = grade_list_key
        item_grades: list[GradeInfo] = []
        item_grade_values: list[float] = []
        for grade in grade_list:
            item_grades.append(
                {
                    "grade": grade["content"],
                    "weight": grade["weight"],
                    "display_len": len(grade["content"]),
                }
            )
            if grade["value"] is not None:
                for _ in range(grade["weight"]):
                    item_grade_values.append(grade["value"])
        item_average: str = str(round(mean(item_grade_values), 3))
        constructed_grades.append(
            {
                "subject": item_subject,
                "subject_len": len(item_subject),
                "grades": item_grades,
                "average": item_average,
            }
        )
    return constructed_grades


#


def format_grades(
    grades: list[LineWork], max_subject_len, max_grade_len, max_average_len
) -> list[FormattedLine]:
    formated_lines: list[FormattedLine] = []
    for grade in grades:
        subject_str: str = grade["subject"] + (
            " " * (max_subject_len - grade["subject_len"])
        )

        grades_visible_len: int = 0
        grades_visible_list: list[str] = []
        for grade_info in grade["grades"]:
            grades_visible_len += grade_info["display_len"] + 1  # + space after
            grades_visible_list.append(grade_info["grade"])
        grades_str: str = " ".join(grades_visible_list) + (
            " " * (max_grade_len - grades_visible_len)
        )  # fills empty space with spaces

        average_str: str = grade["average"].ljust(max_average_len)
        formated_lines.append(
            {"subject": subject_str, "grades": grades_str, "average": average_str}
        )
    return formated_lines


def construct_lines(
    grades: SortedGrades, max_subject_len: int, max_grade_len: int, max_average_len: int
) -> list[str]:
    uncolored_grades: list[LineWork] = construct_LineWork(grades)
    colored_grades: list[LineWork] = color_grade(uncolored_grades)
    formatted_lines: list[FormattedLine] = format_grades(
        colored_grades, max_subject_len, max_grade_len, max_average_len
    )
    for line in formatted_lines:
        print("|", line["subject"], "|", line["grades"], "|", line["average"], "|")


def dev_viz(grades: SortedGrades) -> None:
    print(get_max_lenghts(grades))
    max_lenghts: tuple[int, int, int] = get_max_lenghts(grades)
    max_subject_len: int = max_lenghts[0]
    max_grade_len: int = max_lenghts[1]
    max_average_len: int = max_lenghts[2]

    lines: list[str] = construct_lines(
        grades, max_subject_len, max_grade_len, max_average_len
    )


def vizualize_grades(grades: SortedGrades):
    viz_grades: list[LineWork] = []  # subject, grades, average
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
    ugr: ProcessedGradeList = load_grades()
    sgr: SortedGrades = sort_grades(ugr)
    dev_viz(sgr)
