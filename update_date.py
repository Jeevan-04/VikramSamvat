from app import get_vikram_samvat_date

def update_date_data():
    # Call the function to get and process the date data
    data = get_vikram_samvat_date()
    print(data)

if __name__ == "__main__":
    update_date_data()
