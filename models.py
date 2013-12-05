class Professor:
    def __init__(self, name):
        self.name = name
        self.all_sections = []

    def add_section(self, newSection):
        self.all_sections.append(newSection)

    def get_matrix(self):
        matrix = []
        for section in self.all_sections:
            matrix.append(section.ratings)
        return matrix

    def __repr__(self):
        return self.name


class Section:
    def __init__(self, courseID, professor, ratings):
        self.courseID = courseID
        self.professor = professor
        self.ratings = ratings

    def __repr__(self):
        return self.courseID + " " + self.professor + " " + str(self.ratings)


class Course:
    def __init__(self, courseID):
        self.courseID = courseID
        self.professors = []
        self.sections = []

    def __repr__(self):
        return self.courseID + " and this has " + len(self.sections) + " sections"
