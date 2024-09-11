from matching_problems import solver
from matching_problems.solver.result import Result
from src.server_response import ServerResponse
from src.server_data import ServerData



def run_solver(processing_data: ServerData, args: list[str]) -> tuple[str, Result]:
    processing_data.display()  

    matching_solver = solver.Solver(args, processing_data)
    matching_solver.solve(msg=False, timeLimit=None, threads=None, write=False)
    print(matching_solver.get_results()) 

    solver_status = matching_solver.model.pulp_status
    return solver_status, matching_solver.get_results_object()


def process_matching_result(
    status: str, result: Result, processing_data: ServerData
) -> ServerResponse:
    result.format_result(processing_data.get_hash_tables())
    result.validate()
    result.display()

    return ServerResponse(status, data=result.to_json())
