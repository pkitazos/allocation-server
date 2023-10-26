from matching_problems import solver
from fastapi import FastAPI
from pydantic import BaseModel


class InstanceData(BaseModel):
    students: list[list[int]]
    projects: list[list[int]]
    lecturers: list[list[int]]


class InstanceDataAndArgs(InstanceData):
    args: list[str]


app = FastAPI()


@app.post("/")
async def generous(data: InstanceDataAndArgs):
    args = data.args
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    print(my_solver.get_results())
    return {"message": "I am an algorithm"}


@app.post("/generous")
async def generous(data: InstanceData):
    args = ['-na', '3', '-maxsize', '1', '-gen', '2', '-lsb', '3']
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    print(my_solver.get_results())
    return {"message": "I am the generous algorithm"}


@app.post("/greedy")
async def greedy(data: InstanceData):
    args = ['-na', '3', '-maxsize', '1', '-gre', '2', '-lsb', '3']
    my_solver = solver.Solver(args, data)
    my_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    print(solver.get_results())
    return {"message": "I am the greedy algorithm"}


@app.post("/minimum-cost")
async def the_other_one(data: InstanceData):
    args = ['-na', '3', '-maxsize', '1', '-mincost', '2', '-lsb', '3']
    solver = solver.Solver(args, data)
    solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    print(solver.get_results())
    return {"message": "I am the the other algorithm"}


@app.post("/greedy-generous")
async def greedy_generous(data: InstanceData):
    return {"message": "I am the greedy-generous algorithm"}
