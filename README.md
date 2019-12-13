# Mangasee HTML Scraping
We will be scraping [Mangasee](https://mangaseeonline.us) as it is a one of the better manga sources. The information we will be scraping includes: Series Name, Chapter Numbers, Publish Dates, and URL to the chapter. The purpose of this module is to eventually use it to get notified when a new chapter for a series is published.

## Table of Contents
[HTML](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#html)

[Installing Required Packages](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#installing-required-packages)

[Manga Class](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#manga-class)

[Functions](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#functions)

## HTML
These are snippets of the HTML for a [manga series'](https://mangaseeonline.us/manga/One-Piece) main page.
#### Series Name:
```html
<h1 class="SeriesName">One Piece</h1>
```
#### Single Chapter Entry:
```html
<a class="list-group-item" chapter="964" href="/read-online/One-Piece-chapter-964-page-1.html" title="Read One Piece Chapter 964 For Free Online">
  <span class="chapterLabel">Chapter 964</span>
  <i class="hidden-xs">
  </i><time class="SeriesTime pull-right" datetime="2019-11-29T05:13:28+00:00" datestring="20191129">11/29/2019</time>
</a>
```
#### Chapter Entries:
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

## Installing Required Packages
```python
pip install requests-html
pip install datetime
```
We use the [*request-html*](https://requests-html.kennethreitz.org/) package so that we can easily parse HTML. We use the [*datetime*](https://docs.python.org/3/library/datetime.html) to get the time since a new chapter has been released.

## Manga Class
```python
class Chapter_OBJ:
    def __init__(self, series, chapter_number, date_published, url):
        self.series = series
        self.chapter_number = chapter_number
        self.date_published = date_published
        self.url = url
```
We create a class so that we can store manga chapter's information into a single object. 

We specify 4 attributes: 
- series: Will store the manga series' name (string)
- chapter_number: Will store the chapter number (float)
- date_published: Will store the date the chapter was published on Mangasee (float)
- url: Will store the direct link to the particular chapter (string)

## Functions
#### getLatestChapter
This function is used to get the latest chapter in a manga series. Thankfully Mangasee formats their webpage such that a manga's chapters are listed in descending order. This will allows us to simply look for the the first instance of the the [*list-group-item*](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#single-chapter-entry) attribute. 
- We get the chapter number by finding the *chapterLabel* attribute, replacing the *"Chapter "* substring with an empty substring (so that we remove the *"Chapter "* preceeding every chapter number), and we then convert the string into float type
- We get the chapter publish date by finding the *time* attribute
- We get the direct url link to the chapter by using the *absoulute_links* method, popping the url from a set, and modifying the url so that it gives the link to entire chapter (instead of the first page of the chapter)
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
#### getTimeSinceLastChapter
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
#### getAllChapters
All chapters are listed in a list and all have the [*list-group-item*](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#chapter-entries) attribute. This time we do not use *first=True* when using the *find* method. Doing so allows us to get all instances of the *list-group-item* attribute, which means we have all the chapters. We then iterate through the chapters and store each chapters' information (similarly to the *getLatestChapter* function) into a list, and then return the list.
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
