from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import firebase_admin
from firebase_admin import credentials, auth, firestore
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

# Initialize Firebase Admin SDK
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Decorators for session management
def login_required(f):
    def wrap(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

def password_change_required(f):
    def wrap(*args, **kwargs):
        if 'user' in session and not session.get('password_changed', False):
            return redirect(url_for('change_password'))
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

# Root route to redirect to /login
@app.route('/')
def index():
    return redirect(url_for('login'))

# Routes
@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/tasks')
@login_required
@password_change_required
def tasks():
    return "Tasks page (to be implemented)"

@app.route('/messages')
@login_required
@password_change_required
def messages():
    return "Messages page (to be implemented)"

@app.route('/checklists')
@login_required
@password_change_required
def checklists():
    return "Checklists page (to be implemented)"

@app.route('/locker-keys')
@login_required
@password_change_required
def locker_keys():
    return "Locker Keys page (to be implemented)"

@app.route('/church-meetings')
@login_required
@password_change_required
def church_meetings():
    return "Church Meetings page (to be implemented)"

@app.route('/moves')
@login_required
@password_change_required
def moves():
    return "Moves page (to be implemented)"

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'GET':
        return render_template('change_password.html')

    # Handle POST request to update password_changed status
    if request.method == 'POST':
        try:
            # Verify the ID token to ensure the request is authenticated
            token = request.json.get('idToken')
            if not token:
                logging.error("No token provided in change-password request")
                return jsonify({"error": "No token provided"}), 400

            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            email = decoded_token['email']
            logging.debug(f"Change password request for user: {email} (UID: {uid})")

            # Update password_changed to True in Firestore
            user_ref = db.collection('Staff').document(uid)
            user_ref.update({
                'password_changed': True
            })
            logging.debug(f"Updated password_changed to True for user: {email}")

            # Update the session to reflect the new password_changed status
            session['password_changed'] = True
            logging.debug(f"Session updated with password_changed: True for user: {email}")

            return jsonify({"message": "Password changed successfully"}), 200

        except Exception as e:
            logging.error(f"Change password failed for request: {str(e)}")
            return jsonify({"error": "Failed to change password"}), 400

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))
    
@app.route('/test')
def test():
    return jsonify({"message": "Backend is running"})

# API Routes
@app.route('/api/session', methods=['POST'])
def api_session():
    # Log the incoming request
    logging.debug(f"Incoming session request: {request.json}")

    token = request.json.get('idToken')
    if not token:
        logging.error("No token provided in request")
        return jsonify({"error": "No token provided"}), 400

    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']
        email = decoded_token['email']
        logging.debug(f"Received token for user: {email} (UID: {uid})")

        # Check if user exists in Firestore Staff collection
        user_ref = db.collection('Staff').document(uid)
        user_doc = user_ref.get()
        if not user_doc.exists:
            logging.debug(f"User {email} not found in Firestore, creating new entry")
            # Create a new user entry in Firestore if it doesn't exist
            user_ref.set({
                'email': email,
                'password_changed': False
            })
            password_changed = False
        else:
            password_changed = user_doc.to_dict().get('password_changed', False)
            logging.debug(f"User {email} found in Firestore, password_changed: {password_changed}")

        # Store user info in session
        session['user'] = {
            'uid': uid,
            'email': email
        }
        session['password_changed'] = password_changed
        logging.debug(f"Session updated: {session}")

        # Determine redirect based on password change status
        redirect_url = url_for('change_password') if not password_changed else url_for('tasks')
        logging.debug(f"Redirecting user {email} to {redirect_url}")
        return jsonify({"message": "Login successful", "redirect": redirect_url}), 200

    except Exception as e:
        logging.error(f"Token verification failed for request: {str(e)}")
        return jsonify({"error": "Invalid token"}), 401

@app.route('/api/tasks', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
@password_change_required
def api_tasks():
    return jsonify({"message": "Tasks API (to be implemented)"})

@app.route('/api/messages', methods=['GET', 'POST'])
@login_required
@password_change_required
def api_messages():
    return jsonify({"message": "Messages API (to be implemented)"})

@app.route('/api/checklists', methods=['GET'])
@login_required
@password_change_required
def api_checklists():
    return jsonify({"message": "Checklists API (to be implemented)"})

@app.route('/api/locker-keys', methods=['GET'])
@login_required
@password_change_required
def api_locker_keys():
    return jsonify({"message": "Locker Keys API (to be implemented)"})

@app.route('/api/church-meetings', methods=['GET'])
@login_required
@password_change_required
def api_church_meetings():
    return jsonify({"message": "Church Meetings API (to be implemented)"})

@app.route('/api/moves', methods=['GET'])
@login_required
@password_change_required
def api_moves():
    return jsonify({"message": "Moves API (to be implemented)"})

if __name__ == '__main__':
    app.run(debug=True)