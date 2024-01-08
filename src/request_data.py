from pydantic import BaseModel


class StudentData(BaseModel):
    id: str
    preferences: list[str]


class ProjectData(BaseModel):
    id: str
    lowerBound: int
    upperBound: int
    supervisorId: str


class SupervisorData(BaseModel):
    id: str
    lowerBound: int
    target: int
    upperBound: int


class RequestData(BaseModel):
    # list or projectIds for each student
    students: list[StudentData]
    # list of projects and their details
    projects: list[ProjectData]
    # list of lecturers and their details
    supervisors: list[SupervisorData]


class RequestDataWithArgs(RequestData):
    args: list[str]
