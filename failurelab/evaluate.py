"""Validate and summarize simulator traces without model-generated verdicts."""
import argparse
import json
import math
from pathlib import Path


def number(value, name, minimum=None):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def point(value, name):
    if not isinstance(value, list) or len(value) != 2:
        raise ValueError(f"{name} must contain x and y")
    return [number(v, name) for v in value]


def evaluate(run):
    if run.get("schema_version") != "1.0":
        raise ValueError("Unsupported schema_version")
    scenario = run["scenario"]
    start = point(scenario["start_m"], "start_m")
    goal = point(scenario["goal_m"], "goal_m")
    tolerance = number(scenario["goal_tolerance_m"], "goal_tolerance_m", 0)
    horizon = number(scenario["duration_s"], "duration_s", 0)
    if tolerance == 0 or horizon == 0:
        raise ValueError("Goal tolerance and duration must be positive")
    trace = run["trace"]
    if not isinstance(trace, list) or not trace:
        raise ValueError("A nonempty trace is required")
    previous_t = -1.0
    positions = []
    for sample in trace:
        t = number(sample["t_s"], "t_s", 0)
        if t <= previous_t or t > horizon + 1e-8:
            raise ValueError("Trace timestamps must increase and stay within the duration")
        positions.append(point(sample["position_m"], "position_m"))
        previous_t = t
    if trace[0]["t_s"] != 0 or math.dist(positions[0], start) > 1e-8:
        raise ValueError("Trace must begin at time zero at start_m")
    collision_count = 0
    for event in run["events"]:
        t = number(event["t_s"], "event t_s", 0)
        if t > previous_t:
            raise ValueError("Event cannot occur beyond recorded trace")
        if event["type"] not in ("collision", "sensor_dropout", "sensor_restored"):
            raise ValueError("Unknown event type")
        collision_count += event["type"] == "collision"
    reached_goal = math.dist(positions[-1], goal) <= tolerance
    reason = run["termination"]
    if reason not in ("goal", "collision", "timeout", "cancelled"):
        raise ValueError("Unknown termination reason")
    if reason == "goal" and not reached_goal:
        raise ValueError("Goal termination requires a final position within tolerance")
    if reason == "collision" and collision_count == 0:
        raise ValueError("Collision termination requires collision evidence")
    if reason == "timeout" and not math.isclose(previous_t, horizon, abs_tol=1e-8):
        raise ValueError("Timeout requires the complete simulation duration")
    return {
        "run_id": run["run_id"],
        "controller_id": run["controller_id"],
        "completed": reason == "goal" and reached_goal and collision_count == 0,
        "termination": reason,
        "elapsed_s": previous_t,
        "distance_m": sum(math.dist(a, b) for a, b in zip(positions, positions[1:])),
        "final_goal_distance_m": math.dist(positions[-1], goal),
        "recorded_collisions": collision_count,
        "samples": len(trace),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    args = parser.parse_args()
    try:
        result = evaluate(json.loads(args.run.read_text(encoding="utf-8")))
    except (ValueError, KeyError, TypeError, OSError) as exc:
        parser.exit(2, f"Invalid run: {exc}\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
