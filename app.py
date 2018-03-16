from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from nltk import word_tokenize, FreqDist
import string
from nltk.corpus import stopwords
import wordcloud
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import gensim
from nltk.tokenize import word_tokenize

app = Flask(__name__)
stopwords_list = stopwords.words('english') + ['...', '--']
google_url = "https://www.google.com.sg/search?dcr=0&source=hp&ei=wH5dWp_OJIqF8wWp4ISoBg&q="

@app.route('/fetch_from_google')
def fetch_from_google():
    search = request.args.get('query')
    url = google_url + search
    documents = scrap_data(url)
    sims, dictionary, tf_idf = get_similarites(documents)
    query_tf_idf = get_query_doc_tf_idf(search, dictionary, tf_idf)
    messages = get_similar_docs(sims, query_tf_idf, documents)
    return jsonify(messages)


def scrap_data(url):
    response = requests.get(url)
    soupdata = BeautifulSoup(response.text,'html.parser')
    text_data = soupdata.findAll('span',{'class':'st'})
    return clean_scrap_data(text_data)

def clean_scrap_data(data):
    cleaned_documents = []
    for i in data:
        content = i.text.encode('ascii','ignore').decode("utf-8")
        if len(content) == 0: continue
        text = content.split("...")
        text = [ con.replace("\n", '').replace("\xa0", '').replace("\"",'') for con in text if len(con) > 0 ] 
        if re.search("^\d{1,2}\s[a-zA-Z]{3}\s\d{4}",text[0]):
            text = text[1:]
        if len(text) == 0: continue
        if text[-1][-1] != '.':
            text[-1] = ".".join(text[-1].split(". ")[:-1])
        text = [ con.strip() for con in text if con != [''] ] 
        if text == ['']: continue
        cleaned_documents.append("".join(text))
    return cleaned_documents


def get_similarites(documents):
    gen_docs = [[w.lower() for w in word_tokenize(text)] for text in documents]
    dictionary = gensim.corpora.Dictionary(gen_docs)
    corpus = [dictionary.doc2bow(gen_doc) for gen_doc in gen_docs]
    tf_idf = gensim.models.TfidfModel(corpus)
    sims = gensim.similarities.Similarity('./',tf_idf[corpus], num_features=len(dictionary))
    return sims, dictionary, tf_idf

def get_query_doc_tf_idf(query, dictionary, tf_idf):
    query_doc = [w.lower() for w in word_tokenize(query)]
    query_doc_bow = dictionary.doc2bow(query_doc)
    return tf_idf[query_doc_bow]

def get_similar_docs(sims, query_doc_tf_idf, documents):
    doc_with_rank = {}
    for i,val in enumerate(sims[query_doc_tf_idf]):
        doc_with_rank[i] = val
    doc_sims = sorted(doc_with_rank.items(),key=lambda x : x[1],reverse=True)[:5]
    final_text = []
    for index,_ in doc_sims:
        final_text.append(documents[index])
    return final_text
	

	


if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5000)
