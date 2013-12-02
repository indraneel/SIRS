import mechanize
import re
import sys
import getpass

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
dept = "198"
course = ""

# urls
baseURL = "https://sirs.ctaar.rutgers.edu/index.php"
baseQueryURL = "?survey%5Bsemester%5D="+semester+"&survey%5Byear%5D="+year+"&survey%5Bschool%5D="+schoolCode+"&survey%5Bdept%5D="+dept+"&survey%5Bcourse%5D="+course+"&mode=course',"

br = mechanize.Browser()
br.open(baseURL+baseQueryURL)
assert br.viewing_html()

# select and submit form
br.select_form(nr=0)
br.form['username'] = username
br.form['password'] = password
br.submit()

# form response => should log us in
login_response = br.response()
print "response url = "
print login_response.geturl()
print login_response.info()  # headers
print login_response.read()
