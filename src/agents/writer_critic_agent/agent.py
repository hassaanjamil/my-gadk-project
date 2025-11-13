# Part of agent.py --> Follow https://google.github.io/adk-docs/get-started/quickstart/ to learn the setup
from .constants import (
    LLM_MODEL_NAME,
    STATE_CURRENT_DOC,
    STATE_CRITICISM,
    STATE_INITIAL_TOPIC
 )
from google.adk.agents import LoopAgent, LlmAgent, SequentialAgent
from google.adk.models.lite_llm import LiteLlm
from .tools import exit_loop
from .instruction import (
    instruction_writer_agent,
    description_writer_agent,
    instruction_critic_agent,
    description_critic_agent,
    instruction_refiner_agent,
    description_refiner_agent,
)

# --- Constants ---
print('Contants created.')

# --- Tool Definition ---
print('Tools generated.')

# --- Agent Definitions ---

# STEP 1: Initial Writer Agent (Runs ONCE at the beginning)
initial_writer_agent = LlmAgent(
    name="InitialWriterAgent",
    model=LiteLlm(model=LLM_MODEL_NAME),
    include_contents='none',
    # MODIFIED Instruction: Ask for a slightly more developed start
    instruction=instruction_writer_agent,
    description=description_writer_agent,
    output_key=STATE_CURRENT_DOC
)

# STEP 2a: Critic Agent (Inside the Refinement Loop)
critic_agent_in_loop = LlmAgent(
    name="CriticAgent",
    model=LiteLlm(model=LLM_MODEL_NAME),
    include_contents='none',
    # MODIFIED Instruction: More nuanced completion criteria, look for clear improvement paths.
    instruction=instruction_critic_agent,
    description=description_critic_agent,
    output_key=STATE_CRITICISM
)


# STEP 2b: Refiner/Exiter Agent (Inside the Refinement Loop)
refiner_agent_in_loop = LlmAgent(
    name="RefinerAgent",
    model=LiteLlm(model=LLM_MODEL_NAME),
    # Relies solely on state via placeholders
    include_contents='none',
    instruction=instruction_refiner_agent,
    description=description_refiner_agent,
    tools=[exit_loop], # Provide the exit_loop tool
    output_key=STATE_CURRENT_DOC # Overwrites state['current_document'] with the refined version
)


# STEP 2: Refinement Loop Agent
refinement_loop = LoopAgent(
    name="RefinementLoop",
    # Agent order is crucial: Critique first, then Refine/Exit
    sub_agents=[
        critic_agent_in_loop,
        refiner_agent_in_loop,
    ],
    max_iterations=5 # Limit loops
)

# STEP 3: Overall Sequential Pipeline
# For ADK tools compatibility, the root agent must be named `root_agent`
root_agent = SequentialAgent(
    name="IterativeWritingPipeline",
    sub_agents=[
        initial_writer_agent, # Run first to create initial doc
        refinement_loop       # Then run the critique/refine loop
    ],
    description="Writes an initial document and then iteratively refines it with critique using an exit tool."
)