import math
import models as m
import os
import numpy
from scipy import linalg
import itertools

professorDict = {}
courseDict = {}

"""parse and make Section and Professor objects"""
def makeObject(dirpath, filename):
    f = open(os.sep.join([dirpath, filename]), 'r')

    sections_added = []
    for line in f:
        fields = line.split("|")
        fields[len(fields)-1] = fields[len(fields)-1][:-1]  # getting rid of newline
        pName = fields[0]
        CID = fields[1]

        if CID == "NONE":
            continue

        if all( float(field)==0.0 for field in fields[2:]):
            continue

        # check if rating lengths too small
        if len(fields[2:]) < 8:
            continue

        if len(fields[10:]) < 2:
            continue

        # if the section is already added ,skip for now
        if any(CID in s.courseID for s in sections_added):
            continue

        newSection = m.Section(CID, pName, fields[2:10], fields[10:12])
        #Check if professor in dictionary and add it
        if pName not in professorDict:
            professorDict[pName] = m.Professor(pName)
        currProfessor = professorDict[pName]
        currProfessor.add_section(newSection)
        sections_added.append(newSection)

for (dirpath, dirnames, filenames) in os.walk("./parsed-data/"):
    for filename in filenames:
        if filename[-4:] == ".txt":
            makeObject(dirpath, filename)

"""
Show which questions have impact on quality of course
via seeing their weights after linear regression

"""
"""
    go through all professors
    for all of their sections:
        add the X's to a global matrix
        add the Y's to a global vector
"""

big_x = []
big_y = []
for item in professorDict:
    for x_val in professorDict[item].get_x_matrix():
        big_x.append(x_val)

    for y_val in professorDict[item].get_y_matrix(1):
        big_y.append(y_val)

# print "big x"
# print "~~~~~"
# print big_x
# print "big y"
# print "~~~~~"
# print big_y


"""
    put the arrays into the numpy arrays
"""

X = numpy.array(big_x)
Y = numpy.array(big_y)
#import pdb
#pdb.set_trace();
print "X\n~~"
print X
print "Y\n~~"
print Y

"""
    then, do a linear regresion aka:
        weight vector = (Xtrans * X)^-1 * Xtrans * y
        normalize the weights
        looking at the weights can determine impact
"""

Xt = X.T
# print "Xt"
# print Xt
XtX = numpy.dot(Xt,X)
# print "XtX"
# print XtX
XtXinv = numpy.linalg.inv(XtX)
# print "XtXinv"
# print XtXinv
XtXinvXt = numpy.dot(XtXinv, Xt)
# print "XtXinvXt"
# print XtXinvXt
XtXinvXtY = numpy.dot(XtXinvXt, Y) #unweighted theta vector
print "XtXinvXtY"
print "---------"
print XtXinvXtY

#normalize
XtXinvXtYt = XtXinvXtY.T
normalized_weights = [(item/(math.sqrt(numpy.dot(XtXinvXtYt,XtXinvXtY))))for item in XtXinvXtY]
# print "normalized_weights"
# print normalized_weights
count = 0
for item in normalized_weights:
    print count,item
    count+=1



"""
    then, go through a professor's (any professor's)
    entire section list and average all the x1s->x8s
    plug in these averages into this: X * theta
    AND THAT SHOULD EQUAL THE PREDICTION FOR

"""

# brillX = professorDict['BRILL GARY'].get_x_matrix()
# brillY = professorDict['BRILL GARY'].get_y_matrix()

#print bigXMatrix
#print bigYMatrix
#print (X.T).dot(X)
#print (linalg.inv(X.T.dot(X)).dot(X.T)).dot(Y)
#print "---------------------"
#print "X"
#print "~~"
#print X
#print "---------------------"
#print "X.T"
#print "~~"
#print X.T
#print "---------------------"
#print "X.T.dot(X)"
#print "~~"
#print X.T.dot(X)
#print "---------------------"
#print "linalg.inv(X.T.dot(X))"
#print "~~"
#print linalg.inv(X.T.dot(X))
#print "---------------------"
#print "linalg.inv(X.T.dot(X)).dot(X.T)"
#print "~~"
#print (linalg.inv(X.T.dot(X))).dot(X.T)
#print "---------------------"
#print "Y"
#print "~~"
#print Y
#print "---------------------"
#print "(linalg.inv(X.T.dot(X)).dot(X.T)).dot(Y)"
#print "~~"
#print (linalg.inv(X.T.dot(X)).dot(X.T)).dot(Y)
