from flask import Flask, render_template, request, jsonify
import pickle
from gingerit.gingerit import GingerIt
import re

app = Flask(__name__)

parser = GingerIt()


@app.route("/", methods=["GET", "POST"])
def index():
    message = request.form.get("message")
    result = is_spam(message)
    if request.method == "POST":
        return render_template("check.html", message=result)
    return render_template("index.html")


@app.route("/HashboticsAPI/<text>")
def HashboticsAPI(text):
    result = is_spam(text)
    return jsonify(result)


def is_spam(text):
    with open('model_pickle', "rb") as f:
        imported_model = pickle.load(f)
    text = str(text).lower()
    result = imported_model.predict([f"{text}"])
    if result[0] == 1:
        return "spam!"

    li = re.findall(r"[\w']+", text)
    long_words = ["thiruvananthapuram",
                  "pneumonoultramicroscopicsilicovolcanoconiosis",
                  "hippopotomonstrosesquippedaliophobia",
                  "supercalifragilisticexpialidocious",
                  "pseudopseudohypoparathyroidism",
                  "floccinaucinihilipilification",
                  "antidisestablishmentarianism",
                  "honorificabilitudinitatibus",
                  "thyroparathyroidectomized",
                  "dichlorodifluoromethane",
                  "incomprehensibilities"]
    for i in li:
        if len(i) >= 19:
            if i not in long_words:
                return "spam!"
        elif i == "binod":
            return "spam!"

    try:
        for i in li:
            if parser.parse(i)["corrections"][0]["definition"] == None:
                print(i)
                return "spam!"
    except:
        pass
    return "not spam."


if __name__ == "__main__":
    app.run(debug=True)
