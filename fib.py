# Fibonacci application to calculate n-th number in the sequence via a rest api call.
from flask import Flask, request, jsonify


app = Flask(__name__)

# Function definition that takes 1 argument
def fibonacci(n):
    # Error checking and default values
    if n < 0:
        return "Invalid input"
    elif n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        # Init the vars of f0=a and f1=b to 0 and 1
        a, b = 0, 1
        # Running a for loop depending on the nth number provided to the func starting with F(2) until n+1 to make sure it's included
        for _ in range(2, n + 1):
            # the value of b becomes the value of a; the value of b becomes the sum of a+b
            a, b = b, a + b
        return b

# Maps /fib endpoint to the fuction below so when the url gets hit it executes the function
@app.route('/fib', methods=['GET'])

# Defining the function to respond to /fib endpoint
def get_fibonacci():
    # Error handling
    try:
        n = int(request.args.get('n')) # gets and converts to integer n parameter in the url
        if n < 0: 
            return jsonify({"error": "n must be a non-negative integer"}), 400 # error out if n is negative
        result = fibonacci(n) 
        return jsonify({"n": n, "fibonacci": result}) 
    except (TypeError, ValueError): # More error checking
        return jsonify({"error": "Invalid input, please provide an integer"}), 400 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5001, debug=True) # Starts web server binding it to all interfaces on port 5001
