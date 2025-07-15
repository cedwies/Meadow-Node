#!/bin/sh

# Initialize variables
DATADIR=""
BITCOIN_DIR=""

# Parse arguments
for arg in "$@"; do
  case $arg in
    -datadir=*)
      DATADIR="${arg#*=}"
      ;;
    -bitcoin_dir=*)
      BITCOIN_DIR="${arg#*=}"
      ;;
    *)
      echo "Unknown argument: $arg"
      echo "Usage: $0 -datadir=<path> -bitcoin_dir=<path>"
      exit 1
      ;;
  esac
done

# Validate arguments
if [ -z "$DATADIR" ] || [ -z "$BITCOIN_DIR" ]; then
  echo "Error: both -datadir and -bitcoin_dir must be specified"
  echo "Usage: $0 -datadir=<path> -bitcoin_dir=<path>"
  exit 1
fi

# Check datadir
if [ ! -d "$DATADIR" ]; then
  echo "Error: datadir '$DATADIR' does not exist"
  exit 1
fi

# Check bitcoind binary
BITCOIND_PATH="$BITCOIN_DIR/bin/bitcoind"
if [ ! -x "$BITCOIND_PATH" ]; then
  echo "Error: bitcoind binary not found or not executable at: $BITCOIND_PATH"
  exit 1
fi

# Start bitcoind
"$BITCOIND_PATH" -datadir="$DATADIR" -daemon

echo "bitcoind started from $BITCOIND_PATH with datadir: $DATADIR"

