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

    if date_details and len(date_details) > 1:
        combined_date_string = date_details[1].get_text(strip=True)

        # Check for "Krishna Paksha" or "Shukla Paksha" and split
        if "Krishna Paksha" in combined_date_string:
            split1 = "Krishna Paksha"
        elif "Shukla Paksha" in combined_date_string:
            split1 = "Shukla Paksha"
        else:
            split1 = None

        if split1:
            first_split = combined_date_string.split(split1, 1)
            day_month_part = first_split[0].strip()
            paksha_tithi_part = split1
            remaining_text = first_split[1].strip()
        else:
            logging.error("Paksha not found in the combined date string.")
            return {
                'lines': ["Date not found", "Date not found", "Date not found"]
            }

        # Use regex to find the first number for splitting the remaining text
        import re
        match = re.search(r'(\d+)', remaining_text)
        if match:
            samvat_part = remaining_text[match.start():].strip()
        else:
            logging.error("Number not found in the remaining text for Vikrama Samvata.")
            samvat_part = "Data not found"

        # Collect the date lines
        date_lines = [day_month_part, paksha_tithi_part, samvat_part]
    else:
        logging.error("Date details div not found or empty.")
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
