from flask import Flask, request
import archive_manager
from datetime import datetime, timedelta
app = Flask(__name__)

@app.route('/today', methods=['POST','GET'])
def today():
    if archive_manager.manage():
        print("Archive created.")
    else:
        print("Archive already exists.")
        pass
    print("Fetching archives...")
    papers = archive_manager.fetch()
    # output papers as json
    return papers
    
@app.route('/week', methods=['POST','GET'])
def week():
    week_start = datetime.today() - timedelta(days=7)
    week_end = datetime.today()
    if archive_manager.manage(week_end):
        print("Archive created.")
    else:
        print("Archive already exists.")
        pass
    print("Fetching archives...")
    papers = archive_manager.fetch(week_end, week_start)
    # output papers as json
    return papers


if __name__ == '__main__':
    app.run(debug=True)
