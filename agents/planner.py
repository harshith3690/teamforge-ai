
from agents.llm import invoke_llm

def run_planner(state: dict) -> dict:
    prompt = f"""
You are the Planning and Design agent in TeamForge AI.

Create an implementation plan containing:
1. System architecture
2. Components and their responsibilities
3. Data flow
4. Suggested folder structure
5. Development milestones
6. Testing strategy

Project goal:
{state.get("goal", "")}

Project brief:
{state.get("pm_plan", "")}

Research:
{state.get("research", "")}

Make the plan practical for a small development team.
"""
    result = invoke_llm(prompt)
    return {"plan": result}
