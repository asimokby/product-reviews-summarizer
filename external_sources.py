import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.tokenize.regexp import RegexpTokenizer


def get_bigram_likelihood(statements, stopwords=[], freq_filter=3, nbest=200):
    """
    Returns n (likelihood ratio) bi-grams from a group of documents
    :param        statements: list of strings
    :param output_file: output path for saved file
    :param freq_filter: filter for # of appearances in bi-gram
    :param       nbest: likelihood ratio for bi-grams
    """

    words = list()
    # print('Generating word list...')
    #tokenize sentence into words
    for statement in statements:
        # remove non-words
        tokenizer = RegexpTokenizer(r'\w+')
        words.extend(tokenizer.tokenize(statement))

    bigram_measures = nltk.collocations.BigramAssocMeasures()
    bigram_finder = BigramCollocationFinder.from_words(words)

    # only bi-grams that appear n+ times
    bigram_finder.apply_freq_filter(freq_filter)

    # TODO: use custom stop words
    stop = nltk.corpus.stopwords.words('turkish') + stopwords
    bigram_finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in stop)

    bigram_results = bigram_finder.nbest(bigram_measures.likelihood_ratio, nbest)

    return bigram_finder.score_ngrams(bigram_measures.likelihood_ratio) 

def get_stop_words(one_star_reviews, five_star_reviews):
    stopwords = nltk.corpus.stopwords.words('turkish')

    one_star_all_words = []
    for text in one_star_reviews:
        one_star_all_words.extend(nltk.tokenize.word_tokenize(text))

    one_star_common_words = nltk.FreqDist(w.lower() for w in one_star_all_words if w not in stopwords)
    one_star_common_words = one_star_common_words.most_common(100)
    one_star_common_words = [x[0] for x in one_star_common_words]

    five_star_all_words = []
    for text in five_star_reviews:
        five_star_all_words.extend(nltk.tokenize.word_tokenize(text))

    five_star_common_words = nltk.FreqDist(w.lower() for w in five_star_all_words if w not in stopwords)
    five_star_common_words = five_star_common_words.most_common(100)
    five_star_common_words = [x[0] for x in five_star_common_words]

    common_words = []
    for word in one_star_common_words:
        if word in five_star_common_words:
            common_words.append(word)

    return common_words