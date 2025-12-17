from typing import TypedDict, Optional


class DateInfo(TypedDict):
    Timestamp: int
    Date: str
    DateDisplay: str
    Time: str


class PersonInfo(TypedDict):
    Id: int
    Surname: str
    Name: str
    DisplayName: str


class SubjectInfo(TypedDict):
    Id: int
    Key: str
    Name: str
    Kod: str
    Position: int


class CategoryInfo(TypedDict):
    Id: int
    Name: str
    Code: str


class ColumnInfo(TypedDict):
    Id: int
    Key: str
    PeriodId: int
    Name: str
    Code: str
    Group: str
    Number: int
    Color: int
    Weight: int
    Subject: SubjectInfo
    Category: CategoryInfo


class GradeItem(TypedDict):
    Id: int
    Key: str
    PupilId: int
    ContentRaw: str
    Content: str
    Comment: str
    Value: int
    Numerator: Optional[int]
    Denominator: Optional[int]
    DateCreated: DateInfo
    CreatedAt: str
    DateModify: DateInfo
    ModifiedAt: str
    Creator: PersonInfo
    Modifier: PersonInfo
    Column: ColumnInfo
    CorrectedGrade: Optional[int]


# The full JSON is a list of GradeItem:
GradeList = list[GradeItem]


class ProcessedGrade(TypedDict):
    """
    subject: str
    value: float | None
    content: str
    weight: int
    edited: int
    """

    subject: str
    value: float | None
    content: str
    weight: int
    edited: int


ProcessedGradeList = list[ProcessedGrade]


class GradeInfo(TypedDict):
    """
    grade: str
    weight: int
    display_len: int
    """

    grade: str
    weight: int
    display_len: int


class LineWork(TypedDict):
    """
    subject: str
    grades: list[{"grade": str, "weight": int}]
    average: str
    """

    subject: str
    grades: list[GradeInfo]
    average: str


class FormatedLine(TypedDict):
    """
    subject: str
    grades: str
    average: str
    """

    subject: str
    grades: str
    average: str


class VizGrades(TypedDict):
    subject: str
    grades: list[str]
    average: str


SortedGrades = dict[str, ProcessedGradeList]
