from fastapi import FastAPI
from src.data_processing import process_request_data
from src.utils import run_solver, process_matching_result
from src.server_response import ServerResponse
from src.solver_args import Args
from src.request_data import RequestData, RequestDataWithArgs
from src.server_data import ServerData


app = FastAPI()


@app.post("/")
async def root(data: RequestDataWithArgs):
    processed_request = process_request_data(data)
    processing_data = ServerData(*processed_request)
    status, result = run_solver(processing_data, data.args)

    if status == "Infeasible":
        return ServerResponse.infeasible()

    response = process_matching_result(status, result, processing_data)
    return response.to_json()


@app.post("/generous")
async def generous(data: RequestData):
    processed_request = process_request_data(data)
    processing_data = ServerData(*processed_request)
    status, result = run_solver(processing_data, Args.GENEROUS)

    if status == "Infeasible":
        return ServerResponse.infeasible()

    response = process_matching_result(status, result, processing_data)
    return response.to_json()


@app.post("/greedy")
async def greedy(data: RequestData):
    processed_request = process_request_data(data)
    processing_data = ServerData(*processed_request)
    status, result = run_solver(processing_data, Args.GREEDY)

    if status == "Infeasible":
        return ServerResponse.infeasible()

    response = process_matching_result(status, result, processing_data)
    return response.to_json()


@app.post("/minimum-cost")
async def minimum_cost(data: RequestData):
    processed_request = process_request_data(data)
    processing_data = ServerData(*processed_request)
    status, result = run_solver(processing_data, Args.MINCOST)

    if status == "Infeasible":
        return ServerResponse.infeasible()

    response = process_matching_result(status, result, processing_data)
    return response.to_json()


@app.post("/greedy-generous")
async def greedy_generous(data: RequestData):
    processed_request = process_request_data(data)
    processing_data = ServerData(*processed_request)
    gre_status, gre_result = run_solver(processing_data, Args.GREEDY)

    if gre_status == "Infeasible":
        return ServerResponse.infeasible()

    processing_data.truncate(gre_result.degree)
    status, result = run_solver(processing_data, Args.GENEROUS)

    if status == "Infeasible":
        return ServerResponse.infeasible()

    response = process_matching_result(status, result, processing_data)
    return response.to_json()
