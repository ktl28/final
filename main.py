import urllib.request, urllib.error, urllib.parse, json
from flask import Flask, render_template, request, request
import logging

app = Flask(__name__)

def safe_get(url):
    try:
        return urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print("The server couldn't fulfill the request.")
        print(url)
        print("Error code: ", e.code)
    except urllib.error.URLError as e:
        print("We failed to reach a server")
        print(url)
        print("Reason: ", e.reason)
    return None

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def create(questions,category,difficulty):
    url = "https://opentdb.com/api.php?amount={questions}&category={category}&difficulty={difficulty}&type=multiple".format(questions=questions,category=category,difficulty=difficulty)
    result = safe_get(url)
    if result is not None:
        return json.load(result)

@app.route("/", methods=['GET'])
def main_handler():
    app.logger.info("In Main")
    if request.method == 'GET':
        app.logger.info(request.args.get('category'))
        category = request.args.get('category')
        app.logger.info(request.args.get('questions'))
        questions = request.args.get('questions')
        app.logger.info(request.args.get('difficulty'))
        difficulty = request.args.get('difficulty')
        app.logger.info(request.args.get('players'))
        players = request.args.get('players')

        if category:
            data = create(questions,category,difficulty.lower())
            app.logger.info(data)
            qdict = {}
            hint = {}
            for x in range(int(questions)):
                qdict = data['results'][x]['question']
                hint = options = str(data['results'][x]['incorrect_answers']) + str(data['results'][x]['correct_answer'])
                app.logger.info(hint)
                app.logger.info(qdict)
                return render_template('question.html', qdict=qdict)

    return render_template("home.html")

if __name__ == "__main__":
    # Used when running locally only.
    # When deploying to Google AppEngine, a webserver process
    # will serve your app.
    app.run(host="localhost", port=8080, debug=True)


