from typing import Self

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class WireModel(BaseModel):
    """Base for any model that crosses the wire — snake_case in Python, camelCase in JSON."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class StudentData(WireModel):
    id: str
    preferences: list[str]

    def truncate(self, degree: int) -> Self:
        self.preferences = self.preferences[:degree]
        return self


class ProjectCapacities(WireModel):
    id: str
    lower_bound: int
    upper_bound: int
    supervisor_id: str


class SupervisorCapacities(WireModel):
    id: str
    lower_bound: int
    target: int
    upper_bound: int

    def mod_target(self, modifier: int) -> Self:
        self.target += modifier
        return self

    def mod_upper_bound(self, modifier: int) -> Self:
        self.upper_bound += modifier
        return self


class SpaInput(WireModel):
    """Input data for an instance of the SPA problem"""

    students: list[StudentData]
    """list of students and their preferences"""

    projects: list[ProjectCapacities]
    """list of projects and their capacity constraints"""

    supervisors: list[SupervisorCapacities]
    """list of lecturers and their capacity constraints"""

    def truncate(self, degree: int) -> Self:
        self.students = [s.truncate(degree) for s in self.students]
        return self

    def mod_supervisor_target(self, modifier: int) -> Self:
        self.supervisors = [s.mod_target(modifier) for s in self.supervisors]
        return self

    def mod_supervisor_upper_bound(self, modifier: int) -> Self:
        self.supervisors = [s.mod_upper_bound(modifier) for s in self.supervisors]
        return self


# --- these get sent over the wire


class Match(WireModel):
    student_id: str
    project_id: str
    project_capacities: ProjectCapacities
    preference_rank: int
    supervisor_id: str
    supervisor_capacities: SupervisorCapacities


class SpaOutput(WireModel):
    profile: list[int]
    degree: int
    size: int
    weight: int
    cost: int
    cost_sq: int
    max_lec_abs_diff: int
    sum_lec_abs_diff: int
    matching_pairs: list[tuple[str, str]]
    matching_details: list[Match]
    ranks: list[int]
