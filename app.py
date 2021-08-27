from flask import Flask, render_template, request
import pickle
import language_tool_python

app = Flask(__name__)


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
    text = text.replace("\n", " ")
    result = imported_model.predict([f"{text}"])
    if result[0] == 1:
        return "spam!"
    intensly_spam(text)


def intensly_spam(text):
    text = text.capitalize()
    li = text.lower().split()
    long_words = ["thiruvananthapuram",
                  "pneumonoultramicroscopicsilicovolcanoconiosis",
                  "hippopotomonstrosesquippedaliophobia",
                  "supercalifragilisticexpialidocious",
                  "pseudopseudohypoparathyroidism",
                  "floccinaucinihilipilification",
                  "antidisestablishmentarianism",
                  "honorificabilitudinitatibus",
                  "thyroparathyroidectomized",
                  "dichlorodifluoromethane", "incomprehensibilities"]
    for i in li:
        if i not in long_words:
            if len(i) >= 19:
                return "spam!"
    matches = tool.check(text)
    try:
        if len(matches[0].__dict__.get("replacements")) == 0:
            return "spam!"
    except:
        return "not spam"


if __name__ == "__main__":
    tool = language_tool_python.LanguageTool('en-US')
    app.run(debug=True)
