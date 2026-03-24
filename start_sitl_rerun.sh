#!/bin/bash
# Complete startup script for SITL + Rerun visualization

echo "======================================================================"
echo "Betaflight SITL + Rerun.io Launcher"
echo "======================================================================"

# Kill any existing processes
echo ""
echo "🧹 Cleaning up old processes..."
killall betaflight_SITL 2>/dev/null || true
killall rerun 2>/dev/null || true
sleep 1
echo "✓ Cleaned"

# Activate venv
source .venv/bin/activate

# Start SITL
echo ""
echo "🚀 Starting SITL..."
./obj/betaflight_2025.12.0-beta_SITL &
SITL_PID=$!
echo "   SITL PID: $SITL_PID"

# Wait for port
sleep 3

# Start Rerun bridge
echo ""
echo "📊 Starting Rerun bridge..."
python tools/sitl_rerun_bridge.py &
BRIDGE_PID=$!
echo "   Bridge PID: $BRIDGE_PID"

echo ""
echo "======================================================================"
echo "✅ Running! Rerun viewer should open automatically"
echo "======================================================================"
echo ""
echo "📊 To control the drone:"
echo "   python tools/sitl_demo.py"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Wait
wait
