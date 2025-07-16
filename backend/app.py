from flask import Flask, jsonify, request, render_template, send_file
from io import BytesIO
from tools.doc import edit_word_tables
from db.database import Database
import sqlite3
import json

app = Flask(__name__)
db = Database()

@app.route("/")
def hello_world():
    return "Hello"

@app.route('/users', methods=['GET'])
def get_all_users():
    db.connect()
    users = db.get_all_users()
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
            data['bilmos']
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
            data['bilmos']
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
    users = db.get_all_users_by_rank(rank)
    db.close()
    return jsonify(users)
@app.route('/users/mos/<bilmos>', methods=['GET'])
def get_users_by_mos(bilmos):
    db.connect()
    bilmos = str(bilmos)
    users = db.get_all_users_by_mos(bilmos)
    db.close()
    return jsonify(users)

@app.route('/mosdesc', methods=['GET'])
def get_all_mos_desc():
    db.connect()
    mos_desc = db.get_all_mos_desc()
    db.close()
    return jsonify(mos_desc)

@app.route('/mosdesc/<bilmos>', methods=['GET'])
def get_mos_desc_by_bilmos(bilmos):
    db.connect()
    bilmos = str(bilmos)
    mos_desc = db.get_mos_desc_by_bilmos(bilmos)
    db.close()
    if mos_desc:
        return jsonify(mos_desc)

@app.route('/mosdesc', methods=['POST'])
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

@app.route('/mosdesc/<bilmos>', methods=['PUT'])
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

@app.route('/mosdesc/<bilmos>', methods=['DELETE'])
def delete_mos_desc(bilmos):
    bilmos = str(bilmos)
    db.connect()
    db.delete_mos_desc(bilmos)
    db.close()


@app.route('/fill_counseling', methods=['POST'])
def fill_counseling():
    
    # Get JSON data
    json_data = request.get_json()
    
    # Process the document
    doc_bytes, response = edit_word_tables("./static/counseling.docx", json.dumps(json_data))
    print(response)
    if response['status'] == 'error':
        return jsonify(response), 400
    
    print("Response:", response)
    return send_file(
        BytesIO(doc_bytes),
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        as_attachment=True,
        download_name='filled_counseling.docx'
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)