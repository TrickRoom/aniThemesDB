class Series:
    def __init__(self, title,altTitle,year,songs): #(string, string, int, array)
        self.title = title
        self.altTitle = altTitle
        self.year = year
        self.songs = songs

    def content(self):
        temp = []
        temp.append(self.title)
        temp.append(self.altTitle)
        temp.append(self.year)
        temp.append(self.songs)
        return temp

class Song:
    def __init__(self, title,linkTitles,links,episodes,notes): #(string, array, array, string, string)
        self.title = title
        self.linkT = linkTitles
        self.links = links
        self.eps = episodes
        self.notes = notes

    def content(self):
        temp = []
        temp.append(self.title)
        temp.append(self.linkT)
        temp.append(self.links)
        temp.append(self.eps)
        temp.append(self.notes)
        return temp