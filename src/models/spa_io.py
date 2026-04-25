from typing import Generic, TypeVar, Type

from pydantic import BaseModel
from pydantic.generics import GenericModel


class StudentData(BaseModel):
    id: str
    preferences: list[str]

    def truncate(self, degree: int):
        self.preferences = self.preferences[:degree]
        return self


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

    def modTarget(self, modifier: int):
        self.target += modifier
        return self

    def modUpperBound(self, modifier: int):
        self.upperBound += modifier
        return self


class SpaInput(BaseModel):
    """Input data for an instance of the SPA problem"""

    students: list[StudentData]
    """list of students and their preferences"""

    projects: list[ProjectCapacities]
    """list of projects and their capacity constraints"""

    supervisors: list[SupervisorCapacities]
    """list of lecturers and their capacity constraints"""

    def truncate(self, degree: int):
        self.students = [s.truncate(degree) for s in self.students]
        return self

    def modSupervisorTarget(self, modifier: int):
        self.supervisors = [s.modTarget(modifier) for s in self.supervisors]
        return self

    def modSupervisorUpperBound(self, modifier: int):
        self.supervisors = [s.modUpperBound(modifier) for s in self.supervisors]
        return self


# --- these get sent over the wire


class Match(BaseModel):
    studentId: str
    projectId: str
    projectCapacities: ProjectCapacities
    preferenceRank: int
    supervisorId: str
    supervisorCapacities: SupervisorCapacities


class SpaOutput(BaseModel):
    """..."""

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
