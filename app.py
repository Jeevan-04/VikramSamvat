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

    # Extract date details excluding the location information
    date_details = main_div.find_all('div', recursive=False)

    if date_details and len(date_details) > 1:
        # Assuming date details are in the second div, as the first div might be location
        combined_date_string = date_details[1].get_text(strip=True)

        # First split: Before "Krishna Paksha" or "Shukla Paksha"
        if "Krishna Paksha" in combined_date_string:
            first_split = combined_date_string.split('Krishna Paksha', 1)
            first_part = first_split[0].strip() + " Krishna Paksha"
            remaining_text = first_split[1].strip()
        elif "Shukla Paksha" in combined_date_string:
            first_split = combined_date_string.split('Shukla Paksha', 1)
            first_part = first_split[0].strip() + " Shukla Paksha"
            remaining_text = first_split[1].strip()
        else:
            first_part = "Data not found"
            remaining_text = ""

        # Second split: Splitting remaining text before the first occurrence of a number
        import re
        match = re.search(r'(\d+)', remaining_text)
        if match:
            second_part = remaining_text[:match.start()].strip()
            third_part = remaining_text[match.start():].strip()
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
