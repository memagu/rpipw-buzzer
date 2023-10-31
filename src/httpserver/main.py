from flask import Flask, render_template, request

PORT = 1944
ROOT_PATH = "/"
action = "do_nothing"

app = Flask(__name__)


@app.route(ROOT_PATH + "api/get_action")
def get_action() -> str:
    global action

    temp = action
    action = "do_nothing"

    return temp


@app.route(ROOT_PATH,  methods=["GET", "POST"])
def home() -> str:
    global action

    if request.method == "POST":
        action = request.form.get("action")

    return render_template("index.html", action=action)


def main():
    app.run("0.0.0.0", PORT)


if __name__ == "__main__":
    main()
