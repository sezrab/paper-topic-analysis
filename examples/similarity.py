import sys
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import paper_processor
import scraper

topic_1 = "machine learning"
topic_2 = "deep learning"
topic_3 = "hawking radiation"

def scrape_and_analyse(q):
    print(f"Scraping topic '{q}'...")
    abstracts = []
    for i in range(4):
        papers = scraper.scrape_arxiv(q)
        abstracts += [paper["abstract"].lower() for paper in papers]
    print(f"Analysing topic '{q}'...")
    abstracts = " ".join(abstracts)
    return paper_processor.tf(abstracts)

f1 = scrape_and_analyse(topic_1)
f2 = scrape_and_analyse(topic_2)
f3 = scrape_and_analyse(topic_3)

print(f"Similarity between '{topic_1}' and '{topic_2}': {paper_processor.cosine_similarity(f1, f2):.2f}")
print(f"Similarity between '{topic_1}' and '{topic_3}': {paper_processor.cosine_similarity(f1, f3):.2f}")
