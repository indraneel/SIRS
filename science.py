import re

all_sections = []
with open('parse/ratingsCS.txt', 'rb') as datafile:
    for line in datafile:
        print "------------------------------------"
        fields = line.split("|")
        fields[len(fields)-1] = fields[len(fields)-1][:-1]  # getting rid of newline
        print fields[2:]
        all_sections.append(fields)

