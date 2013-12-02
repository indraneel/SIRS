import re
import mechanize

semester = "Spring"
year = "2013"
schoolCode = "01"
dept = "198"
course = ""
baseURL = "https://sirs.ctaar.rutgers.edu/index.php"
baseQueryURL = "?survey%5Bsemester%5D="+semester+"&survey%5Byear%5D="+year+"&survey%5Bschool%5D="+schoolCode+"&survey%5Bdept%5D="+dept+"&survey%5Bcourse%5D="+course+"&mode=course',"

br = mechanize.Browser()
response1 = br.open(baseURL+baseQueryURL)
assert br.viewing_html()
print br.title()
print response1.geturl()
print response1.info()  # headers
print response1.read()  # body

