from gkeepserver.assignments import AssignmentDirectory


class Report:
    def __init__(self, faculty_username, assignment_dir: AssignmentDirectory,
                 student, body):
        self.faculty_username = faculty_username
        self.