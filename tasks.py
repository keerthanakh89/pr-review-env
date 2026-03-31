
TASKS = [
    {
        "name": "easy",
        "pr_diff": "if user == None: pass",
        "expected_issues": ["null check"]
    },
    {
        "name": "medium",
        "pr_diff": '''
def calc():
    x=1
    return x
''',
        "expected_issues": ["bad naming", "no comments"]
    },
    {
        "name": "hard",
        "pr_diff": '''
for i in range(len(arr)):
    for j in range(len(arr)):
        pass
''',
        "expected_issues": ["performance", "nested loop"]
    }
]
