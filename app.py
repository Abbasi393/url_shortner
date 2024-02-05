import sqlite3
import string
import random
from flask import Flask, redirect, request

app = Flask(__name__)
DATABASE_NAME = "url_shortener.db"


# Function to generate a unique shortcode
def generate_shortcode():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))


# Function to create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS urls
                      (shortcode TEXT PRIMARY KEY, long_url TEXT)''')
    conn.commit()
    conn.close()


# Function to store long URL and corresponding shortcode in the database
def store_url(long_url, shortcode):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (shortcode, long_url) VALUES (?, ?)", (shortcode, long_url))
    conn.commit()
    conn.close()


# Function to retrieve long URL from the database based on shortcode
def get_long_url(shortcode):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE shortcode=?", (shortcode,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


# Route to handle shortening of URLs
@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form['long_url']
    shortcode = generate_shortcode()
    store_url(long_url, shortcode)
    return f'Shortened URL: {request.host_url}{shortcode}'


# Route to handle redirection based on shortcode
@app.route('/<shortcode>')
def redirect_to_long_url(shortcode):
    long_url = get_long_url(shortcode)
    if long_url:
        return redirect(long_url)
    else:
        return "Shortcode not found", 404


if __name__ == '__main__':
    create_table()
    app.run(debug=True)
