from typing import Optional, Union
from enum import Enum, auto

from pydantic import BaseModel


# kill this
class RequestDataWithArgs(SpaInput):
    args: list[str]


class OptimisationCriteria(Enum):
    MAXSIZE = "MAXSIZE"
    GEN = "GEN"
    GRE = "GRE"
    MINCOST = "MINCOST"
    MINSQCOST = "MINSQCOST"
    LSB = "LSB"

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


class CustomConfig(BaseModel):
    flags: Union[
        tuple[OptimisationCriteria],
        tuple[OptimisationCriteria, OptimisationCriteria],
        tuple[OptimisationCriteria, OptimisationCriteria, OptimisationCriteria],
    ]
    supervisorTargetModifier: int = 0
    supervisorUpperQuotaModifier: int = 0
    maxRank: Optional[int] = None

    def to_solver_flags(self) -> list[str]:
        return ["-na", str(len(self.flags))] + flatten(
            [[f.to_solver_flag(), str(i + 1)] for i, f in enumerate(self.flags)]
        )
