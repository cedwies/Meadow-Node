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

# Check bitcoin-cli binary
BITCOIN_CLI_PATH="$BITCOIN_DIR/bin/bitcoin-cli"
if [ ! -x "$BITCOIN_CLI_PATH" ]; then
  echo "Error: bitcoin-cli binary not found or not executable at: $BITCOIN_CLI_PATH"
  exit 1
fi

# Stop bitcoind
"$BITCOIN_CLI_PATH" -datadir="$DATADIR" stop

echo "bitcoind stopped via $BITCOIN_CLI_PATH with datadir: $DATADIR"

