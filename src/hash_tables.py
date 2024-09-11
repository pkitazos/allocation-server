class HashTables:
    def __init__(
        self,
        lecturer__id_to_capacities,
        project__int_to_id,
        project__id_to_lecturer,
        project__id_to_capacities,
        student__int_to_id,
    ):
        self.lecturer__id_to_capacities = lecturer__id_to_capacities
        self.project__int_to_id = project__int_to_id
        self.project__id_to_lecturer = project__id_to_lecturer
        self.project__id_to_capacities = project__id_to_capacities
        self.student__int_to_id = student__int_to_id
