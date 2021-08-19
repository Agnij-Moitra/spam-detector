from flask import Flask, render_template, request
import pickle

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    message = request.form.get("message")
    result = is_spam(message)
    if request.method == "POST":
        return render_template("check.html", message=result)
    return render_template("index.html")


@app.route('/check/<message>')
def check(message):
    return render_template("check.html")


def is_spam(text):
    with open('model_pickle', "rb") as f:
        imported_model = pickle.load(f)
    result = imported_model.predict([f"{text}"])
    if result[0] == 0:
        return "not spam."
    else:
        return "spam."


if __name__ == "__main__":
    app.run()