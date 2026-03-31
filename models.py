from pydantic import BaseModel


class Observation(BaseModel):
    pr_diff: str


class Action(BaseModel):
    action_type: str
    comment: str


class Reward(BaseModel):
    score: float