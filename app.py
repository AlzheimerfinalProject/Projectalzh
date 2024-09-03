from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import bcrypt
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# MongoDB
client = MongoClient('mongodb+srv://mukund7521:21001001300@cluster0.soyzj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['Alzh_detection']
collection = db['users']

def add_user(name, username, password, email):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    user_data = {
        "name": name,
        "username": username,
        "password": hashed_password,
        "email": email
    }
    collection.insert_one(user_data)
    return "User added successfully"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    try:
        message = add_user(name, username, password, email)
        return jsonify({'message': message, 'redirect': url_for('alzheimer_detection')}), 200
    except Exception as e:
        return jsonify({'message': 'Error adding user', 'error': str(e)}), 500

@app.route('/alzheimer')
def alzheimer_detection():
    return render_template('alzheimer.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if file:
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join('uploads', filename) 
            file.save(file_path)
            return jsonify({'message': f'File uploaded successfully: {filename}'}), 200
        except Exception as e:
            return jsonify({'message': 'Error processing file', 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
