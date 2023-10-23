import math
import string
import numpy as np
from wordcloud import WordCloud
import scraper
import utils
from matplotlib import pyplot as plt

stopwords = utils.load_lines("data/stopwords.txt")

def remove_punctuation(text):
    return "".join([c for c in text if c not in string.punctuation])

def stem_word(word):
    if word.endswith("ing"):
        return word[:-3]
    elif word.endswith("ed"):
        return word[:-2]
    elif word.endswith("s"):
        return word[:-1]
    return word

def tokenize(text):
    text = remove_punctuation(text.lower())
    words = sorted(filter(lambda x: x not in stopwords, text.split()))
    return words

def tf(text):
    tokens = tokenize(text)
    total_terms = len(tokens)
    term_freq = {}
    for word in tokens:
        stem = stem_word(word)
        if word in term_freq:
            term_freq[word] += 1
        else:
            if stem in term_freq:
                term_freq[stem] += 1
            else:
                term_freq[word] = 1
    return {k: v/total_terms for k, v in term_freq.items() if v/total_terms > 0.0008}

def cosine_similarity(tf1, tf2):
    # get the unique words from both the documents
    words = set(tf1.keys()).union(set(tf2.keys()))

    # create two vectors with length equal to the number of unique words
    v1 = np.zeros(len(words))
    v2 = np.zeros(len(words))

    # fill the vectors with frequency of occurence of the words
    # the order of the words in the vector is the same as the order in the set words
    for i, word in enumerate(words):
        v1[i] = tf1.get(word, 0)
        v2[i] = tf2.get(word, 0)

    # calculate the cosine similarity
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

if __name__ == "__main__":   
    q = input("Search query: ")
    papers = []
    for page in range(5):
        papers += scraper.scrape_arxiv(q, page)
        

    abstracts = " ".join([paper["abstract"].lower() for paper in papers])

    # perform frequency analysis on all the abstracts
    tf = tf(abstracts)
        
    # Generate a word cloud image
    wc = WordCloud(background_color='white', colormap='plasma', width=1600, height=1600).generate_from_frequencies(tf)
    plt.figure(figsize=(10, 10))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.savefig('wordcloud_{}.png'.format(q.replace(" ","_")), facecolor='k', bbox_inches='tight')