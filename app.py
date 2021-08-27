from flask import Flask, render_template, request
import pickle
from gingerit.gingerit import GingerIt

app = Flask(__name__)

parser = GingerIt()


@app.route("/", methods=["GET", "POST"])
def index():
    message = request.form.get("message")
    result = is_spam(message)
    if request.method == "POST":
        return render_template("check.html", message=result)
    return render_template("index.html")


def is_spam(text):
    with open('model_pickle', "rb") as f:
        imported_model = pickle.load(f)
    text = str(text)
    text = text.replace("\n", " ").lower()
    result = imported_model.predict([f"{text}"])
    if result[0] == 1:
        return "spam!"

    li = text.split()
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
        if i not in long_words:
            if len(i) >= 19:
                return "spam!"

    for j in range(len(parser.parse(text)["corrections"])):
        if parser.parse(text)["corrections"][j]["definition"] == None:
            return "spam!"
    return "not spam"


if __name__ == "__main__":
    app.run(debug=True)
