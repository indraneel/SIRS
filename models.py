class Professor:
    def __init__(self, name):
        self.name = name
        self.all_sections = []

    def add_section(self, newSection):
        self.all_sections.append(newSection)

    def get_x_matrix(self):
        x_matrix = []
        for section in self.all_sections:
            x_matrix.append(section.x)

        return x_matrix

    def get_y_matrix(self, question):
        y_matrix = []
        for section in self.all_sections:
            if not section:
                continue

            if not len(section.y) == 2:
                continue

            y_matrix.append(section.y[question])

        return y_matrix

    def __repr__(self):
        return self.name + " has " + str(len(self.all_sections)) + " sections"


class Section:
    def __init__(self, courseID, professor, features, targets):
        self.courseID = courseID
        self.professor = professor
        self.x = [float(item) for item in features]
        self.y = [float(item) for item in targets]

    def __repr__(self):
        return self.courseID + " " + self.professor + " x=" + str(self.x) + " y="+str(self.y)


class Course:
    def __init__(self, courseID):
        self.courseID = courseID
        self.professors = []
        self.all_sections = []

    def add_section(self, newSection):
        self.all_sections.append(newSection)

    def get_x_matrix(self):
        x_matrix = []
        for section in self.all_sections:
            x_matrix.append(section.x)

        return x_matrix

    def get_y_matrix(self, question):
        y_matrix = []
        for section in self.all_sections:
            if not section:
                continue

            if not len(section.y) == 2:
                continue

            y_matrix.append(section.y[question])

        return y_matrix


    def __repr__(self):
        return self.courseID + " and this has " + len(self.sections) + " sections"
