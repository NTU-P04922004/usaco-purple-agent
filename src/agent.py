import os
import re

from a2a.server.tasks import TaskUpdater
from a2a.types import Message, Part, TaskState, TextPart
from a2a.utils import get_message_text, new_agent_text_message
from loguru import logger
from openai import AsyncOpenAI

from prompt import DIRECT_PROMPT

BASE_URL = os.environ.get("BASE_URL", "https://api.sambanova.ai/v1")
API_KEY = os.environ.get("API_KEY", "dummy")
MODEL_ID = os.environ.get("MODEL_ID", "Meta-Llama-3.3-70B-Instruct")


def extract_python_code_block(markdown_string):
    pattern = r"```python\s*\n(.*?)```"
    code_blocks = re.findall(pattern, markdown_string, flags=re.DOTALL | re.IGNORECASE)
    return code_blocks[0] if code_blocks else ""


class Agent:
    def __init__(self):
        pass

    async def run(self, message: Message, updater: TaskUpdater) -> None:
        """Implement your agent logic here.

        Args:
            message: The incoming message
            updater: Report progress (update_status) and results (add_artifact)

        Use self.messenger.talk_to_agent(message, url) to call other agents.
        """
        input_text = get_message_text(message)

        await updater.update_status(
            TaskState.working, new_agent_text_message("Thinking...")
        )

        client = AsyncOpenAI(
            base_url=BASE_URL,
            api_key=API_KEY,
        )
        prompt = DIRECT_PROMPT.format(problem=input_text)
        messages = [
            {"role": "user", "content": prompt},
        ]
        response = await client.chat.completions.create(
            model=MODEL_ID, messages=messages, temperature=0
        )
        code = extract_python_code_block(response.choices[0].message.content)

        logger.info(f"Agent: {code}")

        await updater.add_artifact(
            parts=[Part(root=TextPart(text=code))],
            name="Solution",
        )
