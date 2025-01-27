import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Path to the text file where customer details will be stored
ORDERS_FILE = "customer_details.txt"

# Create the file if it doesn't exist
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "w") as file:
        file.write("Name\tAddress\tContact\tRemarks\n")  # Headers

@app.route('/place-order', methods=['POST'])
def place_order():
    """
    Endpoint to handle customer details submission.
    """
    try:
        # Parse incoming JSON data
        data = request.json
        name = data.get('name')
        address = data.get('address')
        contact = data.get('contact')
        remarks = data.get('remarks', "")

        # Check for missing required fields
        if not name or not address or not contact:
            return jsonify({"message": "Missing required fields"}), 400

        # Append data to the text file
        with open(ORDERS_FILE, "a") as file:
            file.write(f"{name}\t{address}\t{contact}\t{remarks}\n")

        return jsonify({"message": "Order placed successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

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
        for line in lines[1:]:
            name, address, contact, remarks = line.strip().split("\t")
            orders.append({
                "name": name,
                "address": address,
                "contact": contact,
                "remarks": remarks
            })

        return jsonify({"orders": orders}), 200
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Set the port from environment variable, or default to 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
