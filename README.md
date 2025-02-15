# Web Scraper with Flask

This is a simple web scraping application built using **Flask**, **BeautifulSoup**, and **SQLite**. It allows users to scrape data from web pages, store the history in a database, and download the scraped data as a CSV file.

## Features
- User authentication (Register/Login)
- Scrape data such as **headlines, job listings, full text, and custom HTML elements**
- Save scraping history to an SQLite database
- Download scraped data as a CSV file
- Clear history option
- Flask-based web interface with Bootstrap for styling

## Technologies Used
- **Python** (Flask, BeautifulSoup, requests, pandas)
- **HTML/CSS** (Bootstrap for styling)
- **SQLite** (Database for storing scraping history)
- **JavaScript** (For UI enhancements)

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Web-Scraper-Flask.git
cd Web-Scraper-Flask
```

### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

### 5. Access the App
Go to **http://127.0.0.1:5000/** in your browser.

## How to Use
1. **Register/Login** to access the dashboard.
2. Enter a **URL** and select the type of data you want to scrape.
3. Click **Scrape** to extract data.
4. View scraping history and **download CSV files**.
5. Click **Clear History** to remove all records.

## Troubleshooting
- If the product details or job listings are not saving, check if the HTML structure has changed.
- Make sure the website allows scraping. Some sites block bots.
- Use `print(soup.prettify())` to inspect the HTML and adjust selectors.

## To-Do List
- Improve data extraction for product details.
- Add more scraping options.
- Implement better error handling.

## License
This project is open-source under the **MIT License**.

## Contributing
Feel free to fork this repository and submit pull requests!

---
**Author:** Your Name  
**GitHub:** [YourUsername](https://github.com/yourusername)

