import models
import os

professorDict = {}
courseDict = {}

def makeObject(dirpath, filename):
    f = open(os.sep.join([dirpath, filename]), 'r')
    for line in f:
        fields = line.split("|")
        fields[len(fields)-1] = fields[len(fields)-1][:-1]  # getting rid of newline
        pName = fields[0]
        if pName not in professorDict:
            professorDict[pName] = models.Professor(pName)

fileCount = 0
for (dirpath, dirnames, filenames) in os.walk("./parsed-data/"):
    for filename in filenames:
        fileCount += 1
        if fileCount > 10:
            break
        if filename[-4:] == ".txt":
            makeObject(dirpath, filename)
print professorDict
