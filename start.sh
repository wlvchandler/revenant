#!/bin/bash

set -e

MODS_DIR="modules"
START_SCRIPT="start.py"

cd "$(dirname "$0")"

rebar clean
rebar compile
./start_router.escript

if [ ! -d "$MODS_DIR" ]; then
    echo "Error: Directory $MODS_DIR does not exist."
    exit 1
fi

if [ ! -f "$MODS_DIR/$START_SCRIPT" ]; then
    echo "Error: Python script $START_SCRIPT not found in $MODS_DIR."
    exit 1
fi


echo "Starting services..."
python3 "$MODS_DIR/$START_SCRIPT"
