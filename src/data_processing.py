from matching_problems.solver.matching_details import (
    ProjectCapacities,
    SupervisorCapacities,
)
from src.request_data import ProjectData, RequestData, StudentData, SupervisorData
from src.hash_tables import HashTables

def process_lecturer_data(
    lecturer_arr: list[SupervisorData],
) -> tuple[dict[str, int], dict[str, SupervisorCapacities], list[list[int]]]:
    lecturer__id_to_int: dict[str, int] = {}
    lecturer__id_to_capacities: dict[str, SupervisorCapacities] = {}
    lecturer__processed_data: list[list[int]] = []

    for idx, lecturer in enumerate(lecturer_arr, 1):
        lecturer__id_to_int[lecturer.id] = idx
        lecturer__id_to_capacities[lecturer.id] = SupervisorCapacities(
            lower_bound=lecturer.lowerBound,
            target=lecturer.target,
            upper_bound=lecturer.upperBound,
        )
        lecturer__processed_data.append([
            lecturer.lowerBound,
            lecturer.target,
            lecturer.upperBound,
        ])

    return (
        lecturer__id_to_int,
        lecturer__id_to_capacities,
        lecturer__processed_data,
    )


def process_project_data(
    project_arr: list[ProjectData], lecturer__id_to_int: dict[str, int]
) -> tuple[
    dict[str, int],
    dict[int, str],
    dict[str, str],
    dict[str, ProjectCapacities],
    list[list[int]],
]:
    project__id_to_int: dict[str, int] = {}
    project__int_to_id: dict[int, str] = {}
    project__id_to_lecturer: dict[str, str] = {}
    project__id_to_capacities: dict[str, ProjectCapacities] = {}
    project__processed_data: list[list[int]] = []

    for idx, project in enumerate(project_arr, 1):
        project__id_to_int[project.id] = idx
        project__int_to_id[idx] = project.id

        project__id_to_lecturer[project.id] = project.supervisorId
        project__id_to_capacities[project.id] = ProjectCapacities(
            lower_bound=project.lowerBound,
            upper_bound=project.upperBound,
        )
        project__processed_data.append([
            project.lowerBound,
            project.upperBound,
            lecturer__id_to_int[project.supervisorId],
        ])

    return (
        project__id_to_int,
        project__int_to_id,
        project__id_to_lecturer,
        project__id_to_capacities,
        project__processed_data,
    )


def process_student_data(
    student_arr: list[StudentData], project__id_to_int: dict[str, int]
) -> tuple[dict[int, str], list[list[int]]]:
    student__int_to_id: dict[int, str] = {}
    student__processed_data: list[list[int]] = []

    for idx, student in enumerate(student_arr):
        data = [project__id_to_int[x] for x in student.preferences]
        student__processed_data.append(data)
        student__int_to_id[idx] = student.id

    return (
        student__int_to_id,
        student__processed_data,
    )


def process_request_data(
    data: RequestData,
) -> tuple[list[int], list[int], list[int], HashTables]:

    (
        lecturer__id_to_int,
        lecturer__id_to_capacities,
        lecturer__processed_data,
    ) = process_lecturer_data(data.supervisors)

    (
        project__id_to_int,
        project__int_to_id,
        project__id_to_lecturer,
        project__id_to_capacities,
        project__processed_data,
    ) = process_project_data(data.projects, lecturer__id_to_int)

    (
        student__int_to_id,
        student__processed_data,
    ) = process_student_data(data.students, project__id_to_int)

    hash_tables = HashTables(
        lecturer__id_to_capacities,
        project__int_to_id,
        project__id_to_lecturer,
        project__id_to_capacities,
        student__int_to_id,
    )

    return (
        lecturer__processed_data,
        project__processed_data,
        student__processed_data,
        hash_tables,
    )

