from a2a.server.tasks import TaskUpdater
from a2a.types import Message, Part, TaskState, TextPart
from a2a.utils import get_message_text, new_agent_text_message
from loguru import logger

from graph import graph


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

        initial_state = {"problem_description": input_text, "reflections": []}
        result = graph.invoke(initial_state)
        response = result["code"]
        logger.info(f"Agent: {response}")

        await updater.add_artifact(
            parts=[Part(root=TextPart(text=response))],
            name="Response",
        )
