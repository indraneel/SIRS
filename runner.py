import models as m
import os

professorDict = {}
courseDict = {}

"""parse and make Section and Professor objects"""
def makeObject(dirpath, filename):
    f = open(os.sep.join([dirpath, filename]), 'r')
    for line in f:
        fields = line.split("|")
        fields[len(fields)-1] = fields[len(fields)-1][:-1]  # getting rid of newline
        pName = fields[0]
        CID = fields[1]
        newSection = m.Section(CID, pName, fields[2:12])
        #Check if professor in dictionary and add it
        if pName not in professorDict:
            professorDict[pName] = m.Professor(pName)
        currProfessor = professorDict[pName]
        currProfessor.add_section(newSection)

fileCount = 0
for (dirpath, dirnames, filenames) in os.walk("./parsed-data/"):
    for filename in filenames:
        if filename[-4:] == ".txt":
            makeObject(dirpath, filename)
print professorDict['BRILL GARY'].get_matrix()
print len(professorDict['BRILL GARY'].get_matrix())
