# FailureLab: October 22–31 build plan

FailureLab helps robotics builders reproduce failures and evaluate controller corrections in a simplified warehouse simulation. NVIDIA models on Nebius propose bounded experiments; Python determines outcomes; the browser presents replayable evidence.

## Deadline and submission

Official deadline: October 30, 2026, 1 p.m. America/Toronto. Target submission: October 29, 6 p.m. Day ten is after the deadline and is for maintenance and follow-up, not required submission work.

Working track: Best Apps and Agents, positioning FailureLab as an engineering testing application using Nemotron through Token Factory. Recheck final track fit against the implemented product before submitting.

Official sources:
- https://nebiusglobalaihackathon.devpost.com/
- https://nebiusglobalaihackathon.devpost.com/rules

## Product boundary

One 2D warehouse, one circular robot, rectangular shelves, one baseline controller, one corrected controller, delayed range sensing, and bounded speed variation. Include a nominal delivery, a reproducible failure, and a comparison on separate scenarios. This is an educational simulation; its results describe this simulator, not real-world robot certification.

Keep out of the first version: 3D, hardware, arbitrary uploaded code execution, reinforcement learning, automatic controller rewriting, multiple robots, accounts, billing, and complex integrations.

Sensor delay must affect actual controller observations. Do not manufacture collisions or let the controller read hidden world state. A static fully known map alone is not a convincing sensor-delay experiment: use local reactive sensing or a clearly specified dynamic obstacle, and document the observation model.

## Ownership

Johnson owns `failurelab/simulator.py`, controllers, geometry, sensing, scenario validation, and simulator tests. Hogan and Codex own the experiment planner, API, UI, replay, integration, deployment, and submission materials. Shared contracts and metrics require both sides to agree before changing fields. Integrate daily; send complete source and setup instructions, not selected individual files.

## Daily deliverables

| Day | Date | Johnson | Hogan + Codex | Done when |
|---|---|---|---|---|
| 1 | Thu Oct 22 | Implement `run_scenario(scenario, controller_id)` with deterministic movement and nominal trace | Shared contract, evaluator, UI wireframe, confirm Nebius account/model access | A real simulator trace loads and evaluates; agree file ownership |
| 2 | Fri Oct 23 | Collision geometry, local sensing, delay buffer, valid scenarios | Browser replay and API; first live Nemotron call | Same scenario reproduces exactly; delayed sensing affects behavior; real model call succeeds |
| 3 | Sat Oct 24 | Seeded random scenario generator and hidden evaluation cases | Bounded propose/run/observe loop and experiment history | Agent can run at most 20 valid experiments with logs and graceful errors |
| 4 | Sun Oct 25 | Failure reproduction and obstacle reduction | Evidence-linked report, exported scenario and replay | Repeat a discovered failure; reduce it without losing the failure |
| 5 | Mon Oct 26 | Corrected controller plus regression tests | Before/after view and preliminary deployment | Same case compares both controllers; separate cases test regressions |
| 6 | Tue Oct 27 | Equal-budget random vs AI evaluation; preserve results | User sessions, latency/cost reporting, error states | Report actual results across multiple seeds, including failures and invalid proposals |
| 7 | Wed Oct 28 | Clean-install reproduction and final simulator fixes | Feature freeze; demo recording, README, license, Devpost text, provider feedback | Another person can run the project; hosted demo works without your login |
| 8 | Thu Oct 29 | Independently reproduce demo and check measurements | Submit by 6 p.m.; verify uploaded video, links and required fields | Submission receipt/status confirmed and exact submitted revision recorded |
| 9 | Fri Oct 30 | Available for urgent corrections | Final verification before 1 p.m.; no speculative features | Entry remains complete before official deadline |
| 10 | Sat Oct 31 | Document next experiments | Maintain demo and gather feedback | Preserve submitted version and plan future changes separately |

## Evaluation

Start with five independent seeds per method and 20 valid simulator calls per seed, subject to the available API budget. Record every attempted proposal, including invalid ones. Count reduction calls separately and equally across methods. Record valid failure yield, distinct failure cases, time to first failure, total wall time, tokens, and cost when available. Save model ID, prompt version, controller version, scenario, seed, trace and metrics. Freeze held-out scenarios before tuning the corrected controller. Do not claim AI beats random search unless results support it. Failure explanations must cite run IDs and trace times; mark causal explanations as hypotheses unless a controlled rerun tests them.

## Checkpoints

- End of October 23: if sensor delay has no meaningful effect, fix the observation model before adding UI features.
- End of October 24: if the AI loop is unreliable, narrow proposal parameters and retain one functioning live model path.
- End of October 26: freeze scope to search, replay, and comparison. Reduction is optional if it threatens submission.
- Never replace failed live calls with prerecorded results presented as live. Saved replays should be identified as saved runs.

## Submission checklist

- Each participant meets the official age-of-majority and other eligibility rules.
- Runtime use of an NVIDIA open-source model through Nebius is demonstrated.
- Public repository includes all source, assets, setup instructions, and an open-source license.
- Working demo or test build is freely accessible to judges through December 15.
- Public YouTube demo is under three minutes; show the working system and required technology.
- Description includes purpose, actual results, simulation limitations, chosen track, and tool feedback.
- Verify all links and team members, then record submission confirmation.

## Today's order

1. Send Johnson `JOHNSON_MESSAGE.md` and `SIMULATOR_CONTRACT.md`.
2. Use https://github.com/goodenough7000/FailureLab as the shared repository and work on separate feature branches.
3. Johnson builds the minimal simulator; Hogan obtains Nebius access and keeps credentials out of chat and Git.
4. Use `examples/delivery.json` to integrate the replay while the simulator is being built.
5. Replace the fixture with Johnson's first real run and evaluate it before the first daily check-in.
