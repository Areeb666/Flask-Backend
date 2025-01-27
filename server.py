from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Path to the text file where customer details are stored
ORDERS_FILE = os.getenv("ORDERS_FILE", "customer_details.txt")

# Ensure the file exists and contains a header
if not os.path.exists(ORDERS_FILE):
    with open(ORDERS_FILE, "w") as file:
        file.write("Name\tAddress\tContact\tRemarks\n")  # Headers

@app.route('/place-order', methods=['POST'])
def place_order():
    """
    Endpoint to place a new customer order.
    """
    try:
        # Parse JSON data from the request
        data = request.json
        name = data.get("name")
        address = data.get("address")
        contact = data.get("contact")
        remarks = data.get("remarks", "")

        # Validate required fields
        if not name or not address or not contact:
            return jsonify({"message": "Missing required fields"}), 400

        # Append the order to the text file
        with open(ORDERS_FILE, "a") as file:
            file.write(f"{name}\t{address}\t{contact}\t{remarks}\n")

        return jsonify({"message": "Order placed successfully!"}), 200
    except Exception as e:
        app.logger.error(f"Error while placing the order: {e}")  # Log the error
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
                app.logger.error(f"Skipping malformed line: {line.strip()}")

        return jsonify({"orders": orders}), 200
    except Exception as e:
        app.logger.error(f"Error while reading orders: {e}")
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # Set the port from environment variable, or default to 5000
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
