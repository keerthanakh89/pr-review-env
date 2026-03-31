
from typing import Dict
from pydantic import BaseModel

class Observation(BaseModel):
    pr_diff: str

class Action(BaseModel):
    action_type: str
    comment: str

class Reward(BaseModel):
    score: float

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

        score = sum(1 for e in expected if e in comment) / len(expected)

        if action.action_type == "approve" and score < 1:
            score -= 0.3

        score = max(0.0, min(1.0, score))
        self.done = True

        return self.state(), Reward(score=score), True, {}
