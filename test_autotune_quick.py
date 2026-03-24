#!/usr/bin/env python3
"""Quick test to verify autotune debug values are working"""
import sys
sys.path.insert(0, 'tools')
from sitl_rerun_bridge import MSPClient
import time

msp = MSPClient()
if not msp.connect():
    print("❌ Failed to connect to SITL")
    sys.exit(1)

print("✅ Connected to SITL")
print("\n📊 Checking debug values (should see chirp data)...")

for i in range(5):
    debug = msp.get_debug()
    if debug:
        print(f"  Debug values: {debug}")
    time.sleep(0.5)

print("\n✅ Test complete!")
print("   If debug values are non-zero, autotune code is working!")

msp.disconnect()
