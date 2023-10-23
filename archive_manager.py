# the archive manager is responsible for scraping arxiv maximum once a day and storing the results as json files named by date

import scraper
import tagger
import json
import os
from datetime import datetime, timedelta

# set up constants
ARCHIVE_DIR = "data/archive"
ARCHIVE_INTERVAL = timedelta(days=1)

def manage(now = datetime.now()):
    # create archive directory if it doesn't exist
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    # check if archive for today already exists
    archive_filename = os.path.join(ARCHIVE_DIR, datetime.today().strftime("%Y-%m-%d") + ".json")
    if os.path.exists(archive_filename):
        return False
    else:
        # scrape arxiv
        results = scraper.scrape_arxiv_until("ai", now - ARCHIVE_INTERVAL)
        
        for result in results:
            result["tags"] = tagger.tag_abstract(result["abstract"], thresh=0.23)

        # save results to file
        with open(archive_filename, "w") as f:
            for result in results:
                result["submitted"] = result["submitted"].strftime("%Y-%m-%d")
            json.dump(results, f, default=str)

        print("Archive saved to", archive_filename)
        
    return True

    # # clean up old archives
    # for filename in os.listdir(ARCHIVE_DIR):
    #     filepath = os.path.join(ARCHIVE_DIR, filename)
    #     if os.path.isfile(filepath):
    #         filetime = datetime.strptime(filename[:-5], "%Y-%m-%d")
    #         if now - filetime > ARCHIVE_INTERVAL:
    #             os.remove(filepath)
    #             print("Removed old archive", filepath)

def fetch(start=datetime.today(), stop=datetime.today()):
    start = start.replace(hour=23, minute=59, second=59)
    # fetch archives from start to stop (inclusive)
    # returns a list of json objects
    # assumes start and stop are datetime objects
    archives = []
    file_date = start
    while file_date >= stop:
        archive_filename = os.path.join(ARCHIVE_DIR, file_date.strftime("%Y-%m-%d") + ".json")
        if os.path.exists(archive_filename):
            with open(archive_filename, "r") as f:
                for p in json.load(f):
                    p_date = datetime.strptime(p["submitted"], "%Y-%m-%d")
                    # if publish date between start date and stop date
                    if p_date <= start and p_date >= stop:
                        archives.append(p)
        file_date -= ARCHIVE_INTERVAL
    return archives

if __name__ == "__main__":
    import utils
    days = input("How many days to look back? ")
    days = int(days)
    find_date = datetime.today() - timedelta(days=days)
    manage(find_date)
    [utils.dict_print(d, pause=True) for d in fetch(stop=find_date)]