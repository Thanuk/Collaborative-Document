import os

from flask import Flask, request, jsonify, render_template, redirect, url_for,send_file
from faker import Faker
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import SyncGrant
from werkzeug.utils import secure_filename

app = Flask(__name__)
fake = Faker()


@app.route('/')
def index():
    return render_template('index.html')

# Add your Twilio credentials
@app.route('/token')
def generate_token():
    TWILIO_ACCOUNT_SID = 'AC72e54035f90fec23cead8648f3076b29'
    TWILIO_SYNC_SERVICE_SID = 'ISdc4e04850430d05224bf7bbedece12a0'
    TWILIO_API_KEY = 'SK13c07e8090be1328ff866236b7613e2d'
    TWILIO_API_SECRET = 'r9dLfp0tLXm3IsUJWQI7wIdRawLgRbzZ'

    username = request.args.get('username', fake.user_name())

    # create access token with credentials
    token = AccessToken(TWILIO_ACCOUNT_SID, TWILIO_API_KEY, TWILIO_API_SECRET, identity=username)
    # create a Sync grant and add to token
    sync_grant_access = SyncGrant(TWILIO_SYNC_SERVICE_SID)
    token.add_grant(sync_grant_access)
    return jsonify(identity=username, token=token.to_jwt().decode())

# Write the code here
@app.route('/', methods=['POST'])
def download_text():
    text_from_notepad = request.form["text"]
    with open('workfile.txt', 'w') as f:
        f.write(text_from_notepad)
    
    path_of_file = "workfile.txt"
    return send_file(path_of_file, as_attachment=True)

if __name__ == "__main__":
    app.run(host='localhost', port='5001', debug=True)
