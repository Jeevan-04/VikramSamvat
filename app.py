from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def get_vikram_samvat_date():
    url = 'https://www.drikpanchang.com/?geoname-id=1275339'
    response = requests.get(url)

    logging.info("Fetched HTML content from the website.")
    logging.info(f"Status Code: {response.status_code}")
    logging.info("HTML Content (first 500 chars):")
    logging.info(response.text[:500])

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div containing the date information
    main_div = soup.find('div', class_='dpPHeaderLeftContent dpFlex')

    if not main_div:
        logging.error("Main div not found")
        return {
            'lines': ["Date not found", "Date not found", "Date not found"]
        }

    # Extract all child divs directly inside the main div
    child_divs = main_div.find_all('div', recursive=False)

    if len(child_divs) < 3:
        logging.error("Expected 3 child divs, but found less.")
        return {
            'lines': ["Date not found", "Date not found", "Date not found"]
        }

    # Extract text from each div
    lines = [div.get_text(strip=True) for div in child_divs]

    logging.info(f"Extracted text from child divs: {lines}")

    return {
        'lines': lines
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
