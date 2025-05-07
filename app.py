from flask import Flask, render_template, request, redirect, flash, json
import sqlite3
import datetime
import os

app = Flask(__name__)
app.secret_key = "your_secret_key_here"

# 🔧 Створити БД, якщо її ще нема
if not os.path.exists("database.db"):
    import init_db  # викликає файл init_db.py для створення бази

# Головна сторінка
@app.route("/")
def index():
    return render_template("index.html")

# Сторінка послуг
@app.route("/services")
def services():
    return render_template("services.html")

# Сторінка бронювання
@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        service = request.form["service"]
        date = request.form["date"]
        time = request.form["time"]

        try:
            conn = sqlite3.connect("database.db")
            c = conn.cursor()

            # Перевірка на зайнятість
            c.execute("SELECT * FROM bookings WHERE date = ? AND time = ?", (date, time))
            existing = c.fetchone()

            if existing:
                flash("❌ This date and time is already booked!", "error")
            else:
                c.execute("""
                    INSERT INTO bookings (name, email, phone, service, date, time)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (name, email, phone, service, date, time))
                conn.commit()
                flash("✅ Booking successfully submitted!", "success")

            conn.close()
        except Exception as e:
            flash("❌ Error while saving booking: " + str(e), "error")

        return redirect("/booking")

    return render_template("booking.html")

# Сторінка локації
@app.route("/location")
def location():
    return render_template("location.html")

# Календар бронювань
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
            date_str = row[1]
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
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