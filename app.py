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
            'lines': ["Date not found", "Date not found", "Date not found", "Location not found"]
        }

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the div containing the date information
    main_div = soup.find('div', class_='dpPHeaderLeftWrapper')

    if not main_div:
        logging.error("Main div not found")
        return {
            'lines': ["Date not found", "Date not found", "Date not found"]
        }

    # Extract date details
    date_details = main_div.find_all('div', recursive=False)
    
    # Now process each div to split into specific parts
    if date_details:
        # Split the first div into "Day" and "Month"
        day_month = date_details[0].get_text(strip=True).split(',', 1)
        day = day_month[0] if len(day_month) > 0 else "Day not found"
        month = day_month[1] if len(day_month) > 1 else "Month not found"

        # Second div contains "Paksha and Tithi"
        paksha_tithi = date_details[1].get_text(strip=True) if len(date_details) > 1 else "Paksha/Tithi not found"

        # Third div contains "Samvat details"
        samvat_details = date_details[2].get_text(strip=True) if len(date_details) > 2 else "Samvat not found"
    
        date_lines = [day, month, paksha_tithi, samvat_details]
    else:
        date_lines = ["Date not found", "Date not found", "Date not found"]

    logging.info(f"Extracted text from child divs: {date_lines}")

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
