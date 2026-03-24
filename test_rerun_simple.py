#!/usr/bin/env python3
"""Minimal test to verify Rerun API works"""
import rerun as rr
import numpy as np
import time

print("Testing Rerun API...")
rr.init("test", spawn=True)
print("✅ Rerun initialized - viewer should open")
print()

# Create scene
rr.log("world", rr.ViewCoordinates.RIGHT_HAND_Z_UP, static=True)

print("Logging 50 frames...")
for i in range(50):
    rr.set_time("frame", sequence=i)
    pos = [np.sin(i * 0.1), 0, 1.0]
    rr.log("world/box", rr.Boxes3D(centers=[pos], half_sizes=[0.1, 0.1, 0.1], colors=[255, 0, 0]))
    rr.log("data/value", rr.Scalars(np.array([np.sin(i * 0.1) * 100])))
    print(f"\rFrame {i}/50", end="", flush=True)
    time.sleep(0.1)

print("\n\n✅ Done! Check Rerun viewer for:")
print("   - Timeline at bottom")
print("   - Red box in 3D view")
print("   - Sine wave plot")
