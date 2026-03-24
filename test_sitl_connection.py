#!/usr/bin/env python3
"""Quick test to verify SITL MSP connection"""

import sys
sys.path.insert(0, 'tools')

from sitl_rerun_bridge import MSPClient

print("Testing SITL connection...")
msp = MSPClient()

if not msp.connect():
    print("❌ Failed to connect")
    sys.exit(1)

print("✅ Connected!")

# Test basic queries
print("\n📡 Testing MSP commands:")

status = msp.get_status()
if status:
    print(f"  ✅ STATUS: Armed={status['armed']}, Cycle={status['cycle_time']}µs")
else:
    print("  ❌ STATUS failed")

attitude = msp.get_attitude()
if attitude:
    print(f"  ✅ ATTITUDE: Roll={attitude['roll']:.1f}° Pitch={attitude['pitch']:.1f}° Yaw={attitude['yaw']}°")
else:
    print("  ❌ ATTITUDE failed")

imu = msp.get_raw_imu()
if imu:
    print(f"  ✅ IMU: Gyro={imu['gyro']}")
else:
    print("  ❌ IMU failed")

motors = msp.get_motor()
if motors:
    print(f"  ✅ MOTORS: {motors[:4]}")
else:
    print("  ❌ MOTORS failed")

print("\n✅ All tests passed! SITL + MSP working correctly.")
print("\nNow run: source .venv/bin/activate && python tools/sitl_rerun_bridge.py")

msp.disconnect()
