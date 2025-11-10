from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from src.instructions import root_agent_description1, root_agent_instruction1
from src.tools import get_capital_name
from src.config import agent_content_config
import os

load_dotenv(override=True)

root_agent = LlmAgent(
      model=LiteLlm(model=os.getenv("LLM_MODEL_NAME")),
      name="capital_agent",
      generate_content_config=agent_content_config,
      description=root_agent_description1,
      instruction=root_agent_instruction1,
      tools=[get_capital_name],
)
