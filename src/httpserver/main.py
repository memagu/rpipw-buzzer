from flask import Flask, render_template, request

PORT = 1944
ROOT_PATH = "/"
action = "do_nothing"

app = Flask(__name__)


@app.route(ROOT_PATH + "actions/", methods=["GET", "POST"])
def actions() -> str:
    global action

    if request.method == "POST":
        action = request.form.get("action")

    return render_template("index.html", action=action)


@app.route(ROOT_PATH)
def home() -> str:
    global action

    temp = action
    action = "do_nothing"

    return temp


def main():
    app.run("0.0.0.0", PORT)


if __name__ == "__main__":
    main()
