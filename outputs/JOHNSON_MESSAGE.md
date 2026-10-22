Johnson, we're building FailureLab for the Nebius x NVIDIA hackathon. It's an AI testing engineer for a small warehouse robot simulator: the AI proposes scenarios, Python runs them, and the app shows failures with replays and compares controller fixes.

The deadline is October 30 at 1 p.m. Toronto time. We're aiming to submit October 29. You own the Python simulation engine and controllers. I'll handle the app, Nebius AI planner, replay UI, and integration with Codex.

Please build this first:

1. A simple 10 m by 10 m 2D warehouse with a circular robot, axis-aligned rectangular shelves, a start, and a goal. Use metres and seconds throughout. No 3D or hardware.
2. A deterministic `run_scenario(scenario: dict, controller_id: str) -> dict` function in `failurelab/simulator.py`. The same input, controller and seed should reproduce the same trace.
3. A reasonable simple navigation controller with local obstacle sensing. It must use its observations, not secretly read the whole simulator state. Document what the controller can see.
4. Collision checking against shelves and boundaries, checking the movement segment so the robot cannot jump through obstacles. Validate start/goal clearance and route feasibility for the robot's radius.
5. A sensor-delay buffer. Start with zero delay, then support 0–0.5 seconds. Delay actual observations, not the final metrics. Keep the physical integration timestep fixed initially.
6. Return timestamped positions, collision events, a termination reason, and the full scenario, matching the attached contract.

TODAY: get deterministic movement and one successful no-delay delivery producing JSON. Tomorrow: obstacle sensing, collision checks, delay, and replayable failure cases. You don't need to build FastAPI, a website, or any AI integration.

After that, add a seeded random-scenario generator so we can compare AI-selected experiments with random testing. Then implement a corrected controller and test both on scenarios we didn't use to tune the fix. Keep test cases separate from planner prompts.

Please use Python 3.11+ and as few dependencies as possible. Push all source files and exact run instructions to the shared repo. Check a fresh checkout before saying it runs. Don't commit API keys or virtual environments.

Use the attached SIMULATOR_CONTRACT.md and delivery.json fixture for field names. Tell me before changing the interface. The fixture is for integration; our demo results must come from real simulator runs.

For our first check-in, send the source, one output JSON, the command to run it, and any blockers. We're aiming for a small system we can explain and test thoroughly.
