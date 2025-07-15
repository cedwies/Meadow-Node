from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from meadow_web.bitcoin_utils import (
    is_bitcoin_installed,
    is_bitcoin_running,
    start_bitcoin_node,
    stop_bitcoin_node,
    is_installation_in_progress
)

# Blueprint for anything dashboard-related (UI + API endpoints)
dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    # Renders the main dashboard and passes in the current Bitcoin status
    return render_template(
        'dashboard.html',
        username=current_user.username,
        bitcoin_installed=is_bitcoin_installed(),
        bitcoin_running=is_bitcoin_running(),
        bitcoin_installing=is_installation_in_progress()
    )

@dashboard_bp.route('/api/bitcoin/install', methods=['POST'])
@login_required
def install_bitcoin():
    """API: Kicks off Bitcoin Core installation (runs install script)"""
    from meadow_web.bitcoin_utils import install_bitcoin as install_bitcoin_core

    # Don't allow multiple installs at once – script isn't meant to be parallel-safe
    if is_installation_in_progress():
        return jsonify({
            'success': False,
            'message': "Bitcoin installation already in progress",
            'installed': False,
            'installing': True
        })
    
    success, message = install_bitcoin_core()
    return jsonify({
        'success': success,
        'message': message,
        'installed': success,  # if install worked, then it's installed now
        'installing': is_installation_in_progress()  # might still be in progress if it’s slow
    })

@dashboard_bp.route('/api/bitcoin/status', methods=['GET'])
@login_required
def bitcoin_status():
    """API: Gets live info on whether Bitcoin is installed/running/installing"""
    return jsonify({
        'is_running': is_bitcoin_running(),
        'is_installed': is_bitcoin_installed(),
        'installing': is_installation_in_progress()
    })

@dashboard_bp.route('/api/bitcoin/start', methods=['POST'])
@login_required
def start_bitcoin():
    """API: Starts the Bitcoin node using the shell script"""
    success, message = start_bitcoin_node()
    return jsonify({
        'success': success,
        'message': message,
        'is_running': success  # If it started successfully, it should be running
    })

@dashboard_bp.route('/api/bitcoin/install/status', methods=['GET'])
@login_required
def installation_status():
    """API: Gets current install progress (used for polling)"""
    return jsonify({
        'installing': is_installation_in_progress(),
        'is_installed': is_bitcoin_installed()
    })

@dashboard_bp.route('/api/bitcoin/stop', methods=['POST'])
@login_required
def stop_bitcoin():
    """API: Gracefully stops the Bitcoin node via shell script"""
    success, message = stop_bitcoin_node()
    return jsonify({
        'success': success,
        'message': message,
        'is_running': not success  # If stop worked, it should not be running anymore
    })
