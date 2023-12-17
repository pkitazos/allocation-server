from pydantic import BaseModel


class RequestData(BaseModel):
    # list or projectIds for each student
    students: list[list[str]]
    # list of projects and their details
    projects: list[tuple[str, int, int, str]]
    # list of lecturers and their details
    lecturers: list[tuple[str, int, int, int]]


class RequestDataWithArgs(RequestData):
    args: list[str]
