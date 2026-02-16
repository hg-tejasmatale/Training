import asyncio
import os
from pathlib import Path

from autogen_agentchat.agents import AssistantAgent, CodeExecutorAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.code_executors.local import LocalCommandLineCodeExecutor
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelInfo

async def main() -> None:
    
    model_client = OpenAIChatCompletionClient(
        model="gemini-2.5-flash",
        api_key=('AIzaSyA3m4KtAnU9A8h07h9MmuiCp0i31HQd86g'),
        model_info=ModelInfo(
            vision=True,
            function_calling=True,
            json_output=True,
            family="unknown",
            structured_output=True,
    ),
)


    coder = AssistantAgent(
        "coder",
        model_client=model_client,
        
system_message=(
    "You are a senior engineer. Output ONLY runnable Python code inside "
    "```python``` blocks. Do not include any other code blocks."
)
,
    )

    executor = CodeExecutorAgent(
        "executor",
        model_client=model_client,
        code_executor=LocalCommandLineCodeExecutor(work_dir=Path.cwd() / "runs"),
    )

    user = UserProxyAgent("user")  # human in the loop

    termination = TextMentionTermination("exit", sources=["user"])
    team = RoundRobinGroupChat([user, coder, executor], termination_condition=termination)

    try:
        await Console(team.run_stream())
    finally:
        await model_client.close()


if __name__ == "__main__":
    asyncio.run(main())