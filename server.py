from flask import Flask, request, jsonify
import openpyxl
import os
from flask_cors import CORS  # Add this import

app = Flask(__name__)
CORS(app)  # Enable CORS globally

# Path to the Excel file
EXCEL_FILE = "customer_details.xlsx"

# Create an Excel file with headers if it doesn't exist
if not os.path.exists(EXCEL_FILE):
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Customer Details"
    sheet.append(["Name", "Address", "Contact", "Remarks"])  # Headers
    workbook.save(EXCEL_FILE)

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
        remarks = data.get('remarks')

        # Check for missing required fields
        if not name or not address or not contact:
            return jsonify({"message": "Missing required fields"}), 400

        # Append data to the Excel file
        workbook = openpyxl.load_workbook(EXCEL_FILE)
        sheet = workbook.active
        sheet.append([name, address, contact, remarks])
        workbook.save(EXCEL_FILE)

        return jsonify({"message": "Order placed successfully!"}), 200
    except Exception as e:
        print(f"Error: {e}")  # Log the error
        return jsonify({"message": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
