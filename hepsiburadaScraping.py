from  urllib.request import urlopen
from bs4 import BeautifulSoup

def get_reviews_from_page(review_blocks, review_rating):
    for block in review_blocks: 
        review = block.find("p", {"class": "review-text"}).text  #getting the text of the review
        rating = int(block.findAll("div", attrs ={"class": "ratings active"})[0].attrs['style'].split()[1][:-1])/20 # 1 star == width: 20%
        review_rating.append((review, rating))


def get_reviews(url):
    pagin = 1
    review_rating = [] # list of tuples. Each tuple contains (review, rating)
    while True:
        pre_url = url+'?sayfa=%g'%pagin
        page = urlopen (pre_url)

        # soup = BeautifulSoup(page, "html5lib") # didn't work, tried parser
        soup = BeautifulSoup(page, "html.parser")

        review_blocks = soup.find_all("li", {"class": "review-item"}) #getting all blocks of reviews (listed reviews)
        get_reviews_from_page(review_blocks, review_rating) 
        if len(review_blocks) < 20: # each page contains 20, so if a page is less than 20, break.
            break
        pagin+= 1 
    return review_rating

    
#TODO remove the deafult 


# creating one_star_reviews, and five_star_reviews lists 
def star_reviews(rating, url):
    reviews = get_reviews(url)
    star_reviews = []
    for review in reviews:
        if review[1] == rating:
            star_reviews.append(review)
    return star_reviews

## Ibrahim
def star_reviews_ibrahim(target_rating, reviews, ratings):
    star_reviews = []
    for ind, rating in enumerate(ratings):
        if rating == target_rating:
            star_reviews.append(reviews[ind])
    return star_reviews

# for hepsiburada.com
def is_yorum_page(url):
    yorum_suffix = "-yorumlari"
    if len(url) < len(yorum_suffix):
        raise ValueError("invalid url")

    if url[-10:] == yorum_suffix:
        return True
    return False

# for hepsiburada.com
def get_yorum_page(url):
    if is_yorum_page(url):
        return url

    yorum_suffix = "-yorumlari"

    for i in range(len(url) - 1, -1, -1):
        if url[i] == "?":
            url = url[:i] + yorum_suffix
            return url
    url = url + yorum_suffix
    return url

