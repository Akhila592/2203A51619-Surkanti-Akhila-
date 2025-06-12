import os
import requests
import time
from flask import Flask, jsonify

app = Flask(__name__)

# Configuration
WINDOW_SIZE = 10
THIRD_PARTY_API_BASE_URL = "http://20.244.56.144/evaluation-service"

# In-memory store for numbers
number_window = []

# Map number IDs to API endpoints
API_ENDPOINTS = {
    "p": f"{THIRD_PARTY_API_BASE_URL}/primes",
    "f": f"{THIRD_PARTY_API_BASE_URL}/fibo",
    "e": f"{THIRD_PARTY_API_BASE_URL}/even",
    "r": f"{THIRD_PARTY_API_BASE_URL}/rand",
}

@app.route("/numbers/<string:numberid>", methods=["GET"])
def get_numbers(numberid):
    if numberid not in API_ENDPOINTS:
        return jsonify({"error": "Invalid number ID"}), 400

    window_prev_state = list(number_window)
    
    # Fetch numbers from third-party server
    new_numbers = fetch_numbers_from_third_party(API_ENDPOINTS[numberid])
    
    if new_numbers is not None:
        update_number_window(new_numbers)

    # Calculate average
    avg = sum(number_window) / len(number_window) if number_window else 0.00

    return jsonify({
        "windowPrevState": window_prev_state,
        "windowCurrState": list(number_window),
        "numbers": new_numbers if new_numbers is not None else [],
        "avg": round(avg, 2)
    })

def fetch_numbers_from_third_party(url):
    try:
        start_time = time.time()
        response = requests.get(url, timeout=0.45)  # Timeout less than 500ms
        end_time = time.time()

        if response.status_code == 200 and (end_time - start_time) * 1000 <= 500:
            data = response.json()
            return data.get("numbers", [])
        else:
            app.logger.error(f"Failed to fetch data from {url}: Status {response.status_code}, Time: {(end_time - start_time) * 1000}ms")
            return None
    except requests.exceptions.Timeout:
        app.logger.error(f"Timeout when fetching data from {url}")
        return None
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Request error when fetching data from {url}: {e}")
        return None

def update_number_window(new_numbers):
    global number_window
    
    # Add unique numbers, ignore duplicates
    for num in new_numbers:
        if num not in number_window:
            number_window.append(num)
            
    # Maintain window size
    while len(number_window) > WINDOW_SIZE:
        number_window.pop(0) # Remove oldest number

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9876, debug=True) 