#!/bin/sh

# Exit on unset variables and on errors - strict mode is love, strict mode is life
set -u
set -e

# Add a console on tty1 (so we get an HDMI terminal at boot)
# Works differently depending on whether we're using classic sysvinit or systemd
if [ -e "${TARGET_DIR}/etc/inittab" ]; then
    # For systems using inittab - only add tty1 entry if it's not already there
    grep -qE '^tty1::' "${TARGET_DIR}/etc/inittab" || \
    sed -i '/GENERIC_SERIAL/a\
tty1::respawn:/sbin/getty -L  tty1 0 vt100 # HDMI console' "${TARGET_DIR}/etc/inittab"
elif [ -d "${TARGET_DIR}/etc/systemd" ]; then
    # For systemd-based systems, enable getty on tty1 using the good ol' wants dir
    mkdir -p "${TARGET_DIR}/etc/systemd/system/getty.target.wants"
    ln -sf /lib/systemd/system/getty@.service \
        "${TARGET_DIR}/etc/systemd/system/getty.target.wants/getty@tty1.service"
fi

# Let’s fix perms on init scripts so they actually run and don’t just sit there being useless
echo "[post-build] Setting correct permissions for overlay files..."
chmod +x "${TARGET_DIR}/etc/init.d/S50meadowweb"
chmod +x "${TARGET_DIR}/etc/init.d/S50tor"
chmod +x "${TARGET_DIR}/etc/init.d/S50data_partition"

# Same story here, but for meadow scripts — let’s make sure our Bitcoin stuff can actually execute
chmod +x "${TARGET_DIR}/usr/lib/meadow/scripts/install-bitcoin.sh"
chmod +x "${TARGET_DIR}/usr/lib/meadow/scripts/start-bitcoind.sh"
chmod +x "${TARGET_DIR}/usr/lib/meadow/scripts/stop-bitcoind.sh"
chmod +x "${TARGET_DIR}/usr/lib/meadow/scripts/create-user.sh"

