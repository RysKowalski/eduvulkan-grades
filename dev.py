import json
from statistics import mean
from typing import Literal
from typing_stuff import (
    FormattedLine,
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
BOLD: str = "\033[1m"

SUBJECT_COLOR: str = rgb("fg", fg=(19, 255, 255))  # #14FFFF
VALUE_COLORS: dict[int, str] = {
    1: "",
    2: rgb("fg", (0, 255, 0)),  # #00FF00
    3: rgb("fg", (255, 0, 0)),  # #FF0000
}

# #FF0000 #ED7835 #F8D448 #D2F950 #94FA4E #00FB00
AVERAGE_COLORS: dict[int, str] = {
    1: rgb("both", (0, 255, 255), (255, 0, 0)) + BOLD,
    2: rgb("fg", (237, 120, 53)),
    3: rgb("fg", (248, 212, 72)),
    4: rgb("fg", (210, 249, 80)),
    5: rgb("fg", (148, 250, 78)),
    6: rgb("both", (237, 120, 53), (148, 250, 78)) + BOLD,
}


def color_grade(raw_grades: list[LineWork]) -> list[LineWork]:
    grades: list[LineWork] = raw_grades.copy()
    for i, grade in enumerate(grades):
        grades[i]["subject"] = SUBJECT_COLOR + grade["subject"] + RESET_COLOR
        for j, grade_value_weight in enumerate(grade["grades"]):
            grade["grades"][j]["grade"] = (
                VALUE_COLORS[grade_value_weight["weight"]]
                + grade_value_weight["grade"]
                + RESET_COLOR
            )
        print(grade["average"], i)
        grades[i]["average"] = (
            AVERAGE_COLORS[int(float(grade["average"]))]
            + grade["average"]
            + RESET_COLOR
        )
    return grades


def load_grades() -> ProcessedGradeList:
    with open("grades.json", "r") as file:
        grades: ProcessedGradeList = json.load(file)
    return sorted(grades, key=lambda g: g["subject"])


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


def construct_LineWork(
    grades: SortedGrades,
    max_subject_len: int,
    max_grades_len: int,
    max_average_len: int,
) -> list[LineWork]:
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
                "average_len": len(item_average),
            }
        )
    return constructed_grades


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

        average_str: str = grade["average"] + (
            " " * (max_average_len - grade["average_len"])
        )
        formated_lines.append(
            {
                "subject": subject_str,
                "grades": grades_str,
                "average": average_str,
                "subject_len": max_subject_len + 2,
                "grades_len": max_grade_len + 2,
                "average_len": max_average_len + 2,
            }
        )
    return formated_lines


def construct_lines(
    grades: SortedGrades, max_subject_len: int, max_grade_len: int, max_average_len: int
) -> list[str]:
    uncolored_grades: list[LineWork] = construct_LineWork(
        grades, max_subject_len, max_grade_len, max_average_len
    )
    colored_grades: list[LineWork] = color_grade(uncolored_grades)
    formatted_lines: list[FormattedLine] = format_grades(
        colored_grades, max_subject_len, max_grade_len, max_average_len
    )
    done_lines: list[str] = []
    for line in formatted_lines:
        done_lines.append(
            f"| {line['subject']} | {line['grades']} | {line['average']} |"
        )
    return done_lines


def construct_separator(subject_len: int, grades_len: int, average_len: int) -> str:
    return f"+{'-' * (subject_len + 2)}+{'-' * (grades_len + 1)}+{'-' * (average_len + 2)}+"


def vizualize(grades: SortedGrades) -> None:
    max_lenghts: tuple[int, int, int] = get_max_lenghts(grades)
    max_subject_len: int = max_lenghts[0]
    max_grade_len: int = max_lenghts[1]
    max_average_len: int = max_lenghts[2]

    lines: list[str] = construct_lines(
        grades, max_subject_len, max_grade_len, max_average_len
    )
    separator: str = construct_separator(
        max_subject_len, max_grade_len, max_average_len
    )

    print(separator)
    for line in lines:
        print(line)
        print(separator)


if __name__ == "__main__":
    ugr: ProcessedGradeList = load_grades()
    sgr: SortedGrades = sort_grades(ugr)
    vizualize(sgr)
