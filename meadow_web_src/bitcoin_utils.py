import os
import subprocess
import logging
import time
from pathlib import Path
from typing import Tuple, Optional
from meadow_web.config import BITCOIN_INSTALL_DIR, BITCOIN_DATA_DIR, SCRIPTS_DIR, BITCOIN_INSTALL_URL

logger = logging.getLogger(__name__)

def is_bitcoin_installed() -> bool:
    # Just checks if bitcoind binary is sitting where we expect it
    bitcoind_path = BITCOIN_INSTALL_DIR / 'bin' / 'bitcoind'
    return bitcoind_path.exists() and bitcoind_path.is_file()

def is_installation_in_progress() -> bool:
    # This checks if a Bitcoin install is already happening, using a lock file
    lock_file = Path("/tmp/bitcoin_install.lock")
    
    if lock_file.exists():
        try:
            # Check if the installer process is really running
            result = subprocess.run(
                ['pgrep', '-f', 'install-bitcoin.sh'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            process_running = result.returncode == 0 and bool(result.stdout.strip())

            if not process_running:
                # Stale lock file – nuke it
                try:
                    lock_file.unlink()
                    logger.info("Removed stale lock file as installation process is not running")
                    return False
                except Exception as e:
                    logger.error(f"Failed to remove stale lock file: {e}")
                    # Still mark it as 'in progress' to play it safe
                    return True
            return True
        except Exception as e:
            logger.error(f"Error checking installation process: {str(e)}")
            return True  # better safe than sorry
    return False

def mark_installation_started() -> None:
    # Drop a lock file to say "hands off, I'm installing Bitcoin"
    try:
        with open("/tmp/bitcoin_install.lock", 'w') as f:
            f.write(str(time.time()))
        logger.info("Marked Bitcoin installation as started")
    except Exception as e:
        logger.error(f"Failed to mark installation as started: {str(e)}")

def mark_installation_completed() -> None:
    # Remove the lock file to show we're done installing
    try:
        lock_file = Path("/tmp/bitcoin_install.lock")
        if lock_file.exists():
            lock_file.unlink()
            logger.info("Marked Bitcoin installation as completed")
    except Exception as e:
        logger.error(f"Failed to mark installation as completed: {str(e)}")

def is_bitcoin_running() -> bool:
    # Looks for the 'bitcoind' process in the system process list
    try:
        result = subprocess.run(
            ['ps', 'aux'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Failed to get process list: {result.stderr}")
            return False

        for line in result.stdout.splitlines():
            if 'bitcoind' in line and not 'grep' in line:
                logger.debug(f"Found bitcoind process: {line.strip()}")
                return True

        logger.debug("No bitcoind process found")
        return False
    except Exception as e:
        logger.error(f"Error checking if Bitcoin is running: {str(e)}")
        return False

def stop_bitcoin_node() -> Tuple[bool, str]:
    # Gracefully stops the node using a script – no 'kill -9' brutality
    script_path = SCRIPTS_DIR / 'stop-bitcoind.sh'

    if not script_path.exists() or not os.access(script_path, os.X_OK):
        return False, "Stop script missing or not executable"

    try:
        if not is_bitcoin_running():
            return True, "Bitcoin node is not running"

        cmd = [
            str(script_path),
            f"-datadir={BITCOIN_DATA_DIR}",
            f"-bitcoin_dir={BITCOIN_INSTALL_DIR}"
        ]

        logger.info(f"Stopping Bitcoin node with command: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=60
        )

        if result.stdout:
            logger.info(f"Stop script stdout: {result.stdout}")
        if result.stderr:
            logger.error(f"Stop script stderr: {result.stderr}")

        # Wait and confirm it really shut down
        for _ in range(30):  # check every 2 seconds, for 1 minute
            if not is_bitcoin_running():
                logger.info("Bitcoin node stopped successfully")
                return True, "Bitcoin node stopped successfully"
            time.sleep(2)

        return False, "Failed to stop bitcoind within timeout (still running)"
    except Exception as e:
        error_msg = f"Error stopping Bitcoin node: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg

def start_bitcoin_node() -> Tuple[bool, str]:
    # Fires up the node using the designated shell script
    script_path = SCRIPTS_DIR / 'start-bitcoind.sh'

    if not script_path.exists() or not os.access(script_path, os.X_OK):
        return False, "Start script missing or not executable"

    try:
        cmd = [
            str(script_path),
            f"-datadir={BITCOIN_DATA_DIR}",
            f"-bitcoin_dir={BITCOIN_INSTALL_DIR}"
        ]

        logger.info(f"Starting Bitcoin node with command: {' '.join(cmd)}")

        # Launch script in background so we don’t block
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True
        )

        if process.poll() is None:
            logger.info("Bitcoin node started successfully")
            return True, "Bitcoin node started successfully"
        else:
            _, stderr = process.communicate()
            error_msg = f"Failed to start Bitcoin node: {stderr}"
            logger.error(error_msg)
            return False, error_msg

    except Exception as e:
        error_msg = f"Unexpected error while starting Bitcoin node: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg

def install_bitcoin() -> Tuple[bool, str]:
    # Runs the full installer script with all required args
    script_path = SCRIPTS_DIR / 'install-bitcoin.sh'

    if not script_path.exists():
        error_msg = f"Installation script not found at {script_path}"
        logger.error(error_msg)
        return False, error_msg

    if not script_path.is_file():
        error_msg = f"Installation path is not a file: {script_path}"
        logger.error(error_msg)
        return False, error_msg

    if not os.access(script_path, os.X_OK):
        error_msg = f"Installation script is not executable: {script_path}"
        logger.error(error_msg)
        return False, error_msg

    try:
        mark_installation_started()

        # Ensure the data dir exists before we proceed
        logger.info(f"Ensuring data directory exists: {BITCOIN_DATA_DIR}")
        BITCOIN_DATA_DIR.mkdir(parents=True, exist_ok=True)

        cmd = [
            str(script_path),
            f"--url={BITCOIN_INSTALL_URL}",
            f"--dest={BITCOIN_INSTALL_DIR}",
            f"--data_dir_dest={BITCOIN_DATA_DIR}"
        ]

        logger.info(f"Executing installation command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=1200  # 20 mins max
        )

        mark_installation_completed()

        logger.info(f"Installation stdout: {result.stdout}")
        if result.stderr:
            logger.error(f"Installation stderr: {result.stderr}")

        if result.returncode == 0:
            success_msg = f"Bitcoin installed successfully to {BITCOIN_INSTALL_DIR}"
            logger.info(success_msg)
            return True, success_msg
        else:
            error_msg = f"Installation failed with return code {result.returncode}. Error: {result.stderr or 'No error output'}"
            logger.error(error_msg)
            return False, error_msg

    except subprocess.TimeoutExpired:
        # Don't clear the lock here – the script might still be working
        error_msg = "Installation timed out after 20 minutes but may still be running in background"
        logger.error(error_msg)
        return False, error_msg
    except Exception as e:
        # Clean up the lock in all other failure cases
        mark_installation_completed()
        error_msg = f"Unexpected error during installation: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return False, error_msg
