from env import PREnv, Action

class Client:
    def __init__(self):
        self.env = PREnv()

    def reset(self, task):
        return self.env.reset(task)

    def step(self, action):
        return self.env.step(Action(**action))

    def state(self):
        return self.env.state()