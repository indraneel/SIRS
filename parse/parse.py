""""Parses the SIRS ratings tables."""
from BeautifulSoup import BeautifulSoup
import re

index_html = open('index.html', 'r')
targetFile = open('ratingsCS.txt', 'w')
soup = BeautifulSoup(index_html)

numberedDivs = soup.findAll("div", {"id": re.compile("d*")})
for div in numberedDivs:
    result = ""
    table = div.find("table")
    result += table.find("tr").find("strong").text + "|"  # add professor name
    result += table.find("tr").find("q").text + "|"  # add class taught
    trs = table.findAll("tr")
    for tr in trs:
        td = tr.findAll("td", {"class": "mono stats"})
        if td:
            result += td[0].text + "|"  # add ratings
    result = result[:-1]
    result += "\n"
    targetFile.write(result)
