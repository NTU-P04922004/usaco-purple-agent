import os
import re

from a2a.server.tasks import TaskUpdater
from a2a.types import Message, Part, TaskState, TextPart
from a2a.utils import get_message_text, new_agent_text_message
from langchain_sambanova import ChatSambaNova
from loguru import logger

from prompt import DIRECT_PROMPT


def extract_python_code_block(markdown_string):
    pattern = r"```python\s*\n(.*?)```"
    code_blocks = re.findall(pattern, markdown_string, flags=re.DOTALL | re.IGNORECASE)
    return code_blocks[0] if code_blocks else None


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

        model = ChatSambaNova(
            model="Meta-Llama-3.3-70B-Instruct", max_tokens=8192, temperature=0
        )
        prompt = DIRECT_PROMPT.format(problem=input_text)
        result = model.invoke(prompt)
        code = extract_python_code_block(result.content)

        logger.info(f"Agent: {code}")

        await updater.add_artifact(
            parts=[Part(root=TextPart(text=code))],
            name="Solution",
        )
