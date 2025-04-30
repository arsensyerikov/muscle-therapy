from flask import Flask, render_template, request, redirect, flash, json
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# Головна
@app.route("/")
def index():
    return render_template("index.html")

# Послуги
@app.route("/services")
def services():
    return render_template("services.html")

# Бронювання
@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        service = request.form["service"]
        date = request.form["date"]
        time = request.form["time"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, email, phone, service, date, time) VALUES (?, ?, ?, ?, ?, ?)",
                  (name, email, phone, service, date, time))
        conn.commit()
        conn.close()

        return redirect("/booking")

    return render_template("booking.html")

# Локація
@app.route("/location")
def location():
    return render_template("location.html")

# Календар
@app.route("/calendar")
def calendar():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, date FROM bookings")
    rows = cursor.fetchall()
    conn.close()

    events = []

    for row in rows:
        try:
            # Якщо дата вже у форматі YYYY-MM-DD (від input[type="date"]) — одразу використовуємо
            date_str = row[1]  # напр. '2025-04-30'
            datetime.datetime.strptime(date_str, "%Y-%m-%d")  # валідація
            events.append({
                "title": f"Booked: {row[0]}",
                "start": date_str,
                "color": "#e67e22"
            })
        except Exception as e:
            print("❌ Skip invalid date:", row, "| Error:", e)

    return render_template("calendar.html", events=json.dumps(events))


# Запуск
if __name__ == "__main__":
    app.run(debug=True)
