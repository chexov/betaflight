# Betaflight Hybrid Autotune - Implementation Status

## ✅ Completed: Firmware Changes

### 1. Autotune Metrics Structure (`src/main/flight/pid.h`)
Added `autotuneMetrics[]` to `pidRuntime_t`:
- `peakGyroResponse` - Maximum gyro deviation during chirp
- `rmsError` - RMS tracking error
- `oscillationCount` - Number of zero-crossings
- `sampleCount` - Number of samples collected
- `confidence` - Data quality metric (0-100%)
- `suggestedP` - Calculated P gain suggestion
- `suggestedD` - Calculated D gain suggestion
- `dataValid` - Flag indicating valid data

### 2. Real-Time Metric Collection (`src/main/flight/pid.c`)
During chirp execution:
- Tracks peak gyro response
- Accumulates squared error for RMS calculation
- Counts oscillations (zero-crossings)
- Outputs to DEBUG_CHIRP for visualization:
  - `DEBUG_CHIRP[0]` - Chirp phase (existing)
  - `DEBUG_CHIRP[1]` - Gyro response (NEW)
  - `DEBUG_CHIRP[2]` - Chirp setpoint (NEW)
  - `DEBUG_CHIRP[3]` - Tracking error (NEW)

When chirp completes:
- Finalizes RMS error
- Calculates confidence score
- Estimates suggested P and D gains using simple heuristics:
  - Response ratio < 0.7 → Increase P by 15%
  - Response ratio > 1.3 → Decrease P by 10%
  - D gain scales proportionally with P

### 3. Enhanced Blackbox Logging (`src/main/blackbox/blackbox.c`)
Added to blackbox header for all 3 axes:
- `autotune_{axis}_peak_response`
- `autotune_{axis}_rms_error`
- `autotune_{axis}_oscillations`
- `autotune_{axis}_confidence`
- `autotune_{axis}_suggested_p`
- `autotune_{axis}_suggested_d`

## 🎯 How It Works

### In-Flight (Real-Time):
1. User activates CHIRP mode via RC switch
2. Chirp signal sweeps frequencies on current axis
3. Firmware collects metrics in real-time:
   - Peak gyro response
   - RMS error
   - Oscillation count
4. Basic P/D suggestions calculated immediately
5. Debug values streamed to Rerun for live visualization

### Post-Flight (Offline):
1. Download blackbox log
2. Analyze with offline tool (TODO):
   - FFT-based frequency response
   - Bode plots
   - Phase/gain margins
   - Optimal PID calculation
3. Review suggestions and apply via CLI

## 🚀 Testing in SITL

### Start SITL with Rerun:
```bash
# Terminal 1: SITL
./obj/betaflight_2025.12.0-beta_SITL

# Terminal 2: Rerun Visualization
source .venv/bin/activate
python tools/sitl_rerun_bridge.py

# Terminal 3: Chirp Test
source .venv/bin/activate
python tools/chirp_test.py  # (needs manual start)
# OR
python auto_demo.py         # (runs automatically)
```

### What to Watch in Rerun:
- `chirp/debug_0` - Chirp phase signal
- `chirp/debug_1` - **Gyro response** (NEW!)
- `chirp/debug_2` - **Chirp setpoint** (NEW!)
- `chirp/debug_3` - **Tracking error** (NEW!)

### Expected Behavior:
Without real flight physics (no Gazebo):
- Chirp signal generates correctly ✅
- Debug values update ✅
- Metrics are collected ✅
- Blackbox logs data ✅
- Gyro response = 0 (no physics simulation) ⚠️

With real hardware:
- Full gyro response to chirp excitation
- Actual PID effectiveness visible
- Meaningful autotune suggestions

## 📊 Current Limitations

1. **Simple heuristics** - Basic P/D estimation, not optimal
2. **No I gain tuning** - Only P and D suggested
3. **No filter suggestions** - Doesn't suggest notch frequencies
4. **SITL has no physics** - Can't test actual response without Gazebo/hardware

## 🔜 Next Steps

### Phase 1: Verify Basic Functionality ✅
- [x] Add metrics struct
- [x] Implement collection
- [x] Add blackbox logging
- [x] Rebuild SITL
- [x] Test in SITL - verify debug values appear
- [x] Build for F405 - verified flash usage (57.86%, 42% free)

### Phase 2: Hardware Testing
- [ ] Build for real flight controller target
- [ ] Flash firmware
- [ ] Run chirp on real quad
- [ ] Collect blackbox with actual flight data

### Phase 3: Offline Analysis Tool ✅
- [x] Python script to parse blackbox
- [x] FFT-based frequency response analysis
- [x] Bode plot generation
- [x] Advanced PID calculation (phase margin, bandwidth targets)
- [x] CLI command generator
- [x] Test suite with synthetic data validation

### Phase 4: Refinement
- [ ] Improve P/D estimation algorithms
- [ ] Add I gain suggestions
- [ ] Add filter suggestions based on resonances
- [ ] Confidence scoring improvements
- [ ] Multiple iteration support

## 🛠️ Using the Offline Analysis Tool

### Step 1: Perform Chirp Test on Real Hardware
1. Flash firmware to flight controller
2. Enable blackbox logging (SD card or onboard flash)
3. Set debug mode to CHIRP: `set debug_mode = CHIRP`
4. Assign chirp mode to a switch in the Modes tab
5. Fly and activate chirp mode on each axis (roll, pitch, yaw)
6. Download blackbox log and convert to CSV using Blackbox Explorer

### Step 2: Run Analysis
```bash
# Activate Python environment
source .venv/bin/activate

# Analyze blackbox CSV
python tools/chirp_analyzer.py <blackbox.csv> \
    --axis roll \
    --current-p 45 \
    --current-i 80 \
    --current-d 35 \
    --output roll_analysis.png

# Repeat for pitch and yaw axes
```

### Step 3: Review Results
- Check Bode plots (`roll_analysis.png`) for frequency response
- Review metrics:
  - **Phase margin** - should be 45-60° for stability
  - **Bandwidth** - target 80-120 Hz for racing quads
  - **Resonance peak** - high peaks indicate under-damping
- Apply suggested CLI commands in Betaflight Configurator

### Step 4: Iterate
- Test fly with new gains
- Run chirp again to verify improvement
- Iterate until desired performance achieved

### Testing with Synthetic Data
```bash
# Test the analyzer with mock data
python tools/test_chirp_analyzer.py
```

## 📝 Files Modified

```
src/main/flight/pid.h          - Added autotuneMetrics struct
src/main/flight/pid.c          - Added collection & estimation logic
src/main/blackbox/blackbox.c   - Added autotune logging
tools/sitl_rerun_bridge.py     - Updated for Rerun 0.30.1 API
tools/chirp_test.py            - Chirp test script
tools/auto_demo.py             - Non-interactive demo
tools/chirp_analyzer.py        - Offline FFT-based analysis tool ✨ NEW
tools/test_chirp_analyzer.py   - Test suite with synthetic data ✨ NEW
```

## 🎓 Design Philosophy

**Hybrid Approach:**
- Simple real-time analysis for immediate feedback
- Full offline analysis for optimal results
- User maintains control and understanding
- Low computational overhead on flight controller
- Educational - user sees data and learns tuning

**Safety:**
- No automatic PID changes
- User reviews before applying
- Confidence scores help identify good vs bad data
- Works with existing blackbox infrastructure
