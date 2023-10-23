from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_arxiv(query, page=0, stop_date=None):
    """
    Scrapes the arXiv website for papers related to the given query.

    Args:
        query (str): The search query to use.

    Returns:
        list: A list of dictionaries, where each dictionary represents a paper and contains the following keys:
            - title (str): The title of the paper.
            - authors (list): A list of the authors of the paper.
            - abstract (str): The abstract of the paper.
            - link (str): The link to the paper on the arXiv website.
    """
    
    # base url
    base_url = "https://arxiv.org/search/?searchtype=all&start={}&source=header&query={}"

    # format query
    query = query.replace(" ", "+")

    # create url
    url = base_url.format(page*50,query)

    # send a GET request to the url and parse the response using BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # get all the li with class arxiv-result
    results = soup.find_all("li", class_="arxiv-result")

    # create an empty list to store the scraped papers
    papers = []

    # loop through each result and extract the relevant information
    for result in results:
        paper = {}

        # get the title
        title = result.find("p", class_="title is-5 mathjax").text.strip()
        paper["title"] = title

        # get the authors
        author_line = result.find("p", class_="authors").text.strip().replace("Authors:\n", "")
        authors = [athr.strip() for athr in author_line.split(",")]
        paper["authors"] = authors

        # get the abstract
        abstract = result.find("span", class_="abstract-full has-text-grey-dark mathjax").text.replace("△ Less","").strip()
        paper["abstract"] = abstract

        # get the submitted date
        submitted = result.find("p", class_="is-size-7").text.split(";")[0].strip()[10:]
        submitted = datetime.strptime(submitted, "%d %B, %Y")        
        paper["submitted"] = submitted
        
        if stop_date and submitted < stop_date:
            return papers
        
        # get the link(s)
        try:
            link = result.find("p", class_="list-title is-inline-block").find("span").find("a")["href"]
        except TypeError:
            link = None
        paper["link"] = link
        
        # append the paper to the list of papers
        papers.append(paper)

    return papers

def scrape_arxiv_until(query, stop_date):
    """
    Scrapes the arXiv website for papers related to the given query until the given date.

    Args:
        query (str): The search query to use.
        stop_date (datetime): The date to stop scraping at.

    Returns:
        list: A list of dictionaries, where each dictionary represents a paper and contains the following keys:
            - title (str): The title of the paper.
            - authors (list): A list of the authors of the paper.
            - abstract (str): The abstract of the paper.
            - link (str): The link to the paper on the arXiv website.
    """
    
    # create an empty list to store the scraped papers
    papers = []

    # scrape arxiv until stop_date is reached
    page = 0
    while True:
        page_papers = scrape_arxiv(query, page)
        if len(page_papers) == 0:
            break
        papers.extend(page_papers)
        if page_papers[-1]["submitted"] < stop_date:
            break
        page += 1

    return papers

if __name__ == "__main__":
    import utils
    query = input("Search query: ")
    papers = scrape_arxiv(query)
    for p in papers:
        utils.dict_print(p)
        input()