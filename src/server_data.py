from src.hash_tables import HashTables


class ServerData:

    def __init__(
        self,
        lecturer_data: list[list[int]],
        project_data: list[list[int]],
        student_data: list[list[int]],
        hash_tables: HashTables,
    ):
        self.lecturers = lecturer_data
        self.projects = project_data
        self.students = student_data
        self.hash_tables = hash_tables
    
    def __str__(self):
        lecturers = f"LECTURERS: {self.lecturers}"
        projects = f"PROJECTS: {self.projects}"
        students = f"STUDENTS: {self.students}"
        return f"\n{lecturers}\n\n{projects}\n\n{students}\n"
    
    def truncate(self, degree: int):
        student__data = self.students[:]
        self.students = [x[:degree] for x in student__data]

    def get_hash_tables(self):
        return self.hash_tables


    def display(self):
        print(self)

        
