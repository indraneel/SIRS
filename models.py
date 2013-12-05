class Professor:
    def __init__(self, name):
        self.name = name
        self.all_sections = []

    def add_section(self):
        pass

class Section:
    def __init__(self, courseID, ratings):
        self.courseID = courseID
        self.ratings = ratings

class Course:
