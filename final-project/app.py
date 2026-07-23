from flask import Flask, render_template, request, session, redirect, url_for
from database import load_data, save_data
from models import User, Table, Waitlist




app = Flask(__name__)

# Required for storing login information in the Flask session
app.secret_key = "team-blackjack-development-key"

# Temporary admin password for local development
ADMIN_PASSWORD = "admin"

def find_table(data, table_name):
    """
    Finds a table by its stakes and game type.
    Returns the table dictionary and its list position.
    """

    for index, table_data in enumerate(data["tables"]):
        current_name = (
            f"{table_data['stakes']} "
            f"{table_data['game_type']}"
        )

        if current_name == table_name:
            return table_data, index

    return None, None


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
    selected_table_data, table_index = find_table(data, table_name)

    if selected_table_data is None:
        return "Table not found", 404

    # Convert the saved dictionary into a Table object
    selected_table = Table.from_dict(selected_table_data)

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

        # Create the player as a User object
        player = User(name=player_name, phone_number=phone_number)

        # Convert it to a dictionary before saving it in data.txt
        player_data = player.to_dict()

        # Seat the player if the table has an open seat
        # Let the Table object decide where the player belongs
        status = selected_table.add_player(player_data)

        if status == "waitlisted":
            waitlist_position = len(selected_table.waitlist)
        else:
            waitlist_position = None

        # Replace the original dictionary with the updated table data
        data["tables"][table_index] = selected_table.to_dict()

        save_data(data)

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

    # Convert the saved list into a Waitlist object
    waitlist = Waitlist(selected_table["waitlist"])

    # Make sure the requested waiting player exists
    if player_index < 0 or player_index >= len(waitlist):
        return "Waiting player not found", 404

    # Remove the selected player using the Waitlist class
    waitlist.remove_player(player_index)

    # Convert it back to a regular list before saving
    selected_table["waitlist"] = waitlist.to_list()

    save_data(data)

    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
