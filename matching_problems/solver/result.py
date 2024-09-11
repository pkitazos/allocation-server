import copy

from src.hash_tables import HashTables
from .matching_details import MatchingDetails, ProjectCapacities, SupervisorCapacities


def safe_index(d: dict, x: int, default_val=0):
    return d[x] if x in d else default_val


class Result:
    def __init__(self, model):
        pair_assignments = model._get_pair_assignments()
        profile = model._get_profile(pair_assignments)
        matching = list(map(int, model._get_matching_list(pair_assignments)))

        self.profile = profile
        self.degree = model._get_degree(pair_assignments)
        self.size = sum(profile)
        self.weight = sum((idx + 1) * x for idx, x in enumerate(profile))
        self.cost = model._get_cost(pair_assignments)
        self.cost_sq = model._get_cost_sq(pair_assignments)
        self.max_lec_abs_diff = model._get_max_lec_abs_diff(pair_assignments)
        self.sum_lec_abs_diff = model._get_sum_lec_abs_diff(pair_assignments)
        self.matching_list = matching
        self.matching_details = None
        self.ranks = [x.rank_student for x in pair_assignments]

    def format_result(self, h:HashTables):
        matchups = []
        for idx, (x, r) in enumerate(zip(self.matching_list, self.ranks)):
            student_id = h.student__int_to_id[idx]
            project_id = safe_index(h.project__int_to_id, x, "0")
            lecturer_id = safe_index(h.project__id_to_lecturer, project_id, "0")

            project_capacities = safe_index(
                d=h.project__id_to_capacities,
                x=project_id,
                default_val=ProjectCapacities(lower_bound=0, upper_bound=0),
            )

            supervisor_capacities = safe_index(
                d=h.lecturer__id_to_capacities,
                x=lecturer_id,
                default_val=SupervisorCapacities(
                    lower_bound=0, target=0, upper_bound=0
                ),
            )

            matching_details = MatchingDetails(
                student_id=student_id,
                project_id=project_id,
                supervisor_id=lecturer_id,
                rank=r,
                project_capacities=project_capacities,
                supervisor_capacities=supervisor_capacities,
            )

            matchups.append(matching_details)
        self.matching_details = copy.deepcopy(matchups)

    def validate(self):
        new_profile = [0 for _ in self.profile]
        new_matching_details = []
        for  matched_pair in self.matching_details:
            if matched_pair.project_id == "0":
                continue
            new_profile[matched_pair.preference_rank - 1] += 1
            new_matching_details.append(matched_pair)
        
        self.profile = new_profile
        self.size = sum(self.profile)
        self.weight = sum((idx + 1) * x for idx, x in enumerate(self.profile))
        self.matching_details = new_matching_details


    def to_json(self):
        return {
            "profile": self.profile,
            "degree": self.degree,
            "size": self.size,
            "weight": self.weight,
            "cost": self.cost,
            "costSq": self.cost_sq,
            "maxLecAbsDiff": self.max_lec_abs_diff,
            "sumLecAbsDiff": self.sum_lec_abs_diff,
            "matching": self.matching_details,
            "ranks": self.ranks,
        }

    def display(self):
        print(f"profile: {self.profile}")
        print(f"degree: {self.degree}")
        print(f"size: {self.size}")
        print(f"weight: {self.weight}")
        print(f"cost: {self.cost}")
        print(f"costSq: {self.cost_sq}")
        print(f"maxLecAbsDiff: {self.max_lec_abs_diff}")
        print(f"sumLecAbsDiff: {self.sum_lec_abs_diff}")
        print(f"ranks: {self.ranks}")
        print("matching: [")
        for res in self.matching_details:
            print(f"student: {res.student_id}, project: {res.project_id}, lecturer: {res.supervisor_id}, rank: {res.preference_rank}")
        print("]")
    
