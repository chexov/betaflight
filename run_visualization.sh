#!/bin/bash
# Simple script to run SITL with Rerun visualization

echo "===================================================="
echo "Starting SITL + Rerun Visualization"
echo "===================================================="
echo ""

# Activate venv
source .venv/bin/activate

# Start SITL
echo "1. Starting SITL..."
./obj/betaflight_2025.12.0-beta_SITL > /tmp/sitl.log 2>&1 &
SITL_PID=$!
sleep 3

# Start Rerun bridge
echo "2. Starting Rerun bridge..."
echo "   (Viewer will open - look for the quadcopter in 3D view!)"
echo ""

python tools/sitl_rerun_bridge.py

# Cleanup on exit
kill $SITL_PID 2>/dev/null
