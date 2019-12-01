## The problem
The company often needs to know what specific topics their customers are talking about, whether this be good or bad.

## The solution
Find the most common recurring phrases among the good reviews and the bad reviews and present it.

## Our approach
First we created a scraper that extracts all comments from a product's webpage. Then, we used a bigram collocation finder model to find the most commonly recurring bigrams in all the reviews that had one star. Then, we did the same with all the reviews with five stars. We created a user-friendly GUI that presents all of the results.
The GUI is in "comment feedback.py".

## What is next?
Bigrams having to do with urgent issues can be found and displayed to the product seller or company. This would allow them to receive instantaneous feedback regarding an urgent issue related to their product or service. Depending on the level of urgency, and automatic emailing or messaging notifier could be set up to alert them as quickly as possible.

## Packages
The packages we used:
- nltk
  - BigramCollocationFinder
  - word_tokenize
  - RegexpTokenizer
- PyQt5
- BeautifulSoup
- urlopen
 

