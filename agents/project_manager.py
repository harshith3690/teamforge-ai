
from agents.llm import invoke_llm

def run_project_manager(state: dict) -> dict:
    prompt = f"""
You are the Project Manager agent in TeamForge AI.

Analyze the user's project goal and produce:
1. Project objectives
2. Main features
3. Task breakdown
4. Deliverables
5. Dependencies
6. Success criteria

Project goal:
{state.get("goal", "")}

Return a clear, structured project brief.
"""
    result = invoke_llm(prompt)
    return {"pm_plan": result}
