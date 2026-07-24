# Test File

## Run the application

```bash
cd final-project
python app.py
```

Then open `http://localhost:5000` in your browser.


This program displays a list of available tables and allows the user to select one.
Once a table is selected the user is prompted to input their name and phone number.
If the table has a seat available the player is seated and if not they are placed in a waiting list.

The program also has a link for the admin to click and log in (the password is 'admin')
When the admin logs in they are able to remove players from the tables and wait list. 
When a player is removed from the table the next player on the waitlist will be moved to
their seat at the table and everyone behind them on the waitlist is moved up in position.
