
import gradio as gr
from env import PREnv, Action
from tasks import TASKS

env = PREnv()

def review(task_index, comment):
    task = TASKS[int(task_index)]
    env.reset(task)
    action = Action(action_type="comment", comment=comment)
    _, reward, _, _ = env.step(action)
    return reward.score

iface = gr.Interface(
    fn=review,
    inputs=["number", "text"],
    outputs="text",
    title="PR Review Environment"
)

iface.launch()
