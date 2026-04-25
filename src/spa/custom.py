from src.models.algorithm_opts import CustomConfig
from src.models.spa_io import SpaInput, SpaOutput

from fastapi import APIRouter

spa_router = APIRouter()


@spa_router.post("/custom")
def runCustom(config: CustomConfig, data: SpaInput) -> SpaOutput:
    if config.maxRank != null:
        data = data.truncate(config.maxRank)

    if config.supervisorTargetModifier != 0:
        data = data.modSupervisorTarget(config.supervisorTargetModifier)

    if config.supervisorUpperQuotaModifier != 0:
        data = data.modSupervisorUpperBound(config.supervisorUpperQuotaModifier)

    flags = config.to_solver_flags()

    solve(flags, data)
    ...


@spa_router.post("/generous")
def generous(data: SpaInput) -> SpaOutput:
    # GENEROUS = ["-na", "3", "-maxsize", "1", "-gen", "2", "-lsb", "3"]
    config = CustomConfig(
        flags=[
            OptimisationCriteria.MAXSIZE,
            OptimisationCriteria.GEN,
            OptimisationCriteria.LSB,
        ]
    )
    return runCustom(config, data)


@spa_router.post("/greedy")
def greedy(data: SpaInput) -> SpaOutput:
    # GREEDY = ["-na", "3", "-maxsize", "1", "-gre", "2", "-lsb", "3"]
    config = CustomConfig(
        flags=[
            OptimisationCriteria.MAXSIZE,
            OptimisationCriteria.GRE,
            OptimisationCriteria.LSB,
        ]
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
        flags=[
            OptimisationCriteria.MAXSIZE,
            OptimisationCriteria.MINCOST,
            OptimisationCriteria.LSB,
        ]
    )
    return runCustom(Args.MINCOST, data)
