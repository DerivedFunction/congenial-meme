from flask import Flask, jsonify, request, render_template
from db.database import Database
import sqlite3

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
    users = db.get_all_users_by_mos(bilmos)
    db.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)