import sys,requests as rq,series
from bs4 import BeautifulSoup

def main():
    """Main entry point for the script."""
    links = getLinks()
    # for link in links:
    #     print(link)
    if(True):
        html = getHTML(links[0])
        series = getSeries(html)
        parseSeries(series)



#The get request
def getHTML(url):
    if url=="default":
        url = "https://www.reddit.com/r/animethemes/wiki/year_index"

    headers = {
        "User-Agent": "Testing 1.0",
    }
    r = rq.get(url, headers={"User-Agent": "Testing 1.0"})
    return r.text

def getLinks():
    html = getHTML("default")
    soup = BeautifulSoup(html, 'lxml')
    years = soup.find("div", {"class": "md wiki"})
    yearLinks = []
    for h in years.find_all('h3'):
        yearLinks.append(h.contents[0]['href'])
    return yearLinks

#Returns array of HTML title and table
def getSeries(html):
    soup = BeautifulSoup(html, 'lxml')
    year = soup.find("h1", {"class": "wikititle"}).contents[0]
    content = soup.find("div", {"class": "md wiki"})
    seriesList = [] #Stores list of series objects
    for h in content.find_all("h3"):
        series = [] #temp array to store relevant HTML
        series.append(h) #Name
        if h.next_sibling.next_sibling.name == "p":
            series.append(h.next_sibling.next_sibling) #P tag
            series.append(h.next_sibling.next_sibling.next_sibling.next_sibling) #Table tag
        else:
            series.append(h.next_sibling.next_sibling) #Table tag
        series.append(year)
        seriesList.append(series)
    return seriesList

#Parses the HTML array and returns array of series, links, episodes, and notes
def parseSeries(htmlArr):
    for s in htmlArr:
        if len(s) == 3:
            title = s[0].contents[0].contents[0]
            year = s[2].contents[0]


        else:
            title = s[0].contents[0].contents[0]
            altTitle = s[1].contents[0].contents[0]
            year = s[3].contents[0]

#figure out table parsing now



#Creates organized json database
def populateDb():
    pass

if __name__ == '__main__':
    sys.exit(main())
#get page html
#look for series link title
#grab table under it
#go row by row where first column is name and second is links
#if row has no "title" then stick to the previous. Column is link referring to previous
#do that for each title link