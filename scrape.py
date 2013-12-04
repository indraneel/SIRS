import ast #converts string literal to dictionary
import mechanize
import re
import requests
import sys
import getpass

raw_files_dir = "./raw-files/"

def build_url(name="index", semester="", year="", schoolCode="", dept="", course=""):
    baseURL = "https://sirs.ctaar.rutgers.edu/"+name+".php"
    baseQueryURL = "?survey%5Bsemester%5D="+semester+"&survey%5Byear%5D="+year+"&survey%5Bschool%5D="+schoolCode+"&survey%5Bdept%5D="+dept+"&survey%5Bcourse%5D="+course+"&mode=course"
    return baseURL+baseQueryURL


if len(sys.argv) < 2:
    print "Usage: python scrape.py <netID>"
    sys.exit(0)

# save auth information
username = sys.argv[1]
password = getpass.getpass()

# TODO - lists of possible values for each form input
semester = "Spring"
year = "2013"
schoolCode = "01"
course = ""

# urls
baseURL = "https://sirs.ctaar.rutgers.edu/index.php"
# create browser object

br = mechanize.Browser()
br.open(baseURL)
assert br.viewing_html()

# select and submit form
# print br.response().read()
br.select_form(nr=0)
br.form['username'] = username
br.form['password'] = password
br.submit()

semesters = ["Spring", "Fall"]
years = ["2013", "2012", "2011", "2010", "2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001"]
assert br.viewing_html()
for year in years:
    print year
    for sem in semesters:
	# print sem
	# get school list for a given year-semester
	br.open(build_url("courseFilter", sem, year))
	assert br.viewing_html()
	schools = ast.literal_eval(br.response().read())
	if not schools:
	    continue

	for school in schools['schools']:
	    # print school[0]
	    # get the dept
	    br.open(build_url("courseFilter", sem, year, school[0]))
	    assert br.viewing_html()
	    depts = ast.literal_eval(br.response().read())
	    if not depts:
		continue
	    depts = depts['depts']
	    # print depts
	    for dept in depts:
		size = len(semesters)*len(years)*len(schools['schools'])*len(depts)
		# print "SIZE = " + str(size)
		file_name = ""+year+"-"+sem+"-"+school[0]+"-"+dept+".html"
		target_file = open(raw_files_dir+file_name, "w")
		full_url = build_url("index", sem, year, school[0], dept)
		try:
		    br.open(build_url("index", sem, year, school[0], dept))
		    assert br.viewing_html()
		except:
		    print "it failed = "
		    print full_url 

		target_file.write(br.response().read())
		print "just finished = " + full_url


"""
for dept in depts:
    url = build_url(semester, year, schoolCode, dept)
    br.open(url)
    print br.response().read()
"""
