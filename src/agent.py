from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from src.instructions import time_agent_instruction

from src.tools import get_current_time, get_time_zone

root_agent = Agent(
    model=LiteLlm(model="ollama_chat/llama3.2"),
    name="time_agent",
    description="Tells the current time in a specified city.",
    instruction=(time_agent_instruction),
    tools=[get_time_zone, get_current_time],
)
