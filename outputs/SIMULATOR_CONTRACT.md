# FailureLab simulator contract v1.0

Python entry point: `failurelab.simulator.run_scenario(scenario: dict, controller_id: str) -> dict`.
Raise `ValueError` for invalid scenarios. Do not return invalid layouts as controller failures. No network calls or UI inside the simulator. Input dictionaries must not be mutated.

## Coordinates and units

Coordinates are `[x, y]` in metres with origin at bottom left; positive x right, positive y up. UI inverts y for screen rendering. Time and delay are seconds. Speed is metres per second. A robot is a circle; shelves are axis-aligned rectangles. Contact counts as a collision. Goal tolerance applies to robot-centre distance.

## Scenario fields

| Field | Type | Initial bounds / meaning |
|---|---|---|
| seed | integer | 0 through 2147483647; use a local RNG |
| world_size_m | [number, number] | [10, 10] in first version |
| start_m, goal_m | [number, number] | Within bounds and clear for the full robot radius |
| goal_tolerance_m | number | 0.2 |
| robot_radius_m | number | 0.2 |
| speed_mps | number | 0.2 through 1.5 |
| dt_s | number | Fixed 0.05 initially |
| duration_s | number | 30 |
| sensor_delay_s | number | 0 through 0.5, initially multiples of dt_s |
| obstacles | list | 0–8 rectangles: {id, x_m, y_m, width_m, height_m}; positive sizes, in bounds, unique IDs |

Initial agent proposal fields: `speed_mps`, `sensor_delay_s`, and `obstacles` only. All other fields come from server-side bounds and presets. Reject extra fields at the API boundary. Never execute model-generated code.

Validate that a route exists with obstacle inflation for the robot radius. Document the resolution if using a discretized path feasibility check. Delayed samples should describe readings captured in the sensor's documented coordinate frame; preserve capture timestamps. During startup, use the first reading until the buffer contains enough history. Keep ground truth and sensed state separate. Check continuous movement for collisions using segment/expanded-rectangle geometry or a documented sufficiently conservative method.

## Run fields

`schema_version`: "1.0"; `run_id`: unique string; `controller_id`: versioned identifier; `scenario`: exact input; `termination`: goal, collision, timeout, or cancelled; `trace`: ordered samples; `events`: ordered events.

Each trace sample requires `t_s` and `position_m`. Start at time zero and the scenario start. Timestamps strictly increase. Include the final position and time. Simulator output should include each integration step; the compact fixture is intentionally sparse for integration testing. Optional additions: heading_rad, observed_capture_t_s, command_velocity_mps. Do not change required fields without a version bump.

Each event requires `type` and `t_s`; optional `obstacle_id` and `detail`. Initial accepted types: collision, sensor_dropout, sensor_restored. Event time must fall within the trace. Stop on the first collision. Check collision before declaring goal completion. A timeout must reach duration_s; cancelled runs are not timeout failures.

Use `python -m failurelab.evaluate path/to/run.json` for a structural evidence check. This checker does not validate physical fidelity or independently detect collisions. The simulator owns geometry and event generation, with independent geometry tests.

## Acceptance tests for Johnson

- Same scenario/seed produces identical positions and outcomes (run IDs may differ).
- Empty map reaches the goal; start at goal terminates immediately at t=0.
- Reject start/goal intersecting a shelf or boundary and layouts with no feasible route.
- A fast robot cannot pass through a thin shelf between samples.
- Exact boundary contact and shelf-corner contact are handled consistently.
- Delay zero supplies current observations; delay 0.2 at dt 0.05 supplies observations four steps old after startup.
- A controller cannot access current hidden obstacle state through delayed observations.
- A failure is repeatable without an AI call.
- Controller correction is tested on additional frozen cases, not only the discovered failure.

API wrapper planned for Hogan: POST /api/runs with {scenario, controller_id}, returns this run object; GET /api/health. Johnson only needs the Python function.
