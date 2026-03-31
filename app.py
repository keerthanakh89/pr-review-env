import gradio as gr
from env import PREnv, Action
from tasks import TASKS


def run_all_tasks():
    env = PREnv()
    output = ""

    for task in TASKS:
        env.reset(task)

        comment = "PR Review:\n"
        for issue in task["expected_issues"]:
            comment += f"- {issue}\n"

        action = Action(
            action_type="comment",
            comment=comment
        )

        _, reward, _, _ = env.step(action)

        output += f"\nTask: {task['name']}\n"
        output += f"{comment}\nScore: {reward.score}\n\n"

    return output


iface = gr.Interface(
    fn=run_all_tasks,
    inputs=[],
    outputs="text",
    title="PR Review Agent",
    description="Click run to evaluate PR review tasks"
)

iface.launch()