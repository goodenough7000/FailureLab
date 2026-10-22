import copy
import json
from pathlib import Path
import unittest

from failurelab.evaluate import evaluate


class EvidenceTests(unittest.TestCase):
    def setUp(self):
        self.run = json.loads((Path(__file__).resolve().parents[1] / "examples/delivery.json").read_text())

    def test_delivery_distance(self):
        result = evaluate(self.run)
        self.assertTrue(result["completed"])
        self.assertEqual(result["distance_m"], 2)

    def test_collision_prevents_success_even_at_goal(self):
        self.run["events"] = [{"type": "collision", "t_s": 1.5}]
        self.assertFalse(evaluate(self.run)["completed"])

    def test_false_goal_is_rejected(self):
        self.run["trace"][-1]["position_m"] = [2, 1]
        with self.assertRaises(ValueError):
            evaluate(self.run)

    def test_partial_trace_cannot_claim_timeout(self):
        self.run["termination"] = "timeout"
        with self.assertRaises(ValueError):
            evaluate(self.run)

    def test_cancelled_run_is_not_success(self):
        self.run["termination"] = "cancelled"
        self.assertFalse(evaluate(self.run)["completed"])

    def test_bad_timestamps_rejected(self):
        for value in [0, -1, float("nan"), 100, True]:
            with self.subTest(value=value):
                run = copy.deepcopy(self.run)
                run["trace"][1]["t_s"] = value
                with self.assertRaises(ValueError):
                    evaluate(run)

    def test_future_collision_rejected(self):
        self.run["events"] = [{"type": "collision", "t_s": 20}]
        with self.assertRaises(ValueError):
            evaluate(self.run)


if __name__ == "__main__":
    unittest.main()
