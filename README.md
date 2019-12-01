# Product Comment Summarizer

Extracting most commonly occuring bigrams from most positive and most negative comments for a product.

## The problem

The company often needs to know what specific topics their customers are talking about, whether this be good or bad. However, going through all comments of the customers is inefficient. 


## The solution

Find the most common recurring phrases among the good comments and the bad comments and present it. Therefore, a company won’t have to read all customers’ comments.


## Our approach

First we created a scraper that extracts all comments from a product's webpage. Then, we used a bigram collocation finder model to find the most commonly recurring bigrams in all the comments that had one star. Then, we did the same with all the comments with five stars. We created a user-friendly GUI that presents all of the results.
The GUI is in "comment feedback.py".

## What is next?

Bigrams in comments having to do with urgent issues can be found and displayed to the product seller or company. This would allow them to receive instantaneous feedback regarding an urgent issue related to their product or service. Depending on the level of urgency, and automatic emailing or messaging notifier could be set up to alert them as quickly as possible.

## Built With

* [nltk](https://www.nltk.org/): used for nlp, utilized BigramCollocationFinder
* [PyQt5](https://pypi.org/project/PyQt5/): for GUI
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/): for scraping webpage
* [urllib](https://docs.python.org/3/library/urllib.html): for scraping webpage

## Authors
Ibrahim Tigrek
Asim Okby

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

