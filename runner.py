import random
import sys
import math
import models as m
import os
import numpy
import scipy
from scipy.stats import pearsonr
from collections import OrderedDict
import itertools

# GLOBALS
professorDict = {}  # train
courseDict = {}  # train

testProfessorDict= {}
testCourseDict = {}  # test

big_x = []
big_y = []


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

        if all(float(field) == 0.0 for field in fields[2:]):
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
""" question_type takes [0,1]: {
        0: 'y1 (effec. of instructor)',
        1: 'y2 (quality of course)'
    }"""
def create_big_matrix(global_dict, question_type):
    temp_x = []
    temp_y = []
    for item in global_dict:
        for x_val in global_dict[item].get_x_matrix():
            temp_x.append(x_val)
        for y_val in global_dict[item].get_y_matrix(question_type):
            temp_y.append(y_val)

    return temp_x, temp_y  # and doing the same for y, and returning them

#so we're looking at question 2*** question TWO, the quality of class one
# after iterating through the big matrix of all the sections
# big_x, big_y = create_big_matrix(courseDict)
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
    XtX = numpy.dot(Xt,X)
    XtXinv = numpy.linalg.inv(XtX)
    XtXinvXt = numpy.dot(XtXinv, Xt)
    XtXinvXtY = numpy.dot(XtXinvXt, Y)  # unweighted theta vector
    #print XtXinvXtY <= this is our theta equation!
    #normalize => then i normalize, as per numpy/taylor's (my friend) formula
    XtXinvXtYt = XtXinvXtY.T
    normalized_weights = [(item / (math.sqrt(numpy.dot(XtXinvXtYt,XtXinvXtY)))) for item in XtXinvXtY]
    return normalized_weights  # and return

# and then it's easy! just iterate through the normalized results. these are our weights. lets loo


"""
then, go through a professor's (any professor's)
entire section list and average all the x1s->x8s
plug in these averages into this: X * theta
AND THAT SHOULD EQUAL THE PREDICTION FOR

currently writing the part where we
take in an avg professor features
and then do the plugging stuff"""
def get_avg_features_professor(name):
    if not name in professorDict:
        name = random.choice(professorDict.keys())
    if not name:
        name = random.choice(professorDict.keys())

    features = professorDict[name].get_x_matrix()
    avg_features = [0, 0, 0, 0, 0, 0, 0, 0]
    for featurelist in features:
        for i in range(len(featurelist)):
            avg_features[i] += featurelist[i]

    avg_features = [item / len(features) for item in avg_features]
    return avg_features


def predict_score(input_features, normalized_weights):
    # average of a rand prof * weights =
    orig_val = numpy.dot(input_features, normalized_weights)
    max_avg = [5 for i in range(0, 8)]
    scaling_factor = numpy.dot(max_avg, normalized_weights)
    return (orig_val / scaling_factor) * 5

def correlation():
    y1 = []
    y2 = []
    for prof in professorDict:
        for section in professorDict[prof].all_sections:
            y1.append(section.y[0])
            y2.append(section.y[1])
    return pearsonr(y1, y2)

def root_mean_squared_error(normalized_weights):
    sum_squared_error = 0
    y1_sum = 0
    y2_sum = 0
    prof_class_average = 0
    for prof in professorDict:
        prof_features = get_avg_features_professor(prof)
        predicted_score = predict_score(prof_features, normalized_weights)
        sections = professorDict[prof].all_sections
        for section in sections:
            y1_sum += section.y[0]
            y2_sum += section.y[1]
        prof_class_average = ((y1_sum / len(sections)) + (y2_sum / len(sections))) / 2
        sum_squared_error += (predicted_score - prof_class_average) ** 2
        y1_sum = 0
        y2_sum = 0
    result = math.sqrt(sum_squared_error / len(professorDict))
    return result


def ten_fold_validation():
    orderedProfessorDict = OrderedDict(sorted(professorDict.items(), key=lambda t: t[0]))
    oneFoldLen = len(professorDict) / 10
    training = dict(itertools.islice(orderedProfessorDict.iteritems(), oneFoldLen, len(orderedProfessorDict) - 1))
    validation = dict(itertools.islice(orderedProfessorDict.iteritems(), 0, oneFoldLen))
    x_dim, y_dim = create_big_matrix(training, 0)
    training_weights = linear_regression(x_dim, y_dim)
    error_sum = 0
    for prof in validation:
        avg_features = get_avg_features_professor(prof)
        training_score = predict_score(avg_features, normalized_weights)
        validation_score = predict_score(avg_features, training_weights)
        error_sum += math.sqrt((training_score - validation_score) ** 2)
        print "t_score = ", training_score, "v_score = ", validation_score
    print "error = ", error_sum / len(validation)


def main():
    num_folds = 10
    for (dirpath, dirnames, filenames) in os.walk("./parsed-data/"):
        #subset_training_size = len(filenames)/num_folds
        for filename in filenames:
            #for i in range(0, subset_training_size - 1):
            if filename[-4:] == ".txt":
                makeObject(dirpath, filename)

    big_x, big_y = create_big_matrix(professorDict, 0)

    count = 0
    for item in linear_regression(big_x, big_y):
        count += 1
    if len(sys.argv) == 2:
        input_features = get_avg_features_professor(sys.argv[1])
    else:
        input_features = get_avg_features_professor("")
    normalized_weights = linear_regression(big_x, big_y)

    print predict_score(input_features, normalized_weights)
    print root_mean_squared_error(normalized_weights)
    #print "-----------------------------------------"
    #ten_fold_validation()
    #print "-----------------------------------------"

    print correlation()


if __name__ == "__main__":
    main()
