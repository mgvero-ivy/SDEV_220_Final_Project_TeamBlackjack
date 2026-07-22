from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# Required for storing login information in the Flask session
app.secret_key = "team-blackjack-development-key"

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
    pass #Until finished with the rest of the project
    """if request.method == "POST":
        name = request.form.get("name", "").strip()
        password = request.form.get("password", "").strip()
        phone_number = request.form.get("phone_number", "").strip()
        if not phone_number or not name or not password:
            return render_template("signup.html", error="Name, password, and phone number required.")
        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (name, password, phone_number) VALUES (?, ?, ?)", (email, password, phone_number))
            conn.commit()
            session["user"] = phone_number
            return redirect(url_for("index"))
        except:
            return render_template("signup.html", error="Phone number already exists.")
        finally:
            conn.close()

    return render_template("signup.html")"""

@app.route("/login", methods=["GET", "POST"])
def login():
    pass #Until finished with the rest of the project
    """if request.method == "POST":
        phone_number = request.form.get("phone_number", "").strip()
        password = request.form.get("password", "").strip()

        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE phone_number = ?", (phone_number,))
        row = c.fetchone()
        conn.close()

        if row and (row[0], password):
            session["user"] = phone_number
            return redirect(url_for("index"))
        else:
            return render_template("login.html", error="Invalid credentials.")

    return render_template("login.html")"""

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/admin", methods=["GET", "POST"])
def admin():
    pass #Until finished with the rest of the project
    """if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin.html", error="Incorrect password.")
    return render_template("admin.html")"""

@app.route("/admin/dashboard")
def admin_dashboard():
    pass #temporarilly passing for testing






if __name__ == "__main__":
    app.run(debug=True)
