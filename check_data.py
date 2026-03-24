#!/usr/bin/env python3
"""Check what data SITL is actually returning"""
import sys
sys.path.insert(0, 'tools')
from sitl_rerun_bridge import MSPClient
import time

msp = MSPClient()
if not msp.connect():
    sys.exit(1)

print("Checking SITL data for 5 seconds...\n")

for i in range(10):
    status = msp.get_status()
    attitude = msp.get_attitude()
    imu = msp.get_raw_imu()
    motors = msp.get_motor()

    print(f"Sample {i+1}:")
    if attitude:
        print(f"  Attitude: Roll={attitude['roll']:.1f}° Pitch={attitude['pitch']:.1f}° Yaw={attitude['yaw']}°")
    if imu:
        print(f"  Gyro: {imu['gyro']}")
    if motors:
        print(f"  Motors: {motors[:4]}")
    if status:
        print(f"  Armed: {status['armed']}")
    print()

    time.sleep(0.5)

msp.disconnect()
print("\n💡 If all values are zero/unchanged, SITL needs physics simulation (Gazebo)")
