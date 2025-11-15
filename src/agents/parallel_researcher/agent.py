 # Part of agent.py --> Follow https://google.github.io/adk-docs/get-started/quickstart/ to learn the setup
import logging

from google.adk.agents.llm_agent import LlmAgent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import google_search
from google.adk.agents import SequentialAgent, ParallelAgent
from .constants import LLM_MODEL_NAME
from .instruction import (
    instr_researcher_renewable_agent,
    desc_researcher_renewable_agent,
    instr_transport_researcher_agent,
    desc_transport_researcher_agent,
    instr_carbon_research_agent,
    desc_carbon_research_agent,
    desc_parallel_reasearcher_agent,
    instr_synthesizer_agent,
    desc_synthesizer_agent,
    desc_seq_merger_agent,
)


def _google_search_supported(model_name: str | None) -> bool:
    """ADK google_search tool only works for select hosted models, so skip for local Ollama."""
    if not model_name:
        return True
    return not model_name.lower().startswith("ollama")


if _google_search_supported(LLM_MODEL_NAME):
    researcher_tools = [google_search]
else:
    logging.warning(
        "parallel_researcher: google_search disabled for model %s", LLM_MODEL_NAME
    )
    researcher_tools = []
 # --- 1. Define Researcher Sub-Agents (to run in parallel) ---

 # Researcher 1: Renewable Energy
researcher_agent_1 = LlmAgent(
     name="RenewableEnergyResearcher",
     model=LiteLlm(model=LLM_MODEL_NAME),
     instruction=instr_researcher_renewable_agent,
     description=desc_researcher_renewable_agent,
     tools=researcher_tools,
     output_key="renewable_energy_result"
 )

 # Researcher 2: Electric Vehicles
researcher_agent_2 = LlmAgent(
     name="EVResearcher",
     model=LiteLlm(model=LLM_MODEL_NAME),
     instruction=instr_transport_researcher_agent,
     description=desc_transport_researcher_agent,
     tools=researcher_tools,
     output_key="ev_technology_result"
 )

 # Researcher 3: Carbon Capture
researcher_agent_3 = LlmAgent(
     name="CarbonCaptureResearcher",
     model=LiteLlm(model=LLM_MODEL_NAME),
     instruction=instr_carbon_research_agent,
     description=desc_carbon_research_agent,
     tools=researcher_tools,
     output_key="carbon_capture_result"
 )

 # --- 2. Create the ParallelAgent (Runs researchers concurrently) ---
 # This agent orchestrates the concurrent execution of the researchers.
 # It finishes once all researchers have completed and stored their results in state.
parallel_research_agent = ParallelAgent(
     name="ParallelWebResearchAgent",
     sub_agents=[researcher_agent_1, researcher_agent_2, researcher_agent_3],
     description=desc_parallel_reasearcher_agent
 )

 # --- 3. Define the Merger Agent (Runs *after* the parallel agents) ---
 # This agent takes the results stored in the session state by the parallel agents
 # and synthesizes them into a single, structured response with attributions.
merger_agent = LlmAgent(
     name="SynthesisAgent",
     model=LiteLlm(model=LLM_MODEL_NAME),  # Or potentially a more powerful model if needed for synthesis
     instruction=instr_synthesizer_agent,
     description=desc_synthesizer_agent,
 )


 # --- 4. Create the SequentialAgent (Orchestrates the overall flow) ---
 # This is the main agent that will be run. It first executes the ParallelAgent
 # to populate the state, and then executes the MergerAgent to produce the final output.
sequential_pipeline_agent = SequentialAgent(
     name="ResearchAndSynthesisPipeline",
     # Run parallel research first, then merge
     sub_agents=[parallel_research_agent, merger_agent],
     description=desc_seq_merger_agent
 )

root_agent = sequential_pipeline_agent
