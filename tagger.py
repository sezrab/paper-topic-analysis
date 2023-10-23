import paper_processor
import utils

def tag_abstract(abstract, thresh=0.3):
    """
    Given an abstract, returns a list of topics and their corresponding scores based on their similarity to the abstract.
    
    Parameters:
    abstract (str): The abstract to be tagged.
    thresh (float): The threshold for the cosine similarity score. Topics with a score higher than this value will be returned.
    
    Returns:
    list: A list of tuples, where each tuple contains a topic and its corresponding similarity score.
    """
    tf = paper_processor.tf(abstract)

    tvs = utils.load_topic_vector_file()
    
    topics = []
    for topic, tv in tvs.items():
        score = paper_processor.cosine_similarity(tf, tv)
        topics.append((topic, score))

    # get mean score
    mean_score = sum([score for _, score in topics]) / len(topics)
    
    # get standard deviation
    std_dev = (sum([(score - mean_score)**2 for _, score in topics]) / len(topics))**0.5
    
    # get scores more than 2 standard deviation above the mean
    topics = [(topic, score) for topic, score in topics if score > mean_score + 1.3*std_dev and score > thresh]
    
    # sort topics by score
    topics.sort(key=lambda x: x[1], reverse=True)
    
    # return topic titles
    return [topic for topic, _ in topics]