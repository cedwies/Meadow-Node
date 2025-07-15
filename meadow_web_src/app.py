import os
import sys
from pathlib import Path

# Manually adding the project root to sys.path
# Useful when running scripts from subdirectories – avoids import hell
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import current_user

# Flask app needs to be created *before* we import things that depend on it
app = Flask(__name__)

# Config comes in after the app is made to dodge circular import issues
from meadow_web.config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

# Feed the app its secret keys and DB settings
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Import extensions after app exists – classic Flask sequencing
from meadow_web.extensions import db, login_manager

# Hook up SQLAlchemy and Flask-Login to the app
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # if not logged in, users get sent here

# Model import needs app context (again, circular imports are lurking everywhere)
with app.app_context():
    from meadow_web.models import User

    # Make sure the DB tables actually exist
    db.create_all()

# Same import-sequencing trick: blueprints come in after app is ready
from meadow_web.routes.auth import auth_bp
from meadow_web.routes.dashboard import dashboard_bp

# Plug in the blueprints so Flask knows about our routes
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)

# Needed by Flask-Login to load users from DB sessions
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Makes some Tor-related info globally available in templates
@app.context_processor
def inject_tor_info():
    tor_address = None
    is_tor = False

    # Try to read the onion address from the file (if it exists)
    try:
        with open('/var/lib/tor/hidden_service/hostname', 'r') as f:
            tor_address = f.read().strip()
    except (IOError, FileNotFoundError):
        pass  # No big deal, just means we're not serving over Tor (probably)

    # Now detect if current request came via Tor – multiple heuristics here:
    if request.host and request.host.endswith('.onion'):
        is_tor = True
    elif 'X-Forwarded-Host' in request.headers and request.headers['X-Forwarded-Host'].endswith('.onion'):
        is_tor = True
    elif request.remote_addr and request.remote_addr.endswith('.onion'):  # meh, rare but included
        is_tor = True
    elif request.remote_addr in ('127.0.0.1', '::1') and 'Tor' in request.headers.get('User-Agent', ''):
        is_tor = True

    return {
        'tor_address': tor_address,
        'is_tor': is_tor,
        'connection_type': 'Tor' if is_tor else 'Regular HTTP'
    }

# Default route – send logged-in users to their dashboard, others to login
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    # One-time setup: print a message if there are no users yet
    with app.app_context():
        from meadow_web.models import User
        if not User.query.first():
            print("No users found. Please register the first user at /register")

    # Fire up the Flask server with some sane settings
    from meadow_web.config import HOST, PORT, DEBUG
    app.run(host=HOST, port=PORT, debug=DEBUG, use_reloader=False, threaded=True)
