from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import subprocess
import os

from meadow_web.extensions import db
from meadow_web.models import User
from meadow_web.config import SCRIPTS_DIR

# Auth blueprint for handling login/register/logout
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # First-user-only registration – once one exists, block more
    if User.query.first() is not None:
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Minimal validation – user has to enter something for both fields
        if not username or not password:
            flash('Please provide both username and password', 'error')
            return redirect(url_for('auth.register'))
        
        # Confirm passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('auth.register'))

        # All good, create user and save to DB
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Execute the create-user.sh script with username and password
        # Note: this gets removed after executing it, sort of like a one time use.
        try:
            script_path = os.path.join(SCRIPTS_DIR, 'create-user.sh')
            subprocess.run([script_path, username, password], check=True)
        except subprocess.CalledProcessError as e:
            flash(f'User created but system setup failed: {str(e)}', 'warning')
        except Exception as e:
            flash(f'User created but system setup failed: {str(e)}', 'warning')
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    # Just render the form on GET
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Already logged in? Off you go to the dashboard
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard'))
    
    # No users yet? Redirect to registration
    user_exists = User.query.first() is not None
    if not user_exists:
        return redirect(url_for('auth.register'))
    
    if request.method == 'POST':
        password = request.form.get('password')

        # We assume single-user mode, so we grab the only one
        user = User.query.first()

        # Validate password and log in
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.dashboard'))
        else:
            flash('Invalid password', 'error')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    # Bye! End session and head back to login
    logout_user()
    return redirect(url_for('auth.login'))
