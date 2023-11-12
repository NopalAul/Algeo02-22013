from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the 'uploads' folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_files():
    files = request.files.getlist('files[]')

    for file in files:
        if file.filename == '':
            return jsonify({'error': 'No selected file'})
        
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

    return jsonify({'message': 'Files uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)
