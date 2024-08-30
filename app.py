from flask import Flask, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
from bs4 import BeautifulSoup
import re
import os

app = Flask(__name__)

# Dictionary for converting English digits to Devanagari numerals
english_to_devanagari = str.maketrans('0123456789', '०१२३४५६७८९')

date_data = {
    'parts': ["Date not found", "Date not found", "Date not found"]
}

def convert_to_devanagari(text):
    return text.translate(english_to_devanagari)

def split_date_text(text):
    keywords = ['कृष्ण पक्ष', 'शुक्ल पक्ष']
    parts = []
    
    for keyword in keywords:
        if keyword in text:
            before_keyword, after_keyword = text.split(keyword, 1)
            parts.append(before_keyword.strip())
            text = keyword + ' ' + after_keyword
    
    match = re.search(r'\d', text)
    if match:
        number_index = match.start()
        part1 = text[:number_index].strip()
        part2 = text[number_index:].strip()
        parts.append(part1)
        parts.append(part2)
    else:
        parts.append(text.strip())
    
    return (parts + ["Date not found"] * 3)[:3]

def get_vikram_samvat_date():
    url = 'https://www.drikpanchang.com/?lang=hi'
    response = requests.get(url, headers={'Cache-Control': 'no-cache'})
    soup = BeautifulSoup(response.text, 'html.parser')
    
    main_div = soup.find('div', class_='dpPHeaderLeftContent dpFlex')
    
    if not main_div:
        return {
            'parts': ["Date not found", "Date not found", "Date not found"]
        }
    
    # Debug: Print the raw content for inspection
    print("Raw main_div content:", main_div.prettify())

    # Find the specific divs with the date information and remove any empty divs
    child_divs = [div.get_text(strip=True) for div in main_div.find_all('div', recursive=False) if div.get_text(strip=True)]
    print("Filtered texts extracted from child divs:", child_divs)  # Debugging output

    if len(child_divs) >= 3:
        full_text = " ".join(child_divs)
        full_text = convert_to_devanagari(full_text)
        date_parts = split_date_text(full_text)
    else:
        # Handle unexpected structure
        date_parts = ["Date not found", "Date not found", "Date not found"]
    
    return {
        'parts': date_parts
    }

def update_date_data():
    global date_data
    date_data = get_vikram_samvat_date()
    print("Date data updated:", date_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/vikram-samvat-date', methods=['GET'])
def get_vikram_samvat():
    return jsonify(date_data)

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_date_data, trigger="cron", hour=0, minute=0)
    scheduler.start()
    
    update_date_data()  # Initial load
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000 if no PORT environment variable
    app.run(host="0.0.0.0", port=port, debug=True)
