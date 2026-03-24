#!/usr/bin/env python3
"""Auto demo - no user input needed"""
import sys
sys.path.insert(0, 'tools')
from sitl_rerun_bridge import MSPClient
import time

print("🚁 Auto Demo Starting...")
msp = MSPClient()
if not msp.connect():
    sys.exit(1)

print("✅ Connected - Starting flight in 2 seconds...")
time.sleep(2)

try:
    # Arm
    print("🔓 Arming...")
    for i in range(30):
        msp.set_raw_rc([1500, 1500, 1000, 2000, 2000, 1000, 1000, 1000])
        time.sleep(0.05)

    print("✅ Armed - Climbing...")
    # Climb
    for i in range(80):
        throttle = 1000 + int((i / 80.0) * 600)
        msp.set_raw_rc([1500, 1500, throttle, 1500, 2000, 1000, 1000, 1000])
        time.sleep(0.05)

    print("✅ Hovering - Rolling right...")
    # Roll right
    for i in range(40):
        roll = 1500 + int((i / 40.0) * 300)
        msp.set_raw_rc([roll, 1500, 1600, 1500, 2000, 1000, 1000, 1000])
        time.sleep(0.05)

    # Center
    for i in range(40):
        roll = 1800 - int((i / 40.0) * 300)
        msp.set_raw_rc([roll, 1500, 1600, 1500, 2000, 1000, 1000, 1000])
        time.sleep(0.05)

    print("✅ Pitching forward...")
    # Pitch forward
    for i in range(40):
        pitch = 1500 + int((i / 40.0) * 300)
        msp.set_raw_rc([1500, pitch, 1600, 1500, 2000, 1000, 1000, 1000])
        time.sleep(0.05)

    # Center
    for i in range(40):
        pitch = 1800 - int((i / 40.0) * 300)
        msp.set_raw_rc([1500, pitch, 1600, 1500, 2000, 1000, 1000, 1000])
        time.sleep(0.05)

    print("✅ Landing...")
    # Land
    for i in range(80):
        throttle = 1600 - int((i / 80.0) * 600)
        msp.set_raw_rc([1500, 1500, throttle, 1500, 2000, 1000, 1000, 1000])
        time.sleep(0.05)

    print("🔒 Disarming...")
    # Disarm
    for i in range(30):
        msp.set_raw_rc([1500, 1500, 1000, 1000, 1000, 1000, 1000, 1000])
        time.sleep(0.05)

    print("\n✅ Demo complete! Check Rerun viewer!")

finally:
    msp.disconnect()
