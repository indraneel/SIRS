import random
import math
import models as m
import os
import numpy
from scipy import linalg
import itertools

professorDict = {} # train
courseDict = {} # train

testProfessorDict= {}
testCourseDict = {} # test


"""parse and make Section and Professor objects"""
# def makeObject(dirpath, filename, courseDict, professorDict):
def makeObject(dirpath, filename):
    f = open(os.sep.join([dirpath, filename]), 'r')

    sections_added = []
    for line in f:
        fields = line.split("|")
        fields[len(fields)-1] = fields[len(fields)-1][:-1]  # getting rid of newline
        pName = fields[0]
        if not pName:
            continue

        if pName == "":
            continue

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
        courseID = filename + CID
        if courseID not in courseDict:
            courseDict[courseID] = m.Course(courseID)
        currCourse = courseDict[courseID]
        currCourse.add_section(newSection)
        #Check if professor in dictionary and add it
        if pName not in professorDict:
            professorDict[pName] = m.Professor(pName)
        currProfessor = professorDict[pName]
        currProfessor.add_section(newSection)
        sections_added.append(newSection)

num_folds = 10
for (dirpath, dirnames, filenames) in os.walk("./parsed-data/"):
    # TODO - divvy 9/10 into train, 1/10 into test
    #subset_training_size = len(filenames)/num_folds
    for filename in filenames:
        #for i in range(0, subset_training_size - 1):
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
""" question_type takes [0,1]: {
        0: 'y1 (effec. of instructor)',
        1: 'y2 (quality of course)'
    }"""
def create_big_matrix(global_dict, question_type):
    print "question #"+str(question_type+1)
    print "name "
    temp_x = []
    temp_y = []
    for item in global_dict:
        for x_val in global_dict[item].get_x_matrix():
            temp_x.append(x_val)
        for y_val in global_dict[item].get_y_matrix(question_type):
            temp_y.append(y_val)

    return temp_x, temp_y # and doing the same for y, and returning them

big_x, big_y = create_big_matrix(professorDict, 1)
#so we're looking at question 2*** question TWO, the quality of class one
# after iterating through the big matrix of all the sections
# big_x, big_y = create_big_matrix(courseDict)
# print professorDict
"""
now this is happening
    put the arrays into the numpy arrays
    then, do a linear regresion aka:
        weight vector = (Xtrans * X)^-1 * Xtrans * y
        normalize the weights
        looking at the weights can determine impact
"""

""" returns normalized weights given big_x and big_y """
def linear_regression(big_x, big_y):
    # this should look familiar
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
    #print XtXinvXtY <= this is our theta equation!
    #normalize => then i normalize, as per numpy/taylor's (my friend) formula
    XtXinvXtYt = XtXinvXtY.T
    normalized_weights = [(item/(math.sqrt(numpy.dot(XtXinvXtYt,XtXinvXtY))))for item in XtXinvXtY]
    return normalized_weights # and return

count = 0 # and then it's easy! just iterate through the normalized results. these are our weights. lets loo
for item in linear_regression(big_x, big_y):
    print "weight of question number ",count+1,"=",item
    count+=1


"""
then, go through a professor's (any professor's)
entire section list and average all the x1s->x8s
plug in these averages into this: X * theta
AND THAT SHOULD EQUAL THE PREDICTION FOR

BY THE WAY => I PUT SOME RESULTS IN THE NOTES ON THE POWERPOINT
IT IS VERY MUCH NOT FINISHED HOWEVER.
DO YOU WANT TO DO THAT NOW WHILE I DO THIS?
Are we ready to give results? EVERYTHING BUT THAT


currently writing the part where we
take in an avg professor features
and then do the plugging stuff"""
def get_avg_features_professor(name, professorDict):
    if not name in professorDict:
        name = random.choice(professorDict.keys())
    if not name:
        name = random.choice(professorDict.keys())

    print "name = " + name # i'm stpuid as ffuck
    features = professorDict[name].get_x_matrix()
    avg_features = [0,0,0,0,0,0,0,0]
    for featurelist in features:
        for i in range(len(featurelist)):
            avg_features[i] += featurelist[i]

    # print "pre-dividing by sum"
    # print avg_features
    avg_features = [item/len(features) for item in avg_features]
    # print "post dividing by sum"
    print "avg features = ",avg_features
    return avg_features


def predict_score(input_features, normalized_weights):
    # average of a rand prof * weights =
    orig_val = numpy.dot(input_features,normalized_weights)
    max_avg = [5 for i in range(0,8)]
    scaling_factor = numpy.dot(max_avg,normalized_weights)
    print (orig_val/scaling_factor)*5


input_features = get_avg_features_professor("", professorDict)
normalized_weights = linear_regression(big_x, big_y)
predict_score(input_features, normalized_weights)
