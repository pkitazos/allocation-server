from matching_problems import solver
from fastapi import FastAPI
from pydantic import BaseModel


class MatchingData(BaseModel):
    students: list[list[int]]
    projects: list[list[int]]
    lecturers: list[list[int]]


class MatchingDataCustomArgs(MatchingData):
    args: list[str]


app = FastAPI()


@app.post("/")
async def generous(data: MatchingDataCustomArgs):
    args = data.args
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    print(my_solver.get_results())
    return {"message": "I am an algorithm"}


@app.post("/generous")
async def generous(data: MatchingData):
    args = ['-na', '3', '-maxsize', '1', '-gen', '2', '-lsb', '3']
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    response_data = my_solver.get_results_object()
    print(my_solver.get_results())
    return {"message": "I am the generous algorithm", "data": response_data}


@app.post("/greedy")
async def greedy(data: MatchingData):
    args = ['-na', '3', '-maxsize', '1', '-gre', '2', '-lsb', '3']
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    response_data = my_solver.get_results_object()
    print(my_solver.get_results())
    return {"message": "I am the greedy algorithm", "data": response_data}


@app.post("/minimum-cost")
async def minimum_cost(data: MatchingData):
    args = ['-na', '3', '-maxsize', '1', '-mincost', '2', '-lsb', '3']
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    response_data = my_solver.get_results_object()
    print(my_solver.get_results())
    return {"message": "I am the the minimum cost algorithm", "data": response_data}


@app.post("/greedy-generous")
async def greedy_generous(data: MatchingData):
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
