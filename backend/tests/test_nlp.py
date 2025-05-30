import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import types
fake_response = {
    "choices": [
        {
            "message": {
                "content": (
                    '{"title": "Test", "date_iso": "2024-01-01", "time_iso": "10:00", "priority": "low"}'
                )
            }
        }
    ]
}

# Create fake openai module before import
fake_openai = types.SimpleNamespace()

class FakeChat:
    @staticmethod
    def create(**kwargs):
        return fake_response

fake_openai.ChatCompletion = FakeChat
sys.modules['openai'] = fake_openai

from services.nlp import parse_task, TaskDraft


def test_parse_task():
    result = parse_task('dummy text')
    assert isinstance(result, TaskDraft)
    assert result.title == 'Test'
    assert result.date_iso == '2024-01-01'
    assert result.time_iso == '10:00'
    assert result.priority == 'low'
