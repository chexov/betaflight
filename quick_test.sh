#!/bin/bash
# Quick test script - run everything manually

set -e

echo "Starting SITL + Rerun Visualization Test"
echo ""

# Activate venv
source .venv/bin/activate

# Start SITL in background
echo "Starting SITL..."
./obj/betaflight_2025.12.0-beta_SITL > /tmp/sitl.log 2>&1 &
SITL_PID=$!
echo "SITL PID: $SITL_PID"
sleep 3

# Test connection
echo "Testing connection..."
python test_sitl_connection.py || { echo "Connection failed!"; kill $SITL_PID; exit 1; }

echo ""
echo "✅ SITL is ready!"
echo ""
echo "Now manually run in another terminal:"
echo "  source .venv/bin/activate"
echo "  python tools/sitl_rerun_bridge.py"
echo ""
echo "SITL is running with PID $SITL_PID"
echo "To stop: kill $SITL_PID"
echo ""
echo "Press Ctrl+C when done"

# Wait
wait $SITL_PID
