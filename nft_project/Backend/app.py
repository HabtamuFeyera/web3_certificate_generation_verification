# app.py
from flask import Flask, jsonify

app = Flask(__name__)

# Endpoint to fetch opt-in status
@app.route('/api/opt-in-status', methods=['GET'])
def get_opt_in_status():
    # Implement logic to fetch opt-in status from the database or wherever it's stored
    opt_in_status = 'Approved'  # Replace with actual logic
    return jsonify({'status': opt_in_status})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
