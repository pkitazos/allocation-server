from matching_problems import solver
from fastapi import FastAPI
from pydantic import BaseModel


class ClientMatchingData(BaseModel):
    students: list[list[str]]  # list or projectIds for each student
    # list of projects and their details
    projects: list[tuple[str, int, int, str]]
    # list of lecturers and their details
    lecturers: list[tuple[str, int, int, int]]


class ClientMatchingDataCustomArgs(ClientMatchingData):
    args: list[str]


class ServerMatchingData(BaseModel):
    students: list[list[int]]
    projects: list[list[int]]
    lecturers: list[list[int]]


app = FastAPI()


def hash_lecturers(lecturer_arr: list[tuple[str, int, int, int]]):
    to_int = {}
    to_str = {}
    lecturer_data = []
    for idx, lecturer in enumerate(lecturer_arr, 1):
        (lecturer_id, lb, t, ub) = lecturer
        to_int[lecturer_id] = idx
        to_str[idx] = lecturer_id
        lecturer_data.append([lb, t, ub])
    return (to_int, to_str, lecturer_data)


def hash_projects(project_arr: list[tuple[int, int, str]], lecturer_to_int: dict[str, int]):
    to_int = {}
    to_str = {}
    project_data = []
    for idx, project in enumerate(project_arr, 1):
        (project_id, lb, ub, lecturer_id) = project
        to_int[project_id] = idx
        to_str[idx] = project_id
        project_data.append([lb, ub, lecturer_to_int[lecturer_id]])

    return (to_int, to_str, project_data)


def hash_students(student_arr: list[list[str]], to_int: dict[str, int]) -> list[list[int]]:
    student_data = []
    for student in student_arr:
        student_data.append(list(map(lambda x: to_int[x], student)))
    return student_data


def format_matching(matching_arr: list[int], p_to_str: dict[int, str]):
    return [p_to_str[x] for x in matching_arr]


@app.post("/")
async def root(data: ClientMatchingDataCustomArgs):
    args = data.args
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    print(my_solver.get_results())
    return {"message": "I am an algorithm"}


@app.post("/generous")
async def generous(data: ClientMatchingData):
    args = ['-na', '3', '-maxsize', '1', '-gen', '2', '-lsb', '3']

    l_to_int, l_to_str, lecturer_data = hash_lecturers(data.lecturers)
    p_to_int, p_to_str, project_data = hash_projects(data.projects, l_to_int)
    student_data = hash_students(data.students, p_to_int)

    alg_data = ServerMatchingData(
        students=student_data,
        projects=project_data,
        lecturers=lecturer_data
    )

    print(alg_data)
    my_solver = solver.Solver(args, alg_data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    response_data = my_solver.get_results_object()

    matching = response_data["matching"]
    # formatted_matching = format_matching(matching, p_to_str)
    response_data["matching"] = format_matching(matching, p_to_str)
    print(f"matching solution: {response_data}")
    # print(my_solver.get_results())
    return {"message": "I am the generous algorithm", "data": response_data}


@app.post("/greedy")
async def greedy(data: ClientMatchingData):
    args = ['-na', '3', '-maxsize', '1', '-gre', '2', '-lsb', '3']
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    response_data = my_solver.get_results_object()
    print(my_solver.get_results())
    return {"message": "I am the greedy algorithm", "data": response_data}


@app.post("/minimum-cost")
async def minimum_cost(data: ClientMatchingData):
    args = ['-na', '3', '-maxsize', '1', '-mincost', '2', '-lsb', '3']
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    response_data = my_solver.get_results_object()
    print(my_solver.get_results())
    return {"message": "I am the the minimum cost algorithm", "data": response_data}


@app.post("/greedy-generous")
async def greedy_generous(data: ClientMatchingData):
    gre_args = ['-na', '3', '-maxsize', '1', '-gre', '2', '-lsb', '3']
    gre_solver = solver.Solver(gre_args, data)
    gre_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    gre_response_data = gre_solver.get_results_object()
    print(gre_response_data)

    gre_degree = gre_response_data["degree"]
    original_preferences = data.students
    new_preferences = [x[:gre_degree] for x in original_preferences]
    new_data = data.model_copy()
    new_data.students = new_preferences
    gen_args = ['-na', '3', '-maxsize', '1', '-gen', '2', '-lsb', '3']
    gen_solver = solver.Solver(gen_args, new_data)
    gen_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    response_data = gen_solver.get_results_object()
    print(gen_solver.get_results())

    return {"message": "I am the greedy-generous algorithm", "data": response_data}
