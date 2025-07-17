from flask import Flask, jsonify, request, render_template, send_file
from io import BytesIO
from tools.doc import edit_word_tables
from db.database import Database
import sqlite3
import json

app = Flask(__name__)
db = Database()

@app.route("/")
def home():
    # Return static/index.html
    return render_template("index.html")

@app.route('/users', methods=['GET'])
def get_all_users():
    db.connect()
    users = db.get_all_roster()
    db.close()
    return jsonify(users)

@app.route('/users/<edipi>', methods=['GET'])
def get_user_by_edipi(edipi):
    db.connect()
    user = db.get_user_by_edipi(edipi)
    db.close()
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def insert_user():
    data = request.get_json()
    db.connect()
    try:
        db.insert_user(
            data['rank'],
            data['firstName'],
            data['lastName'],
            data.get('mi', ''),
            data['edipi'],
            data['dor'],
            data['pmos'],
            data['bilmos'],
            data.get('billet', '')
        )
        db.close()
        return jsonify({"message": "User added successfully"}), 201
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": str(e)}), 400

@app.route('/users/<edipi>', methods=['PUT'])
def update_user(edipi):
    data = request.get_json()
    db.connect()
    try:
        db.update_user(
            data['rank'],
            data['firstName'],
            data['lastName'],
            data.get('mi', ''),
            edipi,
            data['dor'],
            data['pmos'],
            data['bilmos'],
            data.get('billet', '')
        )
        db.close()
        return jsonify({"message": "User updated successfully"})
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": str(e)}), 400

@app.route('/users/<edipi>', methods=['DELETE'])
def delete_user(edipi):
    db.connect()
    db.delete_user(edipi)
    db.close()
    return jsonify({"message": "User deleted successfully"})
@app.route('/users/rank/<rank>', methods=['GET'])
def get_users_by_rank(rank):
    db.connect()
    rank = rank.upper()
    users = db.get_all_roster_by_rank(rank)
    db.close()
    return jsonify(users)
@app.route('/users/mos/<bilmos>', methods=['GET'])
def get_users_by_mos(bilmos):
    db.connect()
    bilmos = str(bilmos)
    users = db.get_all_roster_by_mos(bilmos)
    db.close()
    return jsonify(users)

@app.route('/mos', methods=['GET'])
def get_all_mos_desc():
    db.connect()
    mos_desc = db.get_all_mos_desc()
    db.close()
    return jsonify(mos_desc)

@app.route('/mos/<bilmos>', methods=['GET'])
def get_mos_desc_by_bilmos(bilmos):
    db.connect()
    bilmos = str(bilmos)
    mos_desc = db.get_mos_desc_by_bilmos(bilmos)
    db.close()
    if mos_desc:
        return jsonify(mos_desc)

@app.route('/mos', methods=['POST'])
def insert_mos_desc():
    data = request.get_json()
    db.connect()
    try:
        db.insert_mos_desc(
            data['bilmos'],
            data['desc']
        )
        db.close()
        return jsonify({"message": "MOS description added successfully"}), 201
    except sqlite3.Error as e:
        db.close()

@app.route('/mos/<bilmos>', methods=['PUT'])
def update_mos_desc(bilmos):
    data = request.get_json()
    db.connect()
    bilmos = str(bilmos)
    try:
        db.update_mos_desc(
            bilmos,
            data['desc']
        )
        db.close()
        return jsonify({"message": "MOS description updated successfully"})
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": str(e)}), 400

@app.route('/mos/<bilmos>', methods=['DELETE'])
def delete_mos_desc(bilmos):
    try:
        bilmos = str(bilmos)
        db.connect()
        db.delete_mos_desc(bilmos)
        db.close()
        return jsonify({"message": "MOS description deleted successfully"})
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": str(e)}), 400
    


@app.route('/fill_counseling', methods=['POST'])
def fill_counseling():
    
    # Get JSON data
    json_data = request.get_json()
    
    # Process the document
    doc_bytes, response = edit_word_tables("./static/counseling.docx", json.dumps(json_data))
    if response['status'] == 'error':
        return jsonify(response), 400
    
    return send_file(
        BytesIO(doc_bytes),
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name='filled_counseling.docx'
    )
@app.route('/tables', methods=['GET'])
def get_all_tables():
    try:
        db.connect()
        tables = db.get_all_tables()
        db.close()
        return jsonify(tables), 200
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": str(e)}), 500

@app.route('/query', methods=['POST'])
def run_query():
    try:
        statement = request.get_json()['query']
        db.connect()
        # parse the statement for multiple queries
        queries = statement.split(';')
        results = []
        for query in queries:
            query = query.strip()
            if query:
                result = db.run_query(query)
                results.append(result)
        db.close()
        return jsonify(results), 200
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": str(e)}), 500
@app.route('/import/roster', methods=['POST'])
def import_roster():
    try:
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file provided"}), 400
        # Check if it is an CSV file
        if not file.filename.endswith('.csv'):
            return jsonify({"error": "File is not a CSV"}), 400
        db.connect()
        # Read the CSV file
        import csv
        import io
        csv_file = io.StringIO(file.stream.read().decode('utf-8'))
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            # Check if required fields are present
            required_fields = ['rank', 'firstName', 'lastName', 'edipi', 'dor', 'pmos', 'bilmos']
            for field in required_fields:
                if field not in row or not row[field]:
                    row[field] = ''  # Set default value if not present
            # Check if EDIPI is not already in the database
            existing_user = db.get_user_by_edipi(row['edipi'])
            if existing_user:
                # If it is a duplicate entry (edipi), update it
                db.update_user(
                    row['rank'],
                    row['firstName'],
                    row['lastName'],
                    row.get('mi', ''),
                    row['edipi'],
                    row['dor'],
                    row['pmos'],
                    row['bilmos'],
                    row.get('billet', '')
                )
            else:
                # Insert each row into the database
                db.insert_user(
                    row['rank'],
                    row['firstName'],
                    row['lastName'],
                    row.get('mi', ''),
                    row['edipi'],
                    row['dor'],
                    row['pmos'],
                    row['bilmos'],
                    row.get('billet', '')
                )
        db.close()
        return jsonify({"message": "Roster imported successfully"}), 200
    except sqlite3.Error as e:
        db.close()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)