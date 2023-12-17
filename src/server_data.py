from src.request_data import RequestData


class ServerData:

    def __init__(self, data: RequestData):
        self.l_to_int = None
        self.p_to_int = None
        self.p_to_str = None
        self.s_to_str = None
        self.lecturers = self.process_lecturers(data.lecturers)
        self.projects = self.process_projects(data.projects)
        self.students = self.process_students(data.students)

    def process_lecturers(self, lecturer_arr: list[tuple[str, int, int, int]]):
        to_int = {}
        lecturer_data = []
        for idx, lecturer in enumerate(lecturer_arr, 1):
            (lecturer_id, lb, t, ub) = lecturer
            to_int[lecturer_id] = idx
            lecturer_data.append([lb, t, ub])

        self.l_to_int = to_int
        return lecturer_data

    def process_projects(self, project_arr: list[tuple[int, int, str]]):
        to_int = {}
        to_str = {}
        project_data = []
        for idx, project in enumerate(project_arr, 1):
            (project_id, lb, ub, lecturer_id) = project
            to_int[project_id] = idx
            to_str[idx] = project_id
            project_data.append([lb, ub, self.l_to_int[lecturer_id]])

        self.p_to_int = to_int
        self.p_to_str = to_str
        return project_data

    def process_students(self, student_arr: list[list[str]]):
        student_data = []
        to_str = {}
        for idx, (student_id, *student) in enumerate(student_arr):
            student_data.append(list(map(lambda x: self.p_to_int[x], student)))
            to_str[idx] = student_id

        self.s_to_str = to_str
        return student_data

    def truncate(self, degree: int):
        student_data = self.students[:]
        self.students = [x[:degree] for x in student_data]

    def get_hash_tables(self):
        return (self.p_to_str, self.s_to_str)
