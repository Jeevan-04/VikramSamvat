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

    # Find the div containing the date information
    main_div = soup.find('div', class_='dpPHeaderLeftWrapper')

    if not main_div:
        logging.error("Main div not found")
        return {
            'lines': ["Date not found", "Date not found", "Date not found"]
        }

    # Extract date details
    date_details = main_div.find_all('div', recursive=False)

    if date_details:
        # Get the complete string from the second div which contains the combined date details
        combined_date_string = date_details[1].get_text(strip=True) if len(date_details) > 1 else ""

        # First split: Before "Krishna Paksha" or "Shukla Paksha"
        first_split = combined_date_string.split('Krishna Paksha', 1)
        if len(first_split) == 1:
            first_split = combined_date_string.split('Shukla Paksha', 1)
        first_part = first_split[0].strip() if len(first_split) > 0 else "Data not found"
        second_split = first_split[1].strip() if len(first_split) > 1 else ""

        # Second split: Splitting second part before the number (using regex)
        import re
        match = re.search(r'(\d+)', second_split)
        if match:
            second_part = second_split[:match.start()].strip()
            third_part = second_split[match.start():].strip()
        else:
            second_part = "Data not found"
            third_part = "Data not found"

        # Collect the lines
        date_lines = [first_part, second_part, third_part]
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
