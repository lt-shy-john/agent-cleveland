from google.adk.agents import Agent
from google.adk.tools import FunctionTool

from .config import config
from .tools import find_lang_agent

root_agent = Agent(
    name="language_teaching_agent",
    model=config.worker_model,
    description="The agent which teaches user about a foreign language.",
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