from flask import Flask, request, jsonify, render_template
import logging
import time

app = Flask(__name__)

# Configure loggingggggg
logging.basicConfig(level=logging.DEBUG)

def rod_cutting_brute_force(prices, costs, n, max_length, cuts):
    if max_length == 0:
        return 0

    max_value = float('-inf')
    best_cuts_local = []
    for i in range(1, min(n, max_length) + 1):
        current_cuts = []
        current_value = prices[i-1] - costs[i-1] + rod_cutting_brute_force(prices, costs, n, max_length-i, current_cuts)
        if current_value > max_value:
            max_value = current_value
            best_cuts_local = current_cuts + [i]

    cuts[:] = best_cuts_local
    return max_value if max_value != float('-inf') else 0




def rod_cutting_dp(prices, costs, n, max_length):
    dp = [0] * (max_length + 1)
    cuts = [[] for _ in range(max_length + 1)]

    for i in range(1, max_length + 1):
        for j in range(1, min(i, n) + 1):
            current_value = prices[j-1] - costs[j-1] + dp[i-j]
            if current_value > dp[i]:
                dp[i] = current_value
                cuts[i] = cuts[i-j] + [j]

    return dp[max_length], cuts[max_length]



def parse_input(input_str):
    return list(map(int, input_str.split(',')))

def measure_time(func, *args):
    start_time = time.perf_counter()
    result = func(*args)
    end_time = time.perf_counter()
    return result, end_time - start_time

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        prices_str = request.form['prices']
        costs_str = request.form['costs']
        max_length = int(request.form['max_length'])

        prices = parse_input(prices_str)
        costs = parse_input(costs_str)

        logging.debug(f"Prices: {prices}")
        logging.debug(f"Costs: {costs}")
        logging.debug(f"Max Length: {max_length}")


        n = len(prices)

        cuts = []
        brute_force_start = time.perf_counter()
        brute_force_result = rod_cutting_brute_force(prices, costs, n, max_length, cuts)
        brute_force_end = time.perf_counter()
        bf_cuts = cuts
        bf_time_taken = brute_force_end - brute_force_start

        dp_start = time.perf_counter()
        dp_result, dp_cuts = rod_cutting_dp(prices, costs, n, max_length)
        dp_end = time.perf_counter()
        dp_time_taken = dp_end - dp_start

        logging.debug(f"Brute Force Result: {brute_force_result}")
        logging.debug(f"Brute Force Cuts: {bf_cuts}")
        logging.debug(f"Dynamic Programming Result: {dp_result}")
        logging.debug(f"Dynamic Programming Cuts: {dp_cuts}")

        return jsonify({
            'brute_force_result': brute_force_result,
            'brute_force_cuts': bf_cuts,
            'bf_time_taken': f"{bf_time_taken:.20f} seconds",
            'dp_result': dp_result,
            'dp_cuts': dp_cuts,
            'dp_time_taken': f"{dp_time_taken:.20f} seconds"
        })
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

def main():
    app.run(debug=True)

main()