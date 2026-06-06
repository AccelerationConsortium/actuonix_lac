"""Interactive demo: prompt for a target position in mm and drive the actuator.

Targets must be in [5, 95] mm to stay clear of the end stops on a 100 mm stroke.
Ctrl+C (or Ctrl+Z + Enter on Windows) exits.

Run with:
    uv run python examples/interactive.py
"""
import sys
import time

from pylac import ActuonixLAC

STROKE_MM = 100
MIN_MM, MAX_MM = 5.0, 95.0
ACCURACY = 8                 # ~0.78 mm deadband on a 100 mm stroke
SETTLE_TIMEOUT_S = 10
POLL_PERIOD_S = 0.1


def mm_to_count(mm: float) -> int:
    return round(mm * 1023 / STROKE_MM)


def count_to_mm(c: int) -> float:
    return c * STROKE_MM / 1023


def prompt_target() -> float | None:
    """Ask for a target in mm. Return None on EOF (Ctrl+Z / Ctrl+D)."""
    try:
        raw = input(f"target mm [{MIN_MM:.0f}-{MAX_MM:.0f}] (Ctrl+C to quit): ").strip()
    except EOFError:
        return None
    if not raw:
        return prompt_target()
    try:
        mm = float(raw)
    except ValueError:
        print(f"  '{raw}' is not a number.")
        return prompt_target()
    if not (MIN_MM <= mm <= MAX_MM):
        print(f"  {mm:g} mm is outside [{MIN_MM:g}, {MAX_MM:g}] mm.")
        return prompt_target()
    return mm


def wait_until_settled(lac: ActuonixLAC, target_mm: float) -> float:
    """Poll feedback until inside the actuator's deadband or timeout."""
    deadband_mm = (ACCURACY / 1023) * STROKE_MM
    t0 = time.perf_counter()
    pos = count_to_mm(lac.get_feedback())
    while time.perf_counter() - t0 < SETTLE_TIMEOUT_S:
        pos = count_to_mm(lac.get_feedback())
        if abs(pos - target_mm) <= deadband_mm:
            break
        time.sleep(POLL_PERIOD_S)
    return pos


def main() -> int:
    lac = ActuonixLAC()
    lac.set_speed(1023)
    lac.set_accuracy(ACCURACY)
    print(f"connected. current position: {count_to_mm(lac.get_feedback()):.2f} mm")

    try:
        while True:
            target = prompt_target()
            if target is None:        # EOF
                print()
                break
            lac.set_position(mm_to_count(target))
            t0 = time.perf_counter()
            pos = wait_until_settled(lac, target)
            print(f"  arrived: {pos:.2f} mm (target {target:.2f}, elapsed {time.perf_counter()-t0:.2f}s)")
    except KeyboardInterrupt:
        print("\ninterrupted")
    return 0


if __name__ == "__main__":
    sys.exit(main())
