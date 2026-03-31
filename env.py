from typing import Dict
from models import Observation, Action, Reward


class PREnv:
    def __init__(self):
        self.task = None
        self.done = False

    def reset(self, task: Dict):
        self.done = False
        self.task = task
        return Observation(pr_diff=self.task["pr_diff"])

    def state(self):
        return Observation(pr_diff=self.task["pr_diff"])

    def step(self, action: Action):
        if self.done:
            return self.state(), Reward(score=0.0), True, {}

        comment = action.comment.lower()
        expected = self.task["expected_issues"]

        # scoring logic
        score = sum(1 for e in expected if e in comment) / len(expected)

        # penalty for wrong approval
        if action.action_type == "approve" and score < 1:
            score -= 0.3

        score = max(0.0, min(1.0, score))
        self.done = True

        return self.state(), Reward(score=score), True, {}