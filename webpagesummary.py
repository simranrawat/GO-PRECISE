# -*- coding: utf-8 -*-


#Importing required libraries
from string import punctuation
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize 
import urllib.request  
import bs4 as BeautifulSoup
import nltk


def generate_summary2(lnk):
    text = urllib.request.urlopen(lnk)
    article = text.read()
    article_parsed = BeautifulSoup.BeautifulSoup(article,'html.parser')
    paragraphs = article_parsed.find_all('p')
    article_content = ''
    for p in paragraphs:  
        article_content += p.text
    tokens = word_tokenize(article_content)
    nltk.download("stopwords")
    stop_words = stopwords.words('english')
    from string import punctuation
    punctuation = punctuation + '\n'
    word_frequencies = {}
    for word in tokens:    
        if word.lower() not in stop_words:
            if word.lower() not in punctuation:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
    max_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency
    sent_token = sent_tokenize(article_content)
    sentence_scores = {}
    for sent in sent_token:
        sentence = sent.split(" ")
        for word in sentence:        
            if word.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.lower()]
    from heapq import nlargest
    select_length = int(len(sent_token)*0.3)
    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)
    final_summary = [word for word in summary]
    summary = ' '.join(final_summary)
    return summary,len(article_content),len(summary)
