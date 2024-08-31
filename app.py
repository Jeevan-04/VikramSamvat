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
    date_parts = main_div.find_all('div', recursive=True)

    if date_parts and len(date_parts) >= 3:
        # Combined string from the second div
        combined_date_string = date_parts[1].get_text(strip=True)
        logging.info(f"Combined date string: {combined_date_string}")

        # Determine the keyword to split by
        if "Krishna Paksha" in combined_date_string:
            paksha_keyword = "Krishna Paksha"
        elif "Shukla Paksha" in combined_date_string:
            paksha_keyword = "Shukla Paksha"
        else:
            paksha_keyword = None

        # Split the string based on the paksha keyword
        if paksha_keyword:
            first_split = combined_date_string.split(paksha_keyword, 1)
            first_part = first_split[0].strip() + f", {paksha_keyword}"
            remaining_text = first_split[1].strip()
        else:
            logging.error("Paksha not found in the combined date string.")
            return {
                'lines': ["Date not found", "Date not found", "Date not found"]
            }

        # Use regex to find the first number in the remaining text
        import re
        match = re.search(r'(\d+)', remaining_text)
        if match:
            second_part = remaining_text[:match.start()].strip()
            third_part = remaining_text[match.start():].strip()
        else:
            logging.error("Number not found in the remaining text for Vikrama Samvata.")
            second_part = "Data not found"
            third_part = "Data not found"

        # Collect the date lines
        date_lines = [first_part, second_part, third_part]
    else:
        logging.error("Date parts not found or insufficient data.")
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
