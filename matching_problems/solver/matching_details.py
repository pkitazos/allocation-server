from pydantic import BaseModel


class ProjectCapacities(BaseModel):
    lower_bound: int
    upper_bound: int


class SupervisorCapacities(BaseModel):
    lower_bound: int
    target: int
    upper_bound: int


class MatchingDetails:
    student_id: str
    project_id: str
    project_capacities: ProjectCapacities
    preference_rank: int
    supervisor_id: str
    supervisor_capacities: SupervisorCapacities

    def __init__(
        self,
        student_id,
        project_id,
        supervisor_id,
        rank,
        project_capacities,
        supervisor_capacities
    ):
        self.student_id = student_id
        self.project_id = project_id
        self.supervisor_id = supervisor_id
        self.preference_rank = rank
        self.project_capacities = project_capacities
        self.supervisor_capacities = supervisor_capacities
