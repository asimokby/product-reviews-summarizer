from PyQt5.QtCore import QDate, QLocale, Qt, QTimer, QPoint
from PyQt5.QtGui import QFont, QTextCharFormat, QPixmap, QColor, QPainter, QPen, QBrush
from PyQt5.QtWidgets import (QApplication, QCalendarWidget, QCheckBox,
        QComboBox, QDateEdit, QGridLayout, QGroupBox, QHBoxLayout, QLabel,
        QLayout, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QTextEdit, QListWidget, QListWidgetItem)
import random
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.tokenize.regexp import RegexpTokenizer

##
from hepsiburadaScraping import get_reviews  # scraping reviews
from hepsiburadaScraping import star_reviews, star_reviews_ibrahim # get reviews according to rating
from hepsiburadaScraping import get_yorum_page # change to yorum page of product

from external_sources import get_bigram_likelihood, get_stop_words
##

import logging as log
# log.basicConfig(level=log.DEBUG)
log.debug("DEBUGGING")
###########################
WINDOW_WIDTH, WINDOW_HEIGHT = 1300, 600
header_style = 'QGroupBox  {font-size: 16px; font:bold}'
############################

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(20, 40, WINDOW_WIDTH, WINDOW_HEIGHT)
        self.createGroupBoxes()
        self.setupLayout()
        self.show()

    def createGroupBoxes(self):
        # default_url = "https://www.hepsiburada.com/goldmaster-power-in-6100-erkek-bakim-seti-9-in-1-p-HBV00000LG19F-yorumlari"
        default_url = "https://www.hepsiburada.com/huawei-p-smart-2019-64-gb-huawei-turkiye-garantili-p-HBV00000OUFUK?magaza=Hepsiburada"
        ######### Url Scraping
        self.text_input = QLineEdit() 
        self.urlGroupBox = QGroupBox("Url Scraping")

        
        self.text_input.setText(default_url)
        layout = QGridLayout()
        layout.addWidget(self.text_input, 0, 0)
        pushButton = QPushButton("Scrape comments")
        pushButton.clicked.connect(self.pushButtonPressed)
        layout.addWidget(pushButton, 0, 1)
        self.urlGroupBox.setLayout(layout)
        ######## Comment List
        self.commentListGroupBoxTitle = "Comment List"
        self.commentListGroupBox = QGroupBox(self.commentListGroupBoxTitle)
        self.commentListGroupBox.setStyleSheet(header_style)
        layout = QGridLayout()
        self.commentListWidget = QListWidget()
        self.commentListWidget.setWordWrap(True)
        layout.addWidget(self.commentListWidget)
        self.commentListGroupBox.setLayout(layout)
        ####### Positive comments
        self.posCommentListGroupBoxTitle = "Very Positive Comments"
        self.posCommentListGroupBox = QGroupBox(self.posCommentListGroupBoxTitle)
        self.posCommentListGroupBox.setStyleSheet(header_style)
        layout = QGridLayout()
        self.posCommentListWidget = QListWidget()
        self.posCommentListWidget.setWordWrap(True)
        layout.addWidget(self.posCommentListWidget)
        self.posCommentListGroupBox.setLayout(layout)
        ###### Negative comments
        self.negCommentListGroupBoxTitle = "Very Negative Comments"
        self.negCommentListGroupBox = QGroupBox(self.negCommentListGroupBoxTitle)
        self.negCommentListGroupBox.setStyleSheet(header_style)
        layout = QGridLayout()
        self.negCommentListWidget = QListWidget()
        self.negCommentListWidget.setWordWrap(True)
        layout.addWidget(self.negCommentListWidget)
        self.negCommentListGroupBox.setLayout(layout)
        ####### Feedback
        self.createFeedbackGroupBoxes()

    def createFeedbackGroupBoxes(self):
        self.posFeedbackGroupBox = QGroupBox("Most Common Positive Feedback")
        self.posFeedbackGroupBox.setStyleSheet(header_style)
        layout = QGridLayout()
        self.positiveFeedbackTextEdit = QTextEdit()
        self.positiveFeedbackTextEdit.setReadOnly(True)
        self.positiveFeedbackTextEdit.setStyleSheet("background-color: rgb(204, 255, 204);")
        layout.addWidget(self.positiveFeedbackTextEdit)
        self.posFeedbackGroupBox.setLayout(layout)
        ###################
        self.negFeedbackGroupBox = QGroupBox("Most Common Negative Feedback")
        self.negFeedbackGroupBox.setStyleSheet(header_style)
        layout = QGridLayout()
        self.negativeFeedbackTextEdit = QTextEdit()
        self.negativeFeedbackTextEdit.setReadOnly(True)
        self.negativeFeedbackTextEdit.setStyleSheet("background-color: rgb(255, 204, 204);")
        layout.addWidget(self.negativeFeedbackTextEdit)
        self.negFeedbackGroupBox.setLayout(layout)

        
    def setupLayout(self):
        layout = QGridLayout()
        layout.addWidget(self.urlGroupBox, 0, 0, 1, 3)
        layout.addWidget(self.commentListGroupBox, 1, 0, 2, 1)
        layout.addWidget(self.posCommentListGroupBox, 1, 1)
        layout.addWidget(self.negCommentListGroupBox, 2, 1)
        layout.addWidget(self.posFeedbackGroupBox, 1, 2)
        layout.addWidget(self.negFeedbackGroupBox, 2, 2)
        self.setLayout(layout)

    def populateComments(self):
        starred_reviews = []
        for rating, review in list(zip(self.ratings, self.reviews)):
            text = "★" * int(rating)
            text += "☆" * (5 - int(rating))
            text += "   " + review
            starred_reviews.append(text)
        # change title
        self.commentListGroupBox.setTitle(f"{self.commentListGroupBoxTitle} ({len(starred_reviews)})")
        self.populate(self.commentListWidget, starred_reviews)
        # self.commentListWidget.addItem(QListWidgetItem(text))

    def populateFeedback(self):        
        feedback = self.getFeedback(self.one_star_reviews)
        self.negativeFeedbackTextEdit.clear()
        self.negativeFeedbackTextEdit.append(feedback)
        feedback = self.getFeedback(self.five_star_reviews)
        self.positiveFeedbackTextEdit.clear()
        self.positiveFeedbackTextEdit.append(feedback)

        bad_reviews = []
        for review in self.one_star_reviews:
            text = "★☆☆☆☆   "
            text += review
            bad_reviews.append(text)
        # change title
        self.negCommentListGroupBox.setTitle(f"{self.negCommentListGroupBoxTitle} ({len(bad_reviews)})")
        self.populate(self.negCommentListWidget, bad_reviews, colors=[QColor(255, 204, 204), QColor(255, 255, 255)])

        good_reviews = []
        for review in self.five_star_reviews:
            text = "★★★★★   "
            text += review
            good_reviews.append(text)
        # change title        
        self.posCommentListGroupBox.setTitle(f"{self.posCommentListGroupBoxTitle} ({len(good_reviews)})")
        self.populate(self.posCommentListWidget, good_reviews, colors=[QColor(204, 255, 204), QColor(255, 255, 255)])

    def populate(self, listWidget, docs, colors=None):
        listWidget.clear()
        coin = 0
        if not colors:
            gray = QColor(232, 232, 232) # QColor("lightGray")
            colors = [gray, QColor("white")]
        for doc in docs:
            item = QListWidgetItem(doc)
            item.setBackground(colors[coin])
            listWidget.addItem(item)
            coin = (coin + 1) % 2

    def getFeedback(self, reviews):
        # stopwords = get_stop_words(self.one_star_reviews, self.five_star_reviews)
        stopwords = []
        feedback = ""
        for t in get_bigram_likelihood(reviews, stopwords=stopwords):
            feedback += f"\"{t[0][0]} {t[0][1]}\", "
        if feedback != "":
            feedback = feedback[:-2]
        return feedback

    def getReviews(self, url):
        reviews_with_ratings = get_reviews(url)
        self.reviews, self.ratings = list(zip(*reviews_with_ratings))
        self.one_star_reviews = star_reviews_ibrahim(1.0, self.reviews, self.ratings)
        self.five_star_reviews = star_reviews_ibrahim(5.0, self.reviews, self.ratings)

    def pushButtonPressed(self):
        input_url = self.text_input.text() # get the inputted text
        url = get_yorum_page(input_url)
        self.getReviews(url)

        self.populateComments() # all the comments get populated on the left side
        self.populateFeedback()
  

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    window.show()

    sys.exit(app.exec_())