from requests_html import HTML, HTMLSession
from datetime import datetime 

class Chapter_OBJ:
    def __init__(self, series, chapter_number, date_published, url):
        self.series = series
        self.chapter_number = chapter_number
        self.date_published = date_published
        self.url = url

def getAllChapters(Manga_URL):
    session = HTMLSession()
    r = session.get(Manga_URL)

    Chapters = r.html.find('.list-group-item')
    Series_Name = r.html.find('.SeriesName',first=True)

    Chapter_List = []
    for chapter in Chapters:
        Chapter_Number = float(((chapter.find('.chapterLabel',first=True)).text).split(" ")[1])
        Chapter_URL = ((chapter.absolute_links).pop()).replace("-page-1","")
        Chapter_PD = (chapter.find('time',first=True)).text
        Chapter_List.append(Chapter_OBJ(Series_Name,Chapter_Number,Chapter_PD,Chapter_URL))
    return Chapter_List

def getTimeSinceLastChapter(Manga_URL):
    session = HTMLSession()
    r = session.get(Manga_URL)

    Time = ((r.html.find('.list-group-item',first=True).find('time',first=True).html).split('"')[3]).split("+")[0]

    date_format = "%Y-%m-%dT%H:%M:%S"
    newTime = (datetime.strptime(Time,date_format)).strftime(date_format)
    currentTime = (datetime.utcnow()).strftime(date_format)
    tdelta = datetime.strptime(currentTime, date_format) - datetime.strptime(newTime, date_format)

    return tdelta

def getLatestChapter(Manga_URL):
    session = HTMLSession()
    r = session.get(Manga_URL)
    Series_Name = (r.html.find('.SeriesName',first=True)).text

    Latest_Chapter = r.html.find('.list-group-item',first=True)

    Chapter_Number = float(((Latest_Chapter.find('.chapterLabel',first=True)).text).split(" ")[1])
    Chapter_PD = (Latest_Chapter.find('time',first=True)).text
    Chapter_URL = ((Latest_Chapter.absolute_links).pop()).replace("-page-1","")
    return Chapter_OBJ(Series_Name,Chapter_Number,Chapter_PD,Chapter_URL)
