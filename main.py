from fastapi import FastAPI
from matching_problems import solver
from src.solver_args import Args
from src.request_data import RequestData, RequestDataWithArgs
from src.server_data import ServerData


app = FastAPI()


def run_solver(args: list[str], data: ServerData):
    matching_solver = solver.Solver(args, data)
    matching_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    print(matching_solver.get_results())
    return matching_solver.get_results_object()


@app.post("/")
async def root(data: RequestDataWithArgs):
    args = data.args
    req_data = RequestData(
        students=data.students, projects=data.projects, supervisors=data.supervisors
    )
    processing_data = ServerData(req_data)
    result = run_solver(args, processing_data)
    result.format_result(processing_data.get_hash_tables())

    result.display()
    return {"message": "I am an algorithm", "data": result.to_json()}


@app.post("/generous")
async def generous(data: RequestData):
    processing_data = ServerData(data)
    result = run_solver(Args.GENEROUS, processing_data)
    result.format_result(processing_data.get_hash_tables())

    result.display()
    return {"message": "I am the generous algorithm", "data": result.to_json()}


@app.post("/greedy")
async def greedy(data: RequestData):
    processing_data = ServerData(data)
    result = run_solver(Args.GREEDY, processing_data)
    result.format_result(processing_data.get_hash_tables())

    result.display()
    return {"message": "I am the greedy algorithm", "data": result.to_json()}


@app.post("/minimum-cost")
async def minimum_cost(data: RequestData):
    processing_data = ServerData(data)
    result = run_solver(Args.MINCOST, processing_data)
    result.format_result(processing_data.get_hash_tables())

    result.display()
    return {"message": "I am the the minimum cost algorithm", "data": result.to_json()}


@app.post("/greedy-generous")
async def greedy_generous(data: RequestData):
    processing_data = ServerData(data)
    gre_result = run_solver(Args.GREEDY, processing_data)

    processing_data.truncate(gre_result.degree)
    result = run_solver(Args.GENEROUS, processing_data)
    result.format_result(processing_data.get_hash_tables())

    result.display()
    return {"message": "I am the greedy-generous algorithm", "data": result.to_json()}
