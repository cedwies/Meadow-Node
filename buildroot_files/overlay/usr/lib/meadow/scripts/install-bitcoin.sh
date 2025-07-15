#!/bin/sh
# Usage: install_bitcoin.sh --url=<download_url> --dest=<install_path> --data_dir_dest=<path_to_data_dir>

set -e

# Initialize variables
DOWNLOAD_URL=""
INSTALL_PATH=""
DATA_DIR_DEST=""

# Parse named arguments
for arg in "$@"; do
  case $arg in
    --url=*)
      DOWNLOAD_URL="${arg#*=}"
      ;;
    --dest=*)
      INSTALL_PATH="${arg#*=}"
      ;;
    --data_dir_dest=*)
      DATA_DIR_DEST="${arg#*=}"
      ;;
    *)
      echo "[error] Unknown argument: $arg"
      echo "Usage: $0 --url=<download_url> --dest=<install_path> --data_dir_dest=<path_to_data_dir>"
      exit 1
      ;;
  esac
done

# Validate arguments
if [ -z "$DOWNLOAD_URL" ] || [ -z "$INSTALL_PATH" ] || [ -z "$DATA_DIR_DEST" ]; then
  echo "[error] All --url, --dest, and --data_dir_dest must be provided"
  echo "Usage: $0 --url=<download_url> --dest=<install_path> --data_dir_dest=<path_to_data_dir>"
  exit 1
fi

echo "[bitcoin-install] Downloading from: $DOWNLOAD_URL"
TMP_DIR="$(mktemp -d)"
cd "$TMP_DIR"

ARCHIVE_NAME="$(basename "$DOWNLOAD_URL")"
TAR_NAME="${ARCHIVE_NAME%.gz}"  # remove .gz extension

wget --no-check-certificate "$DOWNLOAD_URL"

echo "[bitcoin-install] Unpacking..."
gunzip "$ARCHIVE_NAME"
tar -xf "$TAR_NAME"

EXTRACTED_DIR=$(find . -maxdepth 1 -type d -name "bitcoin-*" | head -n 1)

echo "[bitcoin-install] Installing to: $INSTALL_PATH"
mkdir -p "$INSTALL_PATH"
rm -rf "$INSTALL_PATH"/*
mv "$EXTRACTED_DIR"/* "$INSTALL_PATH"

echo "[bitcoin-install] Copying bitcoin.conf to data directory: $DATA_DIR_DEST"
mkdir -p "$DATA_DIR_DEST"
cp /usr/lib/meadow/bitcoin.conf "$DATA_DIR_DEST"

echo "[bitcoin-install] Cleaning up..."
cd /
rm -rf "$TMP_DIR"

echo "[bitcoin-install] Done. Bitcoin installed to: $INSTALL_PATH"

