
class Result:
    def __init__(self, model):
        pair_assignments = model._get_pair_assignments()
        profile = model._get_profile(pair_assignments)
        matching = list(map(int, model._get_matching_list(pair_assignments)))

        self.size = sum(profile)
        self.profile = profile
        self.degree = model._get_degree(pair_assignments)
        self.weight = sum((idx+1)*x for idx, x in enumerate(profile))
        self.ranks = [x.rank_student for x in pair_assignments]
        self.matching = matching

    def format_result(self, p_to_str: dict[int, str], s_to_str: dict[int, str]):
        matching_pairs = []
        for idx, (x, r) in enumerate(zip(self.matching, self.ranks)):
            matching_pairs.append((s_to_str[idx], p_to_str[x], r))
        self.matching = matching_pairs

    def to_json(self):
        return {
            "size": self.size,
            "profile": self.profile,
            "degree": self.degree,
            "weight": self.weight,
            "ranks": self.ranks,
            "matching": self.matching
        }
