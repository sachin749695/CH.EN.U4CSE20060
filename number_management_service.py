from flask import Flask, request, jsonify
import requests
import concurrent.futures

app = Flask(__name__)

def fetch_numbers(url):
    try:
        response = requests.get(url, timeout=0.5)  # Set timeout to 500 milliseconds
        if response.status_code == 200:
            data = response.json()
            return set(data['numbers'])  # Convert to a set to keep unique numbers
    except requests.exceptions.RequestException:
        pass  # Ignore timeouts and other network errors
    return set()

@app.route('/numbers', methods=['GET'])
def get_numbers():
    urls = request.args.getlist('url')
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Fetch numbers from multiple URLs concurrently
        results = executor.map(fetch_numbers, urls)
    
    merged_numbers = set()
    for numbers in results:
        merged_numbers.update(numbers)
    
    sorted_numbers = sorted(merged_numbers)
    
    return jsonify({'numbers': sorted_numbers})

if __name__ == '__main__':
    app.run(host='localhost', port=8008)
