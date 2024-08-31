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
