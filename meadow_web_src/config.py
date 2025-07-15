import os
from pathlib import Path

# Base dir is wherever this config file lives – handy for relative paths later
BASE_DIR = Path(__file__).parent.absolute()

# SQLite setup – storing user data in a local file for now
SQLALCHEMY_DATABASE_URI = f'sqlite:///{BASE_DIR}/users.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disables SQLAlchemy change tracking overhead (we're not using it)

# Secret key for sessions and cookies
# Pulls from env var if set, otherwise uses a very dev-only fallback
SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-key-change-me-in-production')

# Flask app settings – bind to all interfaces so it's reachable from other devices
DEBUG = True  # Should be False in production unless you like chaos
HOST = '0.0.0.0'
PORT = 8080

# Path where all our control/utility scripts live
SCRIPTS_DIR = Path('/usr/lib/meadow/scripts')

# Where we expect Bitcoin to be installed (binaries go here)
BITCOIN_INSTALL_DIR = Path('/opt/bitcoin/')

# Bitcoin will use this dir for its data (wallet, blocks, etc)
BITCOIN_DATA_DIR = Path('/data/bitcoin-data-directory')

# URL to download Bitcoin Core – make sure this matches your architecture
BITCOIN_INSTALL_URL = 'https://bitcoincore.org/bin/bitcoin-core-28.1/bitcoin-28.1-aarch64-linux-gnu.tar.gz'

# Location of the Tor hidden service hostname file
# Used to read the .onion address if we're serving over Tor
TOR_HOSTNAME_PATH = '/var/lib/tor/hidden_service/hostname'
