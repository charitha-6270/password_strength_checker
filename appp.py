from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Function to check password strength
def check_password_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 12: score += 1
    if re.search(r'[A-Z]', password): score += 1
    if re.search(r'[a-z]', password): score += 1
    if re.search(r'[0-9]', password): score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password): score += 1

    if re.fullmatch(r'[A-Za-z]+', password) or re.fullmatch(r'[0-9]+', password):
        return {"strength": "Very Weak", "score": 0}

    if score < 3:
        return {"strength": "Weak", "score": score}
    elif score < 5:
        return {"strength": "Moderate", "score": score}
    elif score < 7:
        return {"strength": "Strong", "score": score}
    else:
        return {"strength": "Very Strong", "score": score}

# Route for the index (homepage)
@app.route('/')
def index():
    return render_template('index.html')  # Renders the HTML file from the templates folder

# Route for checking password strength (AJAX)
@app.route('/check-password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get("password", "")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    result = check_password_strength(password)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
