from flask import Flask, render_template, request

app = Flask(__name__)

#Displays the main page with all currently available tables
@app.route("/") 
def index():

    #TO DO this list is temporary and will need to be build with table objects
    tables = [
        {"name": "1/3 NL Holdem", "seats": "7/9", "waiting": 0},
        {"name": "2/5 NL Holdem", "seats": "9/9", "waiting": 3},
        {"name": "5/10 NL Holdem", "seats": "9/9", "waiting": 1},
        {"name": "1/2 PLO", "seats": "6/6", "waiting": 4},
        {"name": "2/5 PLO", "seats": "4/6", "waiting": 0},
        {"name": "1/3 LIMIT Holdem", "seats": "4/9", "waiting": 0}
    ]

    return render_template("index.html", tables=tables)

#this shows the player sigh-up page for the chosen table
@app.route("/join/<path:table_name>", methods=["GET", "POST"])
def join(table_name):
    if request.method == "POST":
        player_name = request.form["player_name"]
        phone_number = request.form["phone_number"]


        #TO DO Save player info, check if selected table has open seat, set table_name to the table number/ID 
        return render_template(
            "confirmation.html",
            table_name=table_name,
            player_name=player_name,
            phone_number=phone_number
        )

    return render_template("join.html", table_name=table_name)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    pass #temporarilly passing for testing


@app.route("/login", methods=["GET", "POST"])
def login():
    pass #temporarilly passing for testing

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    pass #temporarilly passing for testing


@app.route("/admin/dashboard")
def admin_dashboard():
    pass #temporarilly passing for testing






if __name__ == "__main__":
    app.run(debug=True)
