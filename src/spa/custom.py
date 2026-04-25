from fastapi import APIRouter

from src.models.algorithm_opts import CustomConfig, OptimisationCriteria
from src.models.spa_io import SpaInput, SpaOutput

spa_router = APIRouter()


@spa_router.post("/custom")
def runCustom(config: CustomConfig, data: SpaInput) -> SpaOutput:
    if config.max_rank != None:
        data = data.truncate(config.max_rank)

    if config.supervisor_target_modifier != 0:
        data = data.mod_supervisor_target(config.supervisor_target_modifier)

    if config.supervisor_upper_quota_modifier != 0:
        data = data.mod_supervisor_target(config.supervisor_upper_quota_modifier)

    flags = config.to_solver_flags()

    # solve(flags, data)
    ...


@spa_router.post("/generous")
def generous(data: SpaInput) -> SpaOutput:
    # GENEROUS = ["-na", "3", "-maxsize", "1", "-gen", "2", "-lsb", "3"]
    config = CustomConfig(
        flags=(
            OptimisationCriteria.MAXSIZE,
            OptimisationCriteria.GEN,
            OptimisationCriteria.LSB,
        )
    )
    return runCustom(config, data)


@spa_router.post("/greedy")
def greedy(data: SpaInput) -> SpaOutput:
    # GREEDY = ["-na", "3", "-maxsize", "1", "-gre", "2", "-lsb", "3"]
    config = CustomConfig(
        flags=(
            OptimisationCriteria.MAXSIZE,
            OptimisationCriteria.GRE,
            OptimisationCriteria.LSB,
        )
    )
    return runCustom(config, data)


@spa_router.post("/greedy-generous")
def greedy_generous(data: SpaInput) -> SpaOutput:
    round1 = greedy(data)

    data = data.truncate(round1.degree)

    return generous(data)


@spa_router.post("/min-cost")
def mincost(data: SpaInput) -> SpaOutput:
    # MINCOST = ["-na", "3", "-maxsize", "1", "-mincost", "2", "-lsb", "3"]
    config = CustomConfig(
        flags=(
            OptimisationCriteria.MAXSIZE,
            OptimisationCriteria.MINCOST,
            OptimisationCriteria.LSB,
        )
    )
    return runCustom(Args.MINCOST, data)
