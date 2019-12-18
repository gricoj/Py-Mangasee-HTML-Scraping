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
We use the [*request-html*](https://pypi.org/project/requests-html/) package so that we can easily parse HTML. We use the [*datetime*](https://docs.python.org/3/library/datetime.html) to get the time since a new chapter has been released.

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
```python
session = HTMLSession()
r = session.get(Manga_URL)
```
#### Getting Series Name
We first start off by looking for the element with class attribute *SeriesName*:
```r.html.find('.SeriesName',first=True)```

This will return the HTML element:
```<h1 class="SeriesName">One Piece</h1>```

We then get the Series' Name by getting the HTML element's text contents:
```(r.html.find('.SeriesName',first=True)).text```

This returns the Series' Name:
```One Piece```
