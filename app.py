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

    # Find the main container div which holds the date elements
    main_div = soup.find('div', class_='dpPHeaderLeftContent')

    if not main_div:
        logging.error("Main div containing date information not found")
        return {
            'lines': ["Date not found", "Date not found", "Date not found"]
        }

    # Extract the specific div elements
    date_parts = main_div.find_all('div')

    if date_parts and len(date_parts) >= 3:
        # Extract each date detail
        day_month = date_parts[0].get_text(strip=True)
        paksha_tithi = date_parts[1].get_text(strip=True)
        samvat_details = date_parts[2].get_text(strip=True)
        
        # Store extracted details in list
        date_lines = [day_month, paksha_tithi, samvat_details]
    else:
        logging.error("Date parts not found or insufficient data.")
        date_lines = ["Date not found", "Date not found", "Date not found"]

    logging.info(f"Extracted text from specific divs: {date_lines}")

    return {
        'lines': date_lines
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
