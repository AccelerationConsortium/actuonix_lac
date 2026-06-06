"""End-to-end sweep demo for the Actuonix LAC.

Run with:
    uv run python examples/demo.py
"""
import time
from pylac import ActuonixLAC

STROKE_MM = 100  # change to 200 or 300 to match your actuator

def mm_to_count(mm):
    return round(mm * 1023 / STROKE_MM)

def count_to_mm(c):
    return c * STROKE_MM / 1023

lac = ActuonixLAC()
lac.set_speed(800)        # 0..1023
lac.set_accuracy(8)       # deadband in counts; smaller = tighter but jitters

print(f"start: {count_to_mm(lac.get_feedback()):.2f} mm")

for target_mm in (1.0, STROKE_MM - 1.0):   # near each end stop, leaves ~1 mm buffer
    lac.set_position(mm_to_count(target_mm))
    time.sleep(8)                          # wait for travel; tune for stroke + load
    print(f"arrived: {count_to_mm(lac.get_feedback()):.2f} mm")
