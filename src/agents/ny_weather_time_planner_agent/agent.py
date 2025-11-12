

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from google.genai import types

from .constants import APP_NAME, USER_ID, SESSION_ID, LLM_MODEL_NAME
from .tools import get_weather, get_current_time
from .config import thinking_config, planner

# Step 1: Create a ThinkingConfig
print("ThinkingConfig:", thinking_config)

# Step 2: Instantiate BuiltInPlanner
print("BuiltInPlanner created.", planner)

# Step 3: Wrap the planner in an LlmAgent
root_agent = LlmAgent(
    model=LiteLlm(model=LLM_MODEL_NAME),  # Set your model name
    name="weather_and_time_agent",
    instruction="You are an agent that returns time and weather",
    planner=planner,
    tools=[get_weather, get_current_time]
)

# Session and Runner
session_service = InMemorySessionService()
session = session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
runner = Runner(agent=root_agent, app_name=APP_NAME, session_service=session_service)
print("Session and runner has been initialized.", runner)

# Agent Interaction
def call_agent(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    for event in events:
        print(f"\nDEBUG EVENT: {event}\n")
        if event.is_final_response() and event.content:
            final_answer = event.content.parts[0].text.strip()
            print("\n🟢 FINAL ANSWER\n", final_answer, "\n")

call_agent("If it's raining in New York right now, what is the current temperature?")