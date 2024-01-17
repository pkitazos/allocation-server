import copy
from matching_problems.solver.matching_details import ProjectCapacities, SupervisorCapacities
from src.request_data import ProjectData, RequestData, StudentData, SupervisorData


class ServerData:

    def __init__(self, data: RequestData):
        self.l_to_int = None
        self.p_to_int = None
        self.p_to_str = None
        self.s_to_str = None
        self.project_to_lecturer = None
        self.project_to_capacities = None
        self.lecturer_to_capacities = None
        self.lecturers = self.process_lecturers(data.supervisors)
        self.projects = self.process_projects(data.projects)
        self.students = self.process_students(data.students)

    def process_lecturers(self, lecturer_arr: list[SupervisorData]):
        to_int = {}
        l_to_c = {}
        lecturer_data = []
        for idx, lecturer in enumerate(lecturer_arr, 1):
            to_int[lecturer.id] = idx
            l_to_c[lecturer.id] = SupervisorCapacities(
                lower_bound=lecturer.lowerBound,
                target=lecturer.target,
                upper_bound=lecturer.upperBound
            )
            data = [lecturer.lowerBound, lecturer.target, lecturer.upperBound]
            lecturer_data.append(data)

        self.l_to_int = dict(to_int)
        self.lecturer_to_capacities = copy.deepcopy(l_to_c)
        return lecturer_data

    def process_projects(self, project_arr: list[ProjectData]):
        to_int = {}
        to_str = {}
        p_to_l = {}
        p_to_c = {}
        project_data = []
        for idx, project in enumerate(project_arr, 1):
            to_int[project.id] = idx
            to_str[idx] = project.id
            p_to_l[project.id] = project.supervisorId
            p_to_c[project.id] = ProjectCapacities(
                lower_bound=project.lowerBound,
                upper_bound=project.upperBound
            )
            data = [project.lowerBound, project.upperBound,
                    self.l_to_int[project.supervisorId]]
            project_data.append(data)

        self.p_to_int = dict(to_int)
        self.p_to_str = dict(to_str)
        self.project_to_lecturer = dict(p_to_l)
        self.project_to_capacities = copy.deepcopy(p_to_c)
        return project_data

    def process_students(self, student_arr: list[StudentData]):
        student_data = []
        to_str = {}
        for idx, student in enumerate(student_arr):
            data = [self.p_to_int[x] for x in student.preferences]
            student_data.append(data)
            to_str[idx] = student.id

        self.s_to_str = to_str
        return student_data

    def truncate(self, degree: int):
        student_data = self.students[:]
        self.students = [x[:degree] for x in student_data]

    def get_hash_tables(self):
        return (self.p_to_str,
                self.s_to_str,
                self.project_to_lecturer,
                self.project_to_capacities,
                self.lecturer_to_capacities)
