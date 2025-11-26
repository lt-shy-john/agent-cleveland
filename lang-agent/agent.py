from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai import types
import asyncio

from .config import config
from plugin.CountInvocationPlugin import CountInvocationPlugin
from .tools import find_lang_agent

root_agent = Agent(
    name="language_teaching_agent",
    model=config.worker_model,
    description="The lang-agent which teaches user about a foreign language.",
    instruction=f"""
    You are a language teaching assistant. Your primary function is to help users to learn vocabulary of foreign language of their choice.

    Your workflow is as follows:
    1.  **Plan:** The user will ask help for one language. To do this, use the `find_lang_agent` tool.
    2.  **Teach** You provide them one example of using the language. 

    If you are asked what is your name respond with Agent Cleveland.
    """,
    sub_agents=[
        find_lang_agent,
    ],
    tools=[],
    output_key="blog_outline",
)

async def main():
    prompt = 'Hi, I am Cleveland. How can I help you?'

    runner = InMemoryRunner(
        agent=root_agent,
        plugins=[
            LoggingPlugin(), CountInvocationPlugin()
        ],
    )

    session = await runner.session_service.create_session(
        user_id='user',
        app_name='agent_cleveland',
    )

    async for event in runner.run_async(
            user_id='user',
            session_id=session.id,
            new_message=types.Content(
                role='user', parts=[types.Part.from_text(text=prompt)]
            )
    ):
        print(f'** Got event from {event.author}')

if __name__ == "__main__":
    asyncio.run(main())
