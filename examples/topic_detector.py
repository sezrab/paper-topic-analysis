import sys
from os import path

sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import paper_processor
import utils

likelyhood = {
    0.1: "very unlikely",
    0.2: "unlikely, but possible",
    0.3: "somewhat likely",
    0.4: "likely",
    0.5: "very likely",
    0.6: "almost certain"
}

abstract = input("Enter an abstract: ")
tf = paper_processor.tf(abstract)

tvs = utils.load_topic_vector_file()
scores = {}
for topic, tv in tvs.items():
    scores[topic] = paper_processor.cosine_similarity(tf, tv)

print()
topic,maxscore = max(scores.items(), key=lambda x: x[1])
if maxscore < 0.1:
    topic = "undecided"

maxscore_key = min(likelyhood.keys(), key=lambda x: abs(x-maxscore))

print("Topic:", topic.upper(), f"({likelyhood[maxscore_key]} / {maxscore:.2f})")

print()

input("Press enter to see scores...")

print("\nScores:")
for topic, score in scores.items():
    print(f"  {topic:<35}: {score:.2f}")
print()