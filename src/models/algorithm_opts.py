from enum import Enum

from src.models.spa_io import WireModel


class OptimisationCriteria(Enum):
    MAXSIZE = "MAXSIZE"
    GEN = "GEN"
    GRE = "GRE"
    MINCOST = "MINCOST"
    MINSQCOST = "MINSQCOST"
    LSB = "LSB"

    # the new_runner map, sorta makes this pointless
    def to_solver_flag(self) -> str:
        match self:
            case OptimisationCriteria.MAXSIZE:
                return "-maxsize"
            case OptimisationCriteria.GEN:
                return "-gen"
            case OptimisationCriteria.GRE:
                return "-gre"
            case OptimisationCriteria.MINCOST:
                return "-mincost"
            case OptimisationCriteria.MINSQCOST:
                return "-minsqcost"
            case OptimisationCriteria.LSB:
                return "-lsb"


class CustomConfig(WireModel):
    flags: (
        tuple[OptimisationCriteria]
        | tuple[OptimisationCriteria, OptimisationCriteria]
        | tuple[OptimisationCriteria, OptimisationCriteria, OptimisationCriteria]
    )

    supervisor_target_modifier: int = 0
    supervisor_upper_quota_modifier: int = 0
    max_rank: int | None = None

    # and this probably
    def to_solver_flags(self) -> list[str]:
        args: list[str] = []
        for i, f in enumerate(self.flags, start=2):
            args.append(f.to_solver_flag())
            args.append(str(i))
        return args
