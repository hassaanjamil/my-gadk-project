from src.config import LLM_MODEL_NAME
from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from src.instructions import root_agent_description1, root_agent_instruction1
from src.tools import get_capital_name

root_agent = LlmAgent(
      model=LiteLlm(model=LLM_MODEL_NAME),
      name="capital_agent",
      description=root_agent_description1,
      instruction=root_agent_instruction1,
      tools=[get_capital_name]
    # instruction and tools will be added next
)
