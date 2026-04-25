from typing import Generic, TypeVar, Type

from pydantic import BaseModel
from pydantic.generics import GenericModel


class StudentData(BaseModel):
    id: str
    preferences: list[str]


class ProjectCapacities(BaseModel):
    id: str
    lowerBound: int
    upperBound: int
    supervisorId: str


class SupervisorCapacities(BaseModel):
    id: str
    lowerBound: int
    target: int
    upperBound: int


class SpaInput(BaseModel):
    students: list[StudentData]
    """list of students and their preferences"""

    projects: list[ProjectCapacities]
    """list of projects and their capacity constraints"""

    supervisors: list[SupervisorCapacities]
    """list of lecturers and their capacity constraints"""


# --- these get sent over the wire


class Match(BaseModel):
    studentId: str
    projectId: str
    projectCapacities: ProjectCapacities
    preferenceRank: int
    supervisorId: str
    supervisorCapacities: SupervisorCapacities


class SpaOutput(BaseModel):
    profile: list[int]
    degree: int
    size: int
    weight: int
    cost: int
    costSq: int
    maxLecAbsDif: int
    sumLecAbsDiff: int
    matchingPairs: list[tuple[str, str]]
    matchingDetails: list[Match]
    ranks: list[int]
