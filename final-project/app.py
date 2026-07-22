from flask import Flask, render_template, request, session, redirect, url_for
from database import load_data, save_data

app = Flask(__name__)

# Required for storing login information in the Flask session
app.secret_key = "team-blackjack-development-key"

# Temporary admin password for local development
ADMIN_PASSWORD = "admin"

def find_table(data, table_name):
    """
    Finds a table by combining its stakes and game type.
    Returns the matching table dictionary or None.
    """

    for table in data["tables"]:
        current_name = f"{table['stakes']} {table['game_type']}"

        if current_name == table_name:
            return table

    return None


#Displays the main page with all currently available tables
# Displays the main page with all currently available tables
@app.route("/")
def index():
    # Load the latest table data from data.txt
    data = load_data()
    tables = data["tables"]

    return render_template("index.html", tables=tables)

# Displays the player signup page for the chosen table
@app.route("/join/<path:table_name>", methods=["GET", "POST"])
def join(table_name):
    # Load the latest saved data
    data = load_data()

    # Find the table selected by the player
    selected_table = find_table(data, table_name)

    if selected_table is None:
        return "Table not found", 404

    if request.method == "POST":
        player_name = request.form.get("player_name", "").strip()
        phone_number = request.form.get("phone_number", "").strip()

        # Make sure both fields were completed
        if not player_name or not phone_number:
            return render_template(
                "join.html",
                table_name=table_name,
                error="Name and phone number are required."
            )

        player = {
            "name": player_name,
            "phone_number": phone_number
        }

        # Seat the player if the table has an open seat
        if len(selected_table["players"]) < selected_table["total_seats"]:
            selected_table["players"].append(player)
            status = "seated"
            waitlist_position = None

        # Otherwise, add the player to the waiting list
        else:
            selected_table["waitlist"].append(player)
            status = "waitlisted"
            waitlist_position = len(selected_table["waitlist"])

        # Save the updated table data to data.txt
        save_data(data)

        return render_template(
            "confirmation.html",
            table_name=table_name,
            player_name=player_name,
            phone_number=phone_number,
            status=status,
            waitlist_position=waitlist_position
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

    # Load the latest table data from data.txt
    data = load_data()
    tables = data["tables"]

    return render_template("admin_dashboard.html", tables=tables)


@app.route(
    "/admin/remove-player/<int:table_id>/<int:player_index>",
    methods=["POST"]
)
def remove_player(table_id, player_index):
    # Only logged-in admins may remove players
    if not session.get("admin"):
        return redirect(url_for("admin"))

    data = load_data()

    # Find the table using its numeric ID
    selected_table = None

    for table in data["tables"]:
        if table["id"] == table_id:
            selected_table = table
            break

    if selected_table is None:
        return "Table not found", 404

    # Make sure the requested player position exists
    if player_index < 0 or player_index >= len(selected_table["players"]):
        return "Player not found", 404

    # Remove the seated player
    selected_table["players"].pop(player_index)

    # Move the first waiting player into the open seat
    if selected_table["waitlist"]:
        next_player = selected_table["waitlist"].pop(0)
        selected_table["players"].append(next_player)

    save_data(data)

    return redirect(url_for("admin_dashboard"))

@app.route(
    "/admin/remove-waiting-player/<int:table_id>/<int:player_index>",
    methods=["POST"]
)
def remove_waiting_player(table_id, player_index):
    # Only logged-in admins may remove waiting players
    if not session.get("admin"):
        return redirect(url_for("admin"))

    data = load_data()

    # Find the selected table
    selected_table = None

    for table in data["tables"]:
        if table["id"] == table_id:
            selected_table = table
            break

    if selected_table is None:
        return "Table not found", 404

    # Make sure the requested waiting player exists
    if (
        player_index < 0
        or player_index >= len(selected_table["waitlist"])
    ):
        return "Waiting player not found", 404

    # Remove the player from the waiting list
    selected_table["waitlist"].pop(player_index)

    save_data(data)

    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
