import json

def dict_print(d, line_length=12, pause=False):
    for key, value in d.items():
        if type(value) == list:
            value = ", ".join(value)
        value = str(value).split(" ")
        
        # split value string into lines of line_length words
        lines = [value[i:i+line_length] for i in range(0, len(value), line_length)]
        print("{:<10} {:<10}".format(str(key), " ".join(lines[0])))
        if len(lines) > 1:
            for line in lines[1:]:
                print("{:<10} {:<10}".format("", " ".join(line)))
    if pause:
        input("Press Enter to continue...")

def load_text(file_name):
    with open(file_name, "r") as f:
        text = f.read()
    return text

def load_lines(file_name):
    with open(file_name, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        
    return lines

def load_topic_vector_file():
    try:
        with open("data/topic_vectors.json", "r") as f:
            topic_vectors = json.load(f)
        return topic_vectors
    except FileNotFoundError:
        return {}
def save_topic_vector_file(topic_vectors):
    with open("data/topic_vectors.json", "w") as f:
        json.dump(topic_vectors, f)