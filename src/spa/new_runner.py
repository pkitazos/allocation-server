from dataclasses import dataclass
from typing import Any

from matching_problems.solver.enums import (
    Extra_constraints,
    Instance_options,
    Optimisation_options,
)
from matching_problems.solver.fileIO import import_model
from matching_problems.solver.lp_solver import LP_Solver
from matching_problems.solver.matching_details import (
    ProjectCapacities as LibProjectCapacities,
)
from matching_problems.solver.matching_details import (
    SupervisorCapacities as LibSupervisorCapacities,
)
from matching_problems.solver.result import Result
from src.hash_tables import HashTables
from src.models.algorithm_opts import CustomConfig, OptimisationCriteria
from src.models.spa_io import SpaInput
from src.server_data import ServerData

# This is the main thing I was saying I "discovered"
# I was really confused about why I was still passing in strings
# and I wanted to see where it was that she uses these strings to actually configure the solver
# and I found that the reason I was still using strings everywhere is because...
# I was still going through the arg parser!!! (why!?!?)
# anyway, even though this map looks identical, I still think we keep it so that our frontend
# doesn't depend directly on the library itnernals
OPT_MAP: dict[OptimisationCriteria, Optimisation_options] = {
    OptimisationCriteria.MAXSIZE: Optimisation_options.MAXSIZE,
    OptimisationCriteria.GEN: Optimisation_options.GENEROUS,
    OptimisationCriteria.GRE: Optimisation_options.GREEDY,
    OptimisationCriteria.MINCOST: Optimisation_options.MINCOST,
    OptimisationCriteria.MINSQCOST: Optimisation_options.MINSQCOST,
    OptimisationCriteria.LSB: Optimisation_options.LOADSUMBAL,
}


@dataclass
class _SolverArgs:
    # idk how to type this
    instance_options: dict[Instance_options, Any]
    extra_constraints: dict[Extra_constraints, bool]
    optimisation_options: list[Optimisation_options]


def _build_solver_args(cfg: CustomConfig) -> _SolverArgs:
    return _SolverArgs(
        instance_options={
            Instance_options.NUMAGENTS: 3,
            Instance_options.TWOPL: False,
            Instance_options.PC: False,
        },
        extra_constraints={Extra_constraints.STAB: False},
        optimisation_options=[OPT_MAP[f] for f in cfg.flags],
    )


# Ported from src/data_processing.py
def _to_server_data(data: SpaInput) -> ServerData:
    lecturer_id_to_int: dict[str, int] = {}
    lecturer_id_to_capacities: dict[str, LibSupervisorCapacities] = {}
    lecturer_rows: list[list[int]] = []

    for idx, sup in enumerate(data.supervisors, 1):
        lecturer_id_to_int[sup.id] = idx
        lecturer_id_to_capacities[sup.id] = LibSupervisorCapacities(
            lower_bound=sup.lower_bound,
            target=sup.target,
            upper_bound=sup.upper_bound,
        )
        lecturer_rows.append([sup.lower_bound, sup.target, sup.upper_bound])

    project_id_to_int: dict[str, int] = {}
    project_int_to_id: dict[int, str] = {}
    project_id_to_lecturer: dict[str, str] = {}
    project_id_to_capacities: dict[str, LibProjectCapacities] = {}
    project_rows: list[list[int]] = []

    for idx, proj in enumerate(data.projects, 1):
        project_id_to_int[proj.id] = idx
        project_int_to_id[idx] = proj.id
        project_id_to_lecturer[proj.id] = proj.supervisor_id
        project_id_to_capacities[proj.id] = LibProjectCapacities(
            lower_bound=proj.lower_bound,
            upper_bound=proj.upper_bound,
        )
        project_rows.append(
            [
                proj.lower_bound,
                proj.upper_bound,
                lecturer_id_to_int[proj.supervisor_id],
            ]
        )

    student_int_to_id: dict[int, str] = {}
    student_rows: list[list[int]] = []
    for idx, student in enumerate(data.students):
        student_int_to_id[idx] = student.id
        student_rows.append([project_id_to_int[p] for p in student.preferences])

    hash_tables = HashTables(
        lecturer_id_to_capacities,
        project_int_to_id,
        project_id_to_lecturer,
        project_id_to_capacities,
        student_int_to_id,
    )

    # we could probably use a better name than ServerData
    return ServerData(lecturer_rows, project_rows, student_rows, hash_tables)


# we can probably use something like this to interface with the library?
# and then hopefully nothing else needs to interface with it
# I still need to go in and gut if from the other `src.` imports
def run_via_library(cfg: CustomConfig, data: SpaInput) -> tuple[str, Result]:
    args = _build_solver_args(cfg)
    server_data = _to_server_data(data)
    model = import_model(server_data)

    lp = LP_Solver(
        model,
        args.instance_options,
        args.extra_constraints,
        args.optimisation_options,
    )
    pulp_status = lp.run(msg=False, timeLimit=None, threads=None, write=False)
    model.pulp_status = pulp_status

    result = model.get_results_object()
    if pulp_status != "Infeasible":
        result.format_result(server_data.get_hash_tables())
        result.validate()

    return pulp_status, result
