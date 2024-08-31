from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime, timedelta
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def split_date_text(text):
    # Define the keywords for splitting
    keywords = ['Krishna Paksha', 'Shukla Paksha', 'Chaturdashi', 'Purnima', 'Amavasya']
    parts = []

    # Split the text based on keywords
    for keyword in keywords:
        if keyword in text:
            before_keyword, after_keyword = text.split(keyword, 1)
            parts.append(before_keyword.strip())
            text = keyword + ' ' + after_keyword

    # Find where the number part starts
    match = re.search(r'\d', text)
    if match:
        number_index = match.start()
        parts.append(text[:number_index].strip())
        parts.append(text[number_index:].strip())
    else:
        parts.append(text.strip())

    # Ensure the parts are not empty and return up to three parts
    return (parts + ["Date not found"] * 3)[:3]

def get_vikram_samvat_date():
    url = 'https://www.drikpanchang.com/?geoname-id=1275339'
    response = requests.get(url)

    logging.info("Fetched HTML content from the website.")
    logging.info(f"Status Code: {response.status_code}")
    logging.info("HTML Content (first 500 chars):")
    logging.info(response.text[:500])

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main div that contains the date information
    main_div = soup.find('div', class_='panchang-date')

    if not main_div:
        logging.error("Main div not found")
        return {
            'parts': ["Date not found", "Date not found", "Date not found"]
        }

    # Extract the text directly from the div
    text = main_div.get_text(strip=True)

    logging.info(f"Extracted text from main div: {text}")

    # Split the text into parts based on criteria
    date_parts = split_date_text(text)

    # Calculate the next date
    next_date = datetime.now() + timedelta(days=1)

    logging.info(f"Next Date: {next_date.strftime('%Y-%m-%d %H:%M:%S')}")

    return {
        'parts': date_parts,
        'next_date': next_date.strftime('%Y-%m-%d %H:%M:%S')
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/vikram-samvat-date', methods=['GET'])
def get_vikram_samvat():
    date = get_vikram_samvat_date()
    return jsonify(date)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if no PORT environment variable
    app.run(host="0.0.0.0", port=port, debug=True)
