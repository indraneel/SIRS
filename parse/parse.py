""""Parses the SIRS ratings tables."""
from BeautifulSoup import BeautifulSoup
import re
import os


def parse(dirpath, filename):
    print "working on = " + os.sep.join([dirpath, filename])
    name = filename[:-5]
    name += ".txt"
    index_html = open(os.sep.join([dirpath,filename]), 'r')
    targetFile = open(os.sep.join(["../parsed-data/", name]), 'w')
    soup = BeautifulSoup(index_html)
    classRegex = "01\:[0-9]{3}\:[0-9]{3}\:[0-9]{2}"

    numberedDivs = soup.findAll("div", {"id": re.compile("d*")})
    for div in numberedDivs:
        result = ""
        table = div.find("table")
        result += table.find("tr").find("strong").text + "|"  # add professor name

        tableText= table.find("tr").text

        if re.compile(classRegex).search(tableText):
            classNum = re.compile(classRegex).search(tableText).group(0)
            result += str(classNum) + "|"
        else:
            result += "NONE|"
        """
        for x in table.find("tr").findAll("br"):
            print x.text

        if table.find("tr").find("q"):
            result += table.find("tr").find("q").text + "|"  # add class taught
        else:
            result += "anon" + "|"
        """

        trs = table.findAll("tr")
        for tr in trs:
            td = tr.findAll("td", {"class": "mono stats"})
            if td:
                result += td[0].text + "|"  # add ratings
        result = result[:-1]
        result += "\n"
        targetFile.write(result)

count = 0
list_of_files = {}
for (dirpath, dirnames, filenames) in os.walk("../raw-data/"):
    for filename in filenames:
        if filename[-5:] == ".html":
            parse(dirpath, filename)
