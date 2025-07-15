#!/bin/sh
# -----------------------------------------------------------------------------
# change.sh  –  creates a user with root privileges (UID 0/GID 0)
# Usage:       ./change.sh <username> <password>
# -----------------------------------------------------------------------------
# • Needs to be run as root.
# • Works even if chpasswd or usermod aren't available (uses fallbacks).
# • Creates /home/<username> with proper permissions.
# -----------------------------------------------------------------------------

set -eu  # bail on error or unset variables

###############################################################################
# 0. Check arguments and ensure we're root
###############################################################################
[ "$(id -u)" -eq 0 ] || { echo "✗ This script must be run as root!" >&2; exit 1; }
[ $# -eq 2 ] || { echo "Usage: $0 <username> <password>" >&2; exit 1; }

USER="$1"
PASS="$2"
HOME_DIR="/home/$USER"

echo "→ Starting creation of user '$USER' with root powers..."

###############################################################################
# 1. Create base directories if needed
###############################################################################
echo "→ Ensuring /home and $HOME_DIR exist..."
[ -d /home ] || mkdir -p /home
[ -d "$HOME_DIR" ] || mkdir -p "$HOME_DIR"

echo "✓ Directories in place."

###############################################################################
# 2. Add user if they don't already exist
###############################################################################
echo "→ Checking if user '$USER' already exists..."
if ! id "$USER" >/dev/null 2>&1; then
    echo "→ User doesn't exist, creating..."
    # Add user with or without home support depending on adduser version
    if adduser -h 2>&1 | grep -q '\-h'; then
        adduser -D -s /bin/sh -h "$HOME_DIR" "$USER"
    else
        # If no -h option (e.g., BusyBox), add and patch manually
        adduser -D -s /bin/sh "$USER"
        sed -i -e "s@^${USER}:[^:]*:[0-9]*:[0-9]*:[^:]*:[^:]*:@${USER}:x:$(id -u "$USER"):$(id -g "$USER")::@" /etc/passwd
    fi
    echo "✓ User '$USER' created."
else
    echo "→ User '$USER' already exists, skipping creation."
fi

###############################################################################
# 3. Set the user's password
###############################################################################
echo "→ Setting password for user '$USER'..."
if command -v chpasswd >/dev/null 2>&1; then
    echo "${USER}:${PASS}" | chpasswd
else
    # Fallback method for BusyBox: passwd needs interactive input
    printf '%s\n%s\n' "$PASS" "$PASS" | passwd "$USER"
fi

echo "✓ Password set."

###############################################################################
# 4. Give the user UID and GID of 0 (aka root powers)
###############################################################################
echo "→ Assigning UID 0 and GID 0 to user '$USER'..."
if command -v usermod >/dev/null 2>&1; then
    usermod -o -u 0 -g 0 "$USER"
else
    # Directly editing /etc/passwd if usermod is missing
    sed -i -e "s@^${USER}:[^:]*:[0-9]*:[0-9]*:@${USER}:x:0:0:@" /etc/passwd
fi

echo "✓ User '$USER' is now effectively root."

###############################################################################
# 5. Set ownership and permissions for home dir
###############################################################################
echo "→ Setting correct permissions on $HOME_DIR..."
chown "$USER":root "$HOME_DIR"
chmod 700 "$HOME_DIR"
echo "✓ Home directory permissions set."

###############################################################################
# 6. Remove setup script if needed
###############################################################################
echo "→ Cleaning up setup script if it exists..."
rm -f /usr/lib/meadow/scripts/create-user.sh || true

###############################################################################
# 7. Done
###############################################################################
echo "✓ All done! User '$USER' now has root privileges."
echo "   → Home:     $HOME_DIR"
echo "   → Login:    ssh ${USER}@<IP>   (Password: $PASS)"

