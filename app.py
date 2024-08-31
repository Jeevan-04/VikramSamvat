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

    if response.status_code != 200:
        logging.error("Failed to retrieve content from the URL.")
        return {
            'lines': ["Date not found", "Date not found", "Date not found"]
        }

    soup = BeautifulSoup(response.text, 'html.parser')

    # Debugging: Print the HTML content to see the structure
    logging.debug("HTML content fetched: %s", soup.prettify())

    # Find the div containing the date information
    main_div = soup.find('div', class_='dpPHeaderLeftWrapper')
    logging.info("Main div found: %s", main_div)

    if not main_div:
        logging.error("Main div not found")
        return {
            'lines': ["Date not found", "Date not found", "Date not found"]
        }

    # Extract date details
    date_details = main_div.find_all('div', recursive=False)
    logging.info("Date details found: %s", date_details)

    # Extract the relevant details from the first three divs
    if len(date_details) >= 3:
        date_lines = [div.get_text(strip=True) for div in date_details[:3]]
    else:
        date_lines = ["Date not found"] * 3

    # Format the output for better readability
    formatted_date_lines = [
        date_lines[0],
        date_lines[1],
        date_lines[2]
    ]

    logging.info(f"Extracted text from child divs: {formatted_date_lines}")

    return {
        'lines': formatted_date_lines
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
