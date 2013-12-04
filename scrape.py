import mechanize
import re
import sys
import getpass

def build_url(semester, year, schoolCode, dept, course=""):
    baseURL = "https://sirs.ctaar.rutgers.edu/index.php"
    baseQueryURL = "?survey%5Bsemester%5D="+semester+"&survey%5Byear%5D="+year+"&survey%5Bschool%5D="+schoolCode+"&survey%5Bdept%5D="+dept+"&survey%5Bcourse%5D="+course+"&mode=course"
    return baseURL+baseQueryURL

depts = ["220", "198","195"]


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

for dept in depts:
    url = build_url(semester, year, schoolCode, dept)
    br.open(url)
    print br.response().read()

