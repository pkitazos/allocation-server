import copy
from .matching_details import MatchingDetails, ProjectCapacities, SupervisorCapacities


def safe_index(d: dict, x: int, default_val=0):
    return d[x] if x != 0 else default_val


class Result:
    def __init__(self, model):
        pair_assignments = model._get_pair_assignments()
        profile = model._get_profile(pair_assignments)
        matching = list(map(int, model._get_matching_list(pair_assignments)))

        self.profile = profile
        self.degree = model._get_degree(pair_assignments)
        self.size = sum(profile)
        self.weight = sum((idx+1)*x for idx, x in enumerate(profile)),
        self.cost = model._get_cost(pair_assignments),
        self.cost_sq = model._get_cost_sq(pair_assignments)
        self.max_lec_abs_diff = model._get_max_lec_abs_diff(pair_assignments),
        self.sum_lec_abs_diff = model._get_sum_lec_abs_diff(pair_assignments),
        self.matching_list = matching
        self.matching_details = None
        self.ranks = [x.rank_student for x in pair_assignments]

    # TODO: refactor method signature
    def format_result(
            self,
            p_to_str: dict[int, str],
            s_to_str: dict[int, str],
            project_to_lecturer: dict[str, str],
            project_to_capacities: dict[str, ProjectCapacities],
            lecturer_to_capacities: dict[str, SupervisorCapacities]):

        matchups = []
        for idx, (x, r) in enumerate(zip(self.matching_list, self.ranks)):
            student_id = s_to_str[idx]
            project_id = safe_index(p_to_str, x)
            lecturer_id = safe_index(project_to_lecturer, project_id)

            project_capacities = safe_index(
                d=project_to_capacities,
                x=project_id,
                default_val=ProjectCapacities(lower_bound=0, upper_bound=0))

            supervisor_capacities = safe_index(
                d=lecturer_to_capacities,
                x=lecturer_id,
                default_val=SupervisorCapacities(lower_bound=0, target=0, upper_bound=0))

            matching_details = MatchingDetails(
                student_id=student_id,
                project_id=project_id,
                supervisor_id=lecturer_id,
                rank=r,
                project_capacities=project_capacities,
                supervisor_capacities=supervisor_capacities
            )

            matchups.append(matching_details)
        self.matching_details = copy.deepcopy(matchups)

    def to_json(self):
        return {
            "profile": self.profile,
            "degree": self.degree,
            "size": self.size,
            "weight": self.weight[0],
            "cost": self.cost[0],
            "costSq": self.cost_sq,
            "maxLecAbsDiff": self.max_lec_abs_diff[0],
            "sumLecAbsDiff": self.sum_lec_abs_diff[0],
            "matching": self.matching_details,
            "ranks": self.ranks
        }
