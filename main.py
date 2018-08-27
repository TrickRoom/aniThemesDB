# -*- coding: utf-8 -*-
import sys,requests as rq, series as sr, json
from bs4 import BeautifulSoup

def main():
    parsed = []
    links = getLinks()
    for link in links:
        print(link)
        html = getHTML(link)
        series = getSeries(html)
        parsed.append(parseSeries(series))
    populateDb(parsed)

#The get request
def getHTML(url):
    if url=="default":
        url = "https://www.reddit.com/r/animethemes/wiki/year_index"

    headers = {
        "User-Agent": "AniThemes 1.2",
    }
    r = rq.get(url, headers=headers)
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
        if h.next_sibling.next_sibling.name == "p" and h.next_sibling.next_sibling.find("strong")!=None:
            series.append(h.next_sibling.next_sibling) #P tag
            series.append(h.next_sibling.next_sibling.next_sibling.next_sibling) #Table tag
        else:
            series.append(h.next_sibling.next_sibling) #Table tag
        series.append(year)
        seriesList.append(series)
    return seriesList

#Parses the HTML array and returns array of series, links, episodes, and notes
def parseSeries(htmlArr):
    seriesList = []
    for s in htmlArr:
        if len(s) == 3:
            title = s[0].contents[0].contents[0]
            year = s[2].contents[0]
            songs = parseTable(s[1])
            seriesList.append(sr.Series(title,"",year,songs))
        else:
            title = s[0].contents[0].contents[0]
            altTitle = s[1].contents[0].contents[0]
            year = s[3].contents[0]
            songs = parseTable(s[2])
            seriesList.append(sr.Series(title,altTitle,year,songs))
    return seriesList

def parseTable(table):
    title = ""
    type = ""
    episodes = ""
    notes = ""
    links = []
    linkTitles = []
    songs = []
    for row in table.find_all('tr'):
        columns = row.find_all('td')
        if len(columns)>1: #avoid the empty row (the header row)
            if len(columns[0].contents)>=1: #if the theme title exists
                if title!="":
                    songs.append(sr.Song(title,type,linkTitles,links,episodes,notes))
                    title = ""
                    type = ""
                    episodes = ""
                    notes = ""
                    links = []
                    linkTitles = []
                tempTitle = columns[0].contents[0].split("\"")
                if len(tempTitle)==1:
                    tempTitle = columns[0].contents[0].split("”")
                print(columns[0].contents[0])
                type = tempTitle[0]
                if len(tempTitle)==1:
                    title = "MV"
                else:
                    title = tempTitle[1]
            themeLink = columns[1].find('a', href=True)
            if themeLink!=None: #error check because of literally one instance in the data
                links.append(columns[1].find('a', href=True)['href'])
                linkTitles.append(columns[1].find('a', href=True).contents[0])
                if(len(columns[2].contents)>=1):
                    episodes = columns[2].contents[0]

                try:
                    if (len(columns[3].contents) >= 1):
                        notes = str(columns[3].contents[0])
                except IndexError:
                    #print("Hit that one improperly formatted box in Mob Psycho 100, year 2016")
                    print("Hit an improperly formatted box.")

    songs.append(sr.Song(title, type, linkTitles, links, episodes, notes))
    return songs

#Creates organized json database
def populateDb(parsedList):
    db = json.dumps(parsedList, default=jsonDefault, indent=4, separators=(',', ': '))
    outfile = open('data.json', 'w')
    outfile.write(db)
    outfile.close

def jsonDefault(object):
    return object.__dict__

if __name__ == '__main__':
    sys.exit(main())
