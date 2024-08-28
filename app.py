from flask import Flask, render_template, jsonify
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

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
        part1 = text[:number_index].strip()
        part2 = text[number_index:].strip()
        parts.append(part1)
        parts.append(part2)
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
        return {
            'parts': ["Date not found", "Date not found", "Date not found"]
        }
    
    # Extract all child divs directly inside the main div
    child_divs = main_div.find_all('div', recursive=False)
    
    # Extract text from each div
    texts = [div.get_text(strip=True) for div in child_divs]
    
    # Join all texts to handle cases where text spans across multiple divs
    full_text = " ".join(texts)
    
    # Convert English digits to Devanagari numerals
    full_text = convert_to_devanagari(full_text)
    
    # Split the text into parts based on criteria
    date_parts = split_date_text(full_text)
    
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
    app.run(debug=True)
