from flask import Flask, request, jsonify, abort, make_response

import os
import pystache
import models as m

app = Flask(__name__, static_folder='public', static_url_path='')
# app = Flask(__name__)

professorDict = {} 
courseDict = {} 

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

 
@app.route('/')
def index():
    build_dir()
    return app.send_static_file('index.html')

@app.route('/all')
def print_all():
    print professorDict


@app.route('/search')
def search():
    if request.args.get('professor'):
	professor_query = request.args.get('professor')
	# localhost/search?professor=[input query]
    else:
	print 'missing parameters'
	return

    print "QUERY = " + professor_query
    if professor_query in professorDict:
	print professorDict[professor_query]

def build_dir():
    for (dirpath, dirnames, filenames) in os.walk("./parsed-data/"):
        for filename in filenames:
            if filename[-4:] == ".txt":
                makeObject(dirpath, filename)
    


if __name__ == '__main__':
    app.run()
