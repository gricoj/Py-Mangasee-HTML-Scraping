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
#### Getting the Series Name
We start off by looking for the element with class attribute *SeriesName*:

```python
r.html.find('.SeriesName',first=True)
```

This would return the HTML element:

```html
<h1 class="SeriesName">One Piece</h1>
```

Inorder to get the Series' Name we need to get the HTML element's text contents:

```python
(r.html.find('.SeriesName',first=True)).text
```

This returns the Series' Name:

```One Piece```

#### Getting the Latests Chapter's Chapter Number, Chapter Publish Date and Chapter URL
We start off by finding and storing the latests chapter's HTML. We use the *first=True* argument so that we are only returned the first chapter entry (chapter entries have class attribute *list-group-item*):

```python
Latest_Chapter = r.html.find('.list-group-item',first=True)
```
##### Chapter Number
Getting the Chapter Number requires us to look for the class attribute *chapterLabel*:

```html
<span class="chapterLabel">Chapter 964</span>
```

We want to extract the ```964``` from the HTML. We would do this by first getting the element's text contents ```Chapter 964``` and splitting that string into a list of strings with *space* as the seperator (I opted for using this method for extracting chapter number because there are mangas that have their *chapter titles* stylized differntly. Most often chapters are simply stylized *Chapter XXX* but there some that do not i.e. One-Punch Man stylizes it's chapters *Punch XXX*, Dr.Stone stylizes it's chapters *Z= XXX*. The one thing they have in common is that there is a space before the actual chapter number). We finally convert the chapter number from type string to type float (We dont convert to type int because *bonus* chapters in a series are labeled *XXX.X*).

```python
Chapter_Number = float(((Latest_Chapter.find('.chapterLabel',first=True)).text).split(" ")[1])
```

