from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/join/<path:table_name>", methods=["GET", "POST"])
def join(table_name):
    if request.method == "POST":
        player_name = request.form["player_name"]
        phone_number = request.form["phone_number"]

        return render_template(
            "confirmation.html",
            table_name=table_name,
            player_name=player_name,
            phone_number=phone_number
        )

    return render_template("join.html", table_name=table_name)


if __name__ == "__main__":
    app.run(debug=True)