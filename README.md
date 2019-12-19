# Mangasee HTML Scraping
We will be scraping [Mangasee](https://mangaseeonline.us) as it is a one of the better manga sources. The information we will be scraping includes: Series Name, Chapter Numbers, Publish Dates, and URL to the chapter. The purpose of this module is to eventually use it to get notified when a new chapter for a series is published.

## Table of Contents
[HTML](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#html)

[Installing Required Packages](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#installing-required-packages)

[Scraping](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#scraping)

[Manga Class](https://github.com/gricoj/Py-Mangasee-HTML-Scraping#manga-class)

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
  <i class="hidden-xs"></i>
  <time class="SeriesTime pull-right" datetime="2019-11-29T05:13:28+00:00" datestring="20191129">11/29/2019</time>
</a>
```
#### Chapter Entries:
```html
<div class="list chapter-list">
  <a class="list-group-item" chapter="964" href="/read-online/One-Piece-chapter-964-page-1.html" title="Read One Piece Chapter 964 For Free Online">
    <span class="chapterLabel">Chapter 964</span>
    <i class="hidden-xs"></i>
    <time class="SeriesTime pull-right" datetime="2019-11-29T05:13:28+00:00" datestring="20191129">11/29/2019</time>
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

## Scraping
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
Getting the Chapter Number requires us to look for the element with class attribute *chapterLabel*:

```html
<span class="chapterLabel">Chapter 964</span>
```

We want to extract the ```964``` from the HTML above. We would do this by first getting the element's text contents ```Chapter 964``` and splitting that string into a list of strings with *space* as the seperator (I opted for using this method for extracting chapter number because there are mangas that have their *chapter titles* stylized differntly. Most often chapters are simply stylized *Chapter XXX* but there some that do not i.e. One-Punch Man stylizes it's chapters *Punch XXX*, Dr.Stone stylizes it's chapters *Z= XXX*. The one thing they have in common is that there is a space before the actual chapter number). We finally convert the chapter number from type string to type float (We dont convert to type int because *bonus* chapters in a series are labeled *XXX.X*).

```python
Chapter_Number = float(((Latest_Chapter.find('.chapterLabel',first=True)).text).split(" ")[1])
```

##### Chapter Publish Date
Getting the date the chapter was published requires us to look for the element with tag *time*:

```html
<time class="SeriesTime pull-right" datetime="2019-11-29T05:13:28+00:00" datestring="20191129">11/29/2019</time>
```

We want to extract the ```11/29/2019``` from the HTML above. Simarly to getting the Series Name, we simply need to get the HTML element's text contents.

```python
Chapter_PD = (Latest_Chapter.find('time',first=True)).text
```

##### Chapter URL
Getting the link to the chapter requires us to use the *absolute_links* method

```python
Chapter_URL = ((Latest_Chapter.absolute_links).pop()).replace("-page-1","")
```

Calling the *absolute_links* method returns a set of all abosolute links in the HTML element:
```https://mangaseeonline.us/read-online/One-Piece-chapter-964-page-1.html```

Since the link is stored in a set, we must pop the link from the set. We then want to format the chapter url such that we get a link to the entire chapter ```https://mangaseeonline.us/read-online/One-Piece-chapter-964.html``` this is done by replacing the *"-page-1"* in the string with nothing.

#### Getting all Chapters in a series
We can get all chapters in a series by looking for the *list-group-item* class attribute, but this time we do not use the *first=True* argument doing so will return list of HTML elements:

```python
Chapters = r.html.find('.list-group-item')
```

We can iterate throught entry and we can follow the same steps as above to get each chapter's Chapter Number, Chapter Publish Date and Chapter URL:

```python
for chapter in Chapters:
  Chapter_Number = float(((chapter.find('.chapterLabel',first=True)).text).split(" ")[1])
  Chapter_URL = ((chapter.absolute_links).pop()).replace("-page-1","")
  Chapter_PD = (chapter.find('time',first=True)).text
```

#### Getting time since the Latest Chapter was published
We start off by getting the latest chapter entry:

```python
Latest_Chapter = r.html.find('.list-group-item',first=True)
```

We then look for the *time* attribute to get the HTML:

```python
(Latest_Chapter.find('time',first=True).html)
```
```html
<time class="SeriesTime pull-right" datetime="2019-11-29T05:13:28+00:00" datestring="20191129">11/29/2019</time>
```
We want to extract the ```2019-11-29T05:13:28```. We first split the string with *"* as the seperator, we get ```2019-11-29T05:13:28+00:00``` by selecting the string with index 3. We then split the string again with *+* as the seperator to ger rid of the ```+00:00```.

```python
Time = ((Latest_Chapter.find('time',first=True).html).split('"')[3]).split("+")[0]
```

Using the datetime module we format the time the chapter was published, we get the time, and find the time elapsed since the last chapter was published:

```python
date_format = "%Y-%m-%dT%H:%M:%S"
newTime = (datetime.strptime(Time,date_format)).strftime(date_format)
currentTime = (datetime.utcnow()).strftime(date_format)
tdelta = datetime.strptime(currentTime, date_format) - datetime.strptime(newTime, date_format)
```

## Manga Class
Creating this class will allow us to create *Chapter Objects* which will allow us to store the information we gather into one object.

```python
class Chapter_OBJ:
    def __init__(self, series, chapter_number, date_published, url):
        self.series = series
        self.chapter_number = chapter_number
        self.date_published = date_published
        self.url = url
```

We specify 4 attributes: 
- series: Will store the manga series' name (string)
- chapter_number: Will store the chapter number (float)
- date_published: Will store the date the chapter was published on Mangasee (float)
- url: Will store the direct link to the particular chapter (string)

## Using the functions
```getLatestChapter```, ```getAllChapters```, and ```getTimeSinceLastChapter``` all take *Manga_URL* as an argument. *Manga_URL* refers to the manga series' main page ```i.e. https://mangaseeonline.us/manga/One-Piece```.

```getLatestChapter```: Returns an object of type *Chapter_OBJ*

```getAllChapters```: Returns a list of objects type *Chapter_OBJ*

```getTimeSinceLastChapter```: Returns
