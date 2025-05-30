# In-memory storage for push tokens and tasks

push_tokens: dict[str, str] = {}
# Example task: {'user_id': '1', 'title': 'Finish report', 'due': datetime}
tasks: list[dict] = []
