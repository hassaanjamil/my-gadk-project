from google.genai.types import ThinkingConfig
from google.adk.planners import BuiltInPlanner

thinking_config = ThinkingConfig(
    include_thoughts=True,   # Ask the model to include its thoughts in the response
    thinking_budget=256      # Limit the 'thinking' to 256 tokens (adjust as needed)
)

planner = BuiltInPlanner(
    thinking_config=thinking_config
)