from fastapi import FastAPI
from matching_problems import solver
from src.server_response import ServerResponse
from src.solver_args import Args
from src.request_data import RequestData, RequestDataWithArgs
from src.server_data import ServerData


app = FastAPI()


def run_solver(args: list[str], data: ServerData):
    matching_solver = solver.Solver(args, data)
    matching_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    print(matching_solver.get_results())
    solver_status = matching_solver.model.pulp_status
    return solver_status, matching_solver.get_results_object()


@app.post("/")
async def root(data: RequestDataWithArgs):
    args = data.args
    req_data = RequestData(
        students=data.students, projects=data.projects, supervisors=data.supervisors
    )
    processing_data = ServerData(req_data)
    status, result = run_solver(args, processing_data)
    if status == "Infeasible":
        return ServerResponse.infeasible()
    
    result.format_result(processing_data.get_hash_tables())
    result.validate()
    result.display()

    response = ServerResponse(status, data=result.to_json())
    return response.to_json()


@app.post("/generous")
async def generous(data: RequestData):
    processing_data = ServerData(data)
    status, result = run_solver(Args.GENEROUS, processing_data)
    if status == "Infeasible":
        return ServerResponse.infeasible()
    
    result.format_result(processing_data.get_hash_tables())
    result.validate()
    result.display()

    response = ServerResponse(status, data=result.to_json())
    return response.to_json()


@app.post("/greedy")
async def greedy(data: RequestData):
    processing_data = ServerData(data)
    status, result = run_solver(Args.GREEDY, processing_data)
    if status == "Infeasible":
        return ServerResponse.infeasible()
    
    result.format_result(processing_data.get_hash_tables())
    result.validate()
    result.display()

    response = ServerResponse(status, data=result.to_json())
    return response.to_json()


@app.post("/minimum-cost")
async def minimum_cost(data: RequestData):
    processing_data = ServerData(data)
    status, result = run_solver(Args.MINCOST, processing_data)
    if status == "Infeasible":
        return ServerResponse.infeasible()
    
    result.format_result(processing_data.get_hash_tables())
    result.validate()
    result.display()

    response = ServerResponse(status, data=result.to_json())
    return response.to_json()


@app.post("/greedy-generous")
async def greedy_generous(data: RequestData):
    processing_data = ServerData(data)
    gre_status, gre_result = run_solver(Args.GREEDY, processing_data)
    if gre_status == "Infeasible":
        return ServerResponse.infeasible()
    
    processing_data.truncate(gre_result.degree)
    status, result = run_solver(Args.GENEROUS, processing_data)
    if status == "Infeasible":
        return ServerResponse.infeasible()
    
    result.format_result(processing_data.get_hash_tables())
    result.validate()
    result.display()
    
    response = ServerResponse(status, data=result.to_json())
    return response.to_json()
