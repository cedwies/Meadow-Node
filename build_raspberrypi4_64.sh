#!/bin/bash

# Preliminaries: - You have to have buildroot downloaded/cloned.
#                  Please see documentation for more information.
#                - Make sure, this file is executable

# Usage: ./build_raspberrypi4_64.sh /path/to/buildroot/

# Exit on error
set -e

# ---- Argument Check ----
if [ -z "$1" ]; then
    echo "Usage: $0 /path/to/buildroot"
    exit 1
fi

# ---- Resolve Paths ----
BUILDROOT_DIR="$(cd "$1" && pwd)"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

DEFCONFIG_PATH="$REPO_DIR/buildroot_files/board/raspberrypi4_64/raspberrypi4_64_defconfig"
USERS_PATH="$REPO_DIR/buildroot_files/other/users.txt"
OVERLAY_PATH="$REPO_DIR/buildroot_files/overlay"
POST_BUILD_PATH="$REPO_DIR/buildroot_files/board/raspberrypi4_64/post-build.sh"
# POST_IMAGE_PATH="$REPO_DIR/buildroot_files/board/raspberrypi4_64/post-image.sh"

# Update the overlay by including the current meadow_web_src as meadow_web.
echo "Updating meadow_web in overlay folder"
MEADOW_WEB_PATH="$REPO_DIR/buildroot_files/overlay/usr/share/meadow_web"
MEADOW_WEB_SRC_PATH="$REPO_DIR/meadow_web_src"
rm -rf $MEADOW_WEB_PATH
cp -r $MEADOW_WEB_SRC_PATH $MEADOW_WEB_PATH

# ---- Buildroot Config ----
cd "$BUILDROOT_DIR"

echo "Applying defconfig..."
make BR2_DEFCONFIG="$DEFCONFIG_PATH" defconfig

# Update .config with paths relative to this script's repo
echo "Patching .config with correct file paths..."

sed -i "/^BR2_ROOTFS_USERS_TABLES/d" .config
echo "BR2_ROOTFS_USERS_TABLES=\"$USERS_PATH\"" >> .config

sed -i "/^BR2_ROOTFS_OVERLAY/d" .config
echo "BR2_ROOTFS_OVERLAY=\"$OVERLAY_PATH\"" >> .config

sed -i "/^BR2_ROOTFS_POST_BUILD_SCRIPT/d" .config
echo "BR2_ROOTFS_POST_BUILD_SCRIPT=\"$POST_BUILD_PATH\"" >> .config

# Re-run olddefconfig to normalize .config
make olddefconfig

# ---- Build Time ----
echo "Starting Buildroot build..."
echo "Running 'make'..."
make

# Provisional: Remove meadowweb from overlay
echo "Removing meadowweb from overlay folder..."
MEADOW_WEB_PATH="$REPO_DIR/buildroot_files/overlay/usr/share/meadow_web"
rm -rf $MEADOW_WEB_PATH

# ---- Find Final Image ----
IMAGE_PATH="$BUILDROOT_DIR/output/images/sdcard.img"

if [ -f "$IMAGE_PATH" ]; then
    echo ""
    echo "✅ Build complete!"
    echo "Your image can be found at:"
    echo "$IMAGE_PATH"
else
    echo "⚠️ Build completed, but no sdcard image was found at expected path: $IMAGE_PATH"
fi

