# Tech Review
 
## Prerequesites to run this project:
 python3
 
 
## Running the project
```shell script
 git clone https://github.com/rakesh-patnaik/tech_review.git
 cd tech_review/code
 python -m venv env
 source env/bin/activate
 pip install --upgrade pip
 pip install matplotlib
 pip install wordcloud
 pip install pandas
 pip install nltk
 python -m pip install lxml bs4 requests
 python  -m pip install python-slugify
 python -m nltk.downloader stopwords
 python -m nltk.downloader punkt
 python -m nltk.downloader wordnet
 mkdir -p unigram/least_frequent_words
 mkdir -p unigram/frequent_words
 mkdir -p bigram/least_frequent_words
 mkdir -p bigram/frequent_words
```
### Unigram WordClouds: Execute code to generate
```shell script
python3 unigram_cnn_news_wordcloud.py
```

this creates wordclouds under <current dir>/unigram/frequent_words and <current dir>/unigram/least_frequent_words


### Bigram WordClouds: Execute code to generate 
```shell script
python3 bigram_cnn_news_wordcloud.py
```

this creates wordclouds under <current dir>/bigram/frequent_words and <current dir>/bigram/least_frequent_words
