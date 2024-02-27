import requests
import time

def get_data_from_database():
    api_url = 'https://free-api-ryfe.onrender.com/washers'
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            # Assuming the API returns JSON, you can process it here
            data = response.json()
            print("Data retrieved successfully:", data)
        else:
            print("Failed to retrieve data. Status code:", response.status_code)
    except requests.exceptions.RequestException as e:
        print("Request failed:", e)

if __name__ == "__main__":
    while True:
        get_data_from_database()
        # Wait for 5 minutes (300 seconds) before making the next request
        time.sleep(300)