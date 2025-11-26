from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.runners import InMemoryRunner
from google.adk.plugins.logging_plugin import LoggingPlugin
from google.genai import types
import asyncio

from .config import config
from plugin.CountInvocationPlugin import CountInvocationPlugin

init_agent = Agent(
    name="language_teaching_init_agent",
    model=config.worker_model,
    description="The lang-agent which teaches user about a foreign language.",
    instruction=f"""
    You are a language teaching assistant. Your primary function is to help users to learn vocabulary of foreign language of their choice.

    Your workflow is as follows:
    1.  **Plan:** The user will ask help for one language. To do this, use the `find_lang_agent` tool.
    2.  **Decide** You then ask what the user want to do today. They will prompt you based on the following options: 
        *  **Teach** You provide them one example of using the language. 
        *  **Conversation** You and the user talks with the language casually. 
        *  **Quiz** You ask the user a word from the language.  

    If you are asked what is your name respond with Agent Cleveland.
    """,
    tools=[],
    output_key="conversation",
)

find_lang_agent = Agent(
    name="find_lang_agent",
    model=config.worker_model,
    instruction="""Find out what language is the user after. """,
    output_key="lang",
)

teacher_agent = Agent(
    name="teacher_agent",
    model=config.worker_model,
    instruction="""Pick any word from the language {lang}, tell the user the meaning of this word. """,
    output_key="vocab_meaning",
)

conversation_agent = Agent(
    name="conversation_agent",
    model=config.worker_model,
    instruction="""You are a casual conversation agent, when the user gives prompts you answer them using the language {lang}. """,
    output_key="sentence",
)

quiz_agent = Agent(
    name="quiz_agent",
    model=config.worker_model,
    instruction="""Ask the user one of the meaning of the words from {lang}. If the user gives the response similar to the word's meaning, then give one point to the user. """,
    output_key="point",
)

parallel_lang_agent = ParallelAgent(
    name="ParallelLangTeam",
    sub_agents=[teacher_agent, conversation_agent, quiz_agent],
)

conversation_refinement_loop = LoopAgent(
    name="LangConversationRefinementLoop",
    sub_agents=[parallel_lang_agent],
    max_iterations=10,  # Prevents infinite loops
)

root_agent = SequentialAgent(
    name="language_teaching_agent",
    description="The lang-agent which teaches user about a foreign language.",
    sub_agents=[
        init_agent, conversation_refinement_loop
    ],
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
