#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
import operator
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from slugify import slugify
from nltk.collocations import BigramAssocMeasures, BigramCollocationFinder
from operator import itemgetter

NEWS_ARTICLE_TAILS = ['This is a breaking story and will be updated',  '© 2019 Cable News Network']
WC_height = 500
WC_width = 1000
WC_max_words = 200

def build_latest_news_title_vs_text_hash():
    cnn_newsfeed_url = 'http://lite.cnn.com/en'
    html_text = requests.get(cnn_newsfeed_url).text
    soup = BeautifulSoup(html_text, 'html.parser')

    news_article_links = []

    for link in soup.find_all('a'):
        relative_path = link.get('href')
        if relative_path.startswith('/en/article'):
            news_article_links.append("http://lite.cnn.com{}".format(relative_path))

    news_article_title_vs_texts = {}

    for news_article_link in news_article_links:
        news_article_html_text = requests.get(news_article_link).text
        soup = BeautifulSoup(news_article_html_text, 'html.parser')
        news_div = soup.find_all("div", class_="afe4286c")[0]
        title_text = news_div.find_all("h2")[0].text
        news_text = news_div.find_all("div")[1].text
        news_article_title_vs_texts[title_text] = news_text

    return news_article_title_vs_texts

def prepareStopWords():
    stopwordsList = stopwords.words('english')
    stopwordsList.append('(CNN)')
    stopwordsList.append('updated')
    stopwordsList.append('dont')
    stopwordsList.append('didnt')
    stopwordsList.append('doesnt')
    stopwordsList.append('cant')
    stopwordsList.append('couldnt')
    stopwordsList.append('couldve')
    stopwordsList.append('im')
    stopwordsList.append('ive')
    stopwordsList.append('isnt')
    stopwordsList.append('theres')
    stopwordsList.append('wasnt')
    stopwordsList.append('wouldnt')
    stopwordsList.append('a')
    return stopwordsList

def preprocess_text(rawText):
    # Lowercase and tokenize
    rawText = rawText.lower()
    # Remove single quote early since it causes problems with the tokenizer.
    rawText = rawText.replace("'", "")

    tokens = nltk.word_tokenize(rawText)
    text = nltk.Text(tokens)

    # Load default stop words and add a few more.
    stopWords = prepareStopWords()

    # Remove extra chars and remove stop words.
    text_content = [''.join(re.split("[ .,;:!?‘’``''@#$%^_&*()<>{}~\n\t\\\-]", word)) for word in text]

    text_content = [word for word in text_content if word not in stopWords]

    # After the punctuation above is removed it still leaves empty entries in the list.
    # Remove any entries where the len is zero.
    text_content = [s for s in text_content if len(s) != 0]

    WNL = nltk.WordNetLemmatizer()
    text_content = [WNL.lemmatize(t) for t in text_content]

    return text_content

def generate_frequent_words_wordcloud(title, text_content):
    finder = BigramCollocationFinder.from_words(text_content)
    bigram_measures = BigramAssocMeasures()
    scored = finder.score_ngrams(bigram_measures.raw_freq)

    scoredList = sorted(scored, key=itemgetter(1), reverse=True)
    word_dict = {}

    listLen = len(scoredList)

    for i in range(listLen):
        word_dict['_'.join(scoredList[i][0])] = scoredList[i][1]

    wordCloud = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width)

    wordCloud.generate_from_frequencies(word_dict)

    plt.title(slugify(title))
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.axis("off")

    wordCloud.to_file("bigram/frequent_words/" + slugify(title) + ".png")

def generate_least_frequent_words_wordcloud(title, text_content):
    finder = BigramCollocationFinder.from_words(text_content)
    bigram_measures = BigramAssocMeasures()
    scored = finder.score_ngrams(bigram_measures.raw_freq)
    scoredList = sorted(scored, key=itemgetter(1))
    scoredListLen = len(scoredList)-1
    maxLenCnt = 0
    MINSCORE = 0.000265
    indx = 0
    while (indx < scoredListLen) and (scoredList[indx][1] < MINSCORE):
        indx += 1
    word_dict2 = {}
    while (indx < scoredListLen) and (maxLenCnt < WC_max_words):
        word_dict2['_'.join(scoredList[indx][0])] = scoredList[indx][1]
        indx +=  1
        maxLenCnt += 1

    wordCloud = WordCloud(max_words=WC_max_words, height=WC_height, width=WC_width)
    if len(word_dict2) > 0:
        wordCloud.generate_from_frequencies(word_dict2)
        plt.title(slugify(title))
        plt.imshow(wordCloud, interpolation='bilinear')
        plt.axis("off")
        wordCloud.to_file("bigram/least_frequent_words/" + slugify(title) + ".png")

news_article_title_vs_texts = build_latest_news_title_vs_text_hash()

for title in news_article_title_vs_texts:
    processed_text = preprocess_text(news_article_title_vs_texts[title])
    generate_frequent_words_wordcloud(title, processed_text)
    generate_least_frequent_words_wordcloud(title, processed_text)