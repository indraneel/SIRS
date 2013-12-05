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
def create_big_matrix(global_dict):
    temp_x = []
    temp_y = []
    for item in global_dict:
        for x_val in global_dict[item].get_x_matrix():
            temp_x.append(x_val)

        for y_val in global_dict[item].get_y_matrix(1):
            temp_y.append(y_val)

    return temp_x, temp_y

big_x, big_y = create_big_matrix(professorDict)



"""
    put the arrays into the numpy arrays
    then, do a linear regresion aka:
        weight vector = (Xtrans * X)^-1 * Xtrans * y
        normalize the weights
        looking at the weights can determine impact
"""

""" returns normalized weights given big_x and big_y """
def linear_regression(big_x, big_y):
    X = numpy.array(big_x)
    Y = numpy.array(big_y)
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
    #print "XtXinvXtY"
    #print "---------"
    #print XtXinvXtY

    #normalize
    XtXinvXtYt = XtXinvXtY.T
    normalized_weights = [(item/(math.sqrt(numpy.dot(XtXinvXtYt,XtXinvXtY))))for item in XtXinvXtY]
    return normalized_weights

count = 0
for item in linear_regression(big_x, big_y):
    print "weight of question number ",count+1,"=",item
    count+=1


"""
then, go through a professor's (any professor's)
entire section list and average all the x1s->x8s
plug in these averages into this: X * theta
AND THAT SHOULD EQUAL THE PREDICTION FOR

"""
