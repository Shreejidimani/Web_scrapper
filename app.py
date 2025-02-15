import os
import csv
import sqlite3
from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pytz

# Import database instance
from database import db, create_tables, ScrapeHistory, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scraper.db'
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize db with the app
db.init_app(app)
create_tables(app) 

# Ensure static folder for CSV files exists
CSV_FOLDER = os.path.join(os.getcwd(), 'static', 'scraped_files')
if not os.path.exists(CSV_FOLDER):
    os.makedirs(CSV_FOLDER)

def init_db():
    """Initialize the database with user authentication table."""
    conn = sqlite3.connect("scraper.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.context_processor
def inject_user():
    return {"current_user": session.get("username")}

@app.route('/')
def home():
    return render_template("home.html")  # Ensure home.html exists in the templates folder

@app.route('/dashboard')
def dashboard():
    if "username" not in session:  # Check if user is logged in
        return redirect(url_for("login"))
    history = ScrapeHistory.query.order_by(ScrapeHistory.date_scraped.desc()).all()
    return render_template("dashboard.html", history=history)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("scraper.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            return "Username already exists. Try another."
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("scraper.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            error = "Invalid username or password. Please try again."
    
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("home"))

def scrape_website(url):
    """Scrapes the website and returns the parsed BeautifulSoup object."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    else:
        return None

from datetime import datetime
import pytz

@app.route('/scrape', methods=['POST'])
def scrape():
    url = request.form['url']
    data_type = request.form['data_type']

    # Call the scraper function
    soup = scrape_website(url)  
    if not soup:
        flash("Failed to retrieve content. Check the URL.", "danger")
        return redirect(url_for('dashboard'))
    
    scraped_data = []

    if data_type == "products":
        products = soup.find_all('div', class_="product")  # Update class name based on website
        
        for product in products:
            name = product.find('h2', class_="product-title")
            price = product.find('span', class_="product-price")
            link = product.find('a', href=True)

            scraped_data.append({
                "Product Name": name.get_text(strip=True) if name else "N/A",
                "Price": price.get_text(strip=True) if price else "N/A",
                "Link": link['href'] if link else "N/A"
            })

    elif data_type == "headlines":
        elements = soup.find_all(['h1', 'h2', 'h3'])
        scraped_data = [{"Headline": e.get_text(strip=True)} for e in elements]

    elif data_type == "job_listings":
        jobs = soup.find_all('div', class_="job-card")  # Update class based on job website
        scraped_data = [{"Job Title": job.get_text(strip=True)} for job in jobs]

    elif data_type == "full_text":
        scraped_data = [{"Text": soup.get_text()}]

    elif data_type == "custom":
        tag = request.form.get("tag", "").strip()
        attribute = request.form.get("attribute", "").strip()
        value = request.form.get("value", "").strip()
        
        if tag:
            if attribute and value:
                elements = soup.find_all(tag, {attribute: value})
            else:
                elements = soup.find_all(tag)
            
            scraped_data = [{tag: e.get_text(strip=True)} for e in elements]

    # **🌟 Correct the Time Here 🌟**
    tz = pytz.timezone("Asia/Kolkata")  # Change to your timezone
    timestamp = datetime.now(tz)  # ✅ Store as datetime object

    # Save Data to CSV
    if scraped_data:
        filename = f"scraped_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
        file_path = os.path.join(CSV_FOLDER, filename)

        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(scraped_data[0].keys())  # Headers
            for row in scraped_data:
                writer.writerow(row.values())

        # Save to database with corrected timestamp
        new_entry = ScrapeHistory(url=url, data_type=data_type, filename=filename, date_scraped=timestamp)  # ✅ Use datetime object
        db.session.add(new_entry)
        db.session.commit()

    flash("Scraping completed successfully!", "success")
    return redirect(url_for('dashboard'))


@app.route('/download/<file_id>')
def download(file_id):
    entry = ScrapeHistory.query.get(file_id)
    if entry and entry.filename:
        return send_from_directory(CSV_FOLDER, entry.filename, as_attachment=True)
    flash("File not found!", "danger")
    return redirect(url_for('dashboard'))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    ScrapeHistory.query.delete()
    db.session.commit()
    flash("Scraping history cleared!", "info")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure database is created
    app.run(debug=True)
