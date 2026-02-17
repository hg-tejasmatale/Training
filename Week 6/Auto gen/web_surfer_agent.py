import asyncio
from autogen_agentchat.ui import Console
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_core.models import ModelInfo
import os

async def main() -> None:
    # ✅ Never hardcode secrets
    api_key = ""
    if not api_key:
        raise RuntimeError("Set GOOGLE_API_KEY in your environment")

    gemini_client=OpenAIChatCompletionClient(
            model="gemini-2.5-flash-lite",
            api_key=api_key,
            model_info=ModelInfo(
                vision=True,
                function_calling=True,
                json_output=True,
                family="unknown",
                structured_output=True,
            ),
        )

    web_surfer_agent = MultimodalWebSurfer(
        name="MultimodalWebSurfer",
        model_client=gemini_client,
    )

    user = AssistantAgent(name = "user",
    model_client = gemini_client,
    description = "You are and ai agent who summarize the web content and give the summarization of the result")


    agent_team = RoundRobinGroupChat([web_surfer_agent,user], max_turns=5)

    task = """Navigate to Google and search about Demon1 valorant player.
    """

    stream = agent_team.run_stream(task=task)
    await Console(stream)

    await web_surfer_agent.close()

if __name__ == "__main__":
    asyncio.run(main())