class Series:
    def __init__(self, title,altTitle,year,songs): #(string, string, int, array)
        self.title = title
        self.altTitle = altTitle
        self.year = year
        self.songs = songs

class Song:
    def __init__(self, title,linkTitles,links,episodes,notes): #(string, array, array, string, string)
        self.title = title
        self.linkT = linkTitles
        self.links = links
        self.eps = episodes
        self.notes = notes