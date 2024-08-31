from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import re
import os
from datetime import datetime
import pytz
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Dictionary for converting English digits to Devanagari numerals
english_to_devanagari = str.maketrans('0123456789', '०१२३४५६७८९')

def convert_to_devanagari(text):
    return text.translate(english_to_devanagari)

def split_date_text(text):
    # Define the keywords and numbers for splitting
    keywords = ['कृष्ण पक्ष', 'शुक्ल पक्ष']
    parts = []

    # Split the text based on keywords and numbers
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
    url = 'https://www.drikpanchang.com/?lang=hi'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the main div that contains the date information
    main_div = soup.find('div', class_='dpPHeaderLeftContent dpFlex')

    if not main_div:
        logging.error("Main div not found")
        return {
            'parts': ["Date not found", "Date not found", "Date not found"]
        }

    # Extract all child divs directly inside the main div
    child_divs = main_div.find_all('div', recursive=False)

    if not child_divs:
        logging.error("No child divs found")
        return {
            'parts': ["Date not found", "Date not found", "Date not found"]
        }

    # Extract text from each div
    texts = [div.get_text(strip=True) for div in child_divs]

    # Join all texts to handle cases where text spans across multiple divs
    full_text = " ".join(texts)

    # Convert English digits to Devanagari numerals
    full_text = convert_to_devanagari(full_text)

    # Split the text into parts based on criteria
    date_parts = split_date_text(full_text)

    # Handle time zone adjustment
    local_tz = pytz.timezone('Asia/Kolkata')  # IST (UTC+5:30)
    now = datetime.now(local_tz)
    utc_now = now.astimezone(pytz.utc)

    logging.info(f"Current Time (IST): {now.strftime('%Y-%m-%d %H:%M:%S')}")
    logging.info(f"Current Time (UTC): {utc_now.strftime('%Y-%m-%d %H:%M:%S')}")

    return {
        'parts': date_parts
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
