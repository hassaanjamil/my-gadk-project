from dotenv import load_dotenv
import os
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from .instructions import root_agent_description1, root_agent_instruction1
from .tools import get_capital_name
from .config import agent_content_config

load_dotenv(override=True)

LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME")

root_agent = LlmAgent(
      model=LiteLlm(model=LLM_MODEL_NAME),
      name="capital_agent",
      generate_content_config=agent_content_config,
      description=root_agent_description1,
      instruction=root_agent_instruction1,
      tools=[get_capital_name],
)
