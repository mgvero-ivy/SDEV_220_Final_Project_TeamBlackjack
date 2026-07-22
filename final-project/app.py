from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

# Required for storing login information in the Flask session
app.secret_key = "team-blackjack-development-key"

# Temporary admin password for local development
ADMIN_PASSWORD = "admin"

# Temporary table data used by both the main page and admin dashboard
# This will later be replaced with data loaded from a file
tables = [
    {
        "id": 1,
        "game_type": "NL Holdem",
        "stakes": "1/3",
        "seats_filled": 7,
        "total_seats": 9,
        "waiting": 0
    },
    {
        "id": 2,
        "game_type": "NL Holdem",
        "stakes": "2/5",
        "seats_filled": 9,
        "total_seats": 9,
        "waiting": 3
    },
    {
        "id": 3,
        "game_type": "NL Holdem",
        "stakes": "5/10",
        "seats_filled": 9,
        "total_seats": 9,
        "waiting": 1
    },
    {
        "id": 4,
        "game_type": "PLO",
        "stakes": "1/2",
        "seats_filled": 6,
        "total_seats": 6,
        "waiting": 4
    },
    {
        "id": 5,
        "game_type": "PLO",
        "stakes": "2/5",
        "seats_filled": 4,
        "total_seats": 6,
        "waiting": 0
    },
    {
        "id": 6,
        "game_type": "LIMIT Holdem",
        "stakes": "1/3",
        "seats_filled": 4,
        "total_seats": 9,
        "waiting": 0
    }
]

#Displays the main page with all currently available tables
@app.route("/") 
def index():
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
    if request.method == "POST":
        # Get the password entered in the form
        password = request.form.get("password", "")

        if password == ADMIN_PASSWORD:
            # Remember that the admin successfully logged in
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))

        # Reload the page with an error message
        return render_template(
            "admin.html",
            error="Incorrect password."
        )

    return render_template("admin.html")
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
    # Prevent users from opening the dashboard without logging in
    if not session.get("admin"):
        return redirect(url_for("admin"))

    return render_template("admin_dashboard.html", tables=tables)






if __name__ == "__main__":
    app.run(debug=True)
