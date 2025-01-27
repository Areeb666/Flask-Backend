import os
from flask import Flask, jsonify

app = Flask(__name__)

# Path to the text file where customer details are stored
ORDERS_FILE = "customer_details.txt"

# Ensure the file exists and contains a header
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "w") as file:
        file.write("Name\tAddress\tContact\tRemarks\n")  # Headers

@app.route('/get-orders', methods=['GET'])
def get_orders():
    """
    Endpoint to retrieve all customer orders.
    """
    try:
        with open(ORDERS_FILE, "r") as file:
            lines = file.readlines()

        # Skip the header and process the data
        orders = []
        for line in lines[1:]:  # Skip the header
            try:
                name, address, contact, remarks = line.strip().split("\t")
                orders.append({
                    "name": name,
                    "address": address,
                    "contact": contact,
                    "remarks": remarks
                })
            except ValueError:
                print(f"Skipping malformed line: {line.strip()}")

        return jsonify({"orders": orders}), 200
    except Exception as e:
        print(f"Error while reading orders: {e}")  # Log the error
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Set the port from environment variable, or default to 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
