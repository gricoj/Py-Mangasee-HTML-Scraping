# Mangasee-HTML-Scraping
Series Name:
```html
<h1 class="SeriesName">One Piece</h1>
```
Chapter Entries
```html
<div class="list chapter-list">
  <a class="list-group-item" chapter="964" href="/read-online/One-Piece-chapter-964-page-1.html" title="Read One Piece Chapter 964 For Free Online">
    <span class="chapterLabel">Chapter 964</span>
    <i class="hidden-xs">
    </i><time class="SeriesTime pull-right" datetime="2019-11-29T05:13:28+00:00" datestring="20191129">11/29/2019</time>
  </a>
  .
  .
  .
  .
  
  <a class="list-group-item" chapter="1" href="/read-online/One-Piece-chapter-1-page-1.html" title="Read One Piece Chapter 1 For Free Online">
    <span class="chapterLabel">Chapter 1</span>
    <i class="hidden-xs"></i>
    <time class="SeriesTime pull-right" datetime="2019-03-21T01:08:43+00:00" datestring="20190321">03/21/2019</time>
  </a>
</div>
```
Single Chapter Entry:
```html
<a class="list-group-item" chapter="964" href="/read-online/One-Piece-chapter-964-page-1.html" title="Read One Piece Chapter 964 For Free Online">
  <span class="chapterLabel">Chapter 964</span>
  <i class="hidden-xs">
  </i><time class="SeriesTime pull-right" datetime="2019-11-29T05:13:28+00:00" datestring="20191129">11/29/2019</time>
</a>
```
### Manga Class
```python
class Chapter_OBJ:
    def __init__(self, series, chapter_number, date_published, url):
        self.series = series
        self.chapter_number = chapter_number
        self.date_published = date_published
        self.url = url
```
### Functions
```python
def getLatestChapter(Manga_URL):
    session = HTMLSession()
    r = session.get(Manga_URL)
    Series_Name = (r.html.find('.SeriesName',first=True)).text

    Latest_Chapter = r.html.find('.list-group-item',first=True)

    Chapter_Number = float(((Latest_Chapter.find('.chapterLabel',first=True)).text).replace("Chapter ",""))
    Chapter_PD = (Latest_Chapter.find('time',first=True)).text
    Chapter_URL = ((Latest_Chapter.absolute_links).pop()).replace("-page-1","")
    return Chapter_OBJ(Series_Name,Chapter_Number,Chapter_PD,Chapter_URL)
```
```python
def getTimeSinceLastChapter(Manga_URL):
    session = HTMLSession()
    r = session.get(Manga_URL)

    Time = ((r.html.find('.list-group-item',first=True).find('time',first=True).html).split('"')[3]).split("+")[0]

    date_format = "%Y-%m-%dT%H:%M:%S"
    newTime = (datetime.strptime(Time,date_format)).strftime(date_format)
    currentTime = (datetime.utcnow()).strftime(date_format)
    tdelta = datetime.strptime(currentTime, date_format) - datetime.strptime(newTime, date_format)

    return tdelta
```
```python
def getAllChapters(Manga_URL):
    session = HTMLSession()
    r = session.get(Manga_URL)

    Chapters = r.html.find('.list-group-item')
    Series_Name = r.html.find('.SeriesName',first=True)

    Chapter_Array = []
    for chapter in Chapters:
        Chapter_Number = float(((chapter.find('.chapterLabel',first=True)).text).replace("Chapter ",""))
        Chapter_URL = ((chapter.absolute_links).pop()).replace("-page-1","")
        Chapter_PD = (chapter.find('time',first=True)).text
        Chapter_Array.append(Chapter_OBJ(Series_Name,Chapter_Number,Chapter_PD,Chapter_URL))
    return Chapter_Array
```
