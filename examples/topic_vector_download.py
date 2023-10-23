import sys
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import paper_processor
import scraper
import utils

tvs = utils.load_topic_vector_file()

print("Topics: "+", ".join(tvs.keys()))

topic = input("Enter a topic: ")

print(f"Scraping topic '{topic}'...")
abstracts = []
for i in range(5):
    papers = scraper.scrape_arxiv(topic)
    abstracts += [paper["abstract"].lower() for paper in papers]
print(f"Analysing topic '{topic}'...")
abstracts = " ".join(abstracts)

tf = paper_processor.tf(abstracts)
tvs[topic] = tf
utils.save_topic_vector_file(tvs)