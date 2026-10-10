
from agents.llm import invoke_llm

def run_researcher(state: dict) -> dict:
    prompt = f"""
You are the Researcher agent in TeamForge AI.

Analyze the project requirements and identify:
1. Technical requirements
2. Suitable technologies
3. Constraints and assumptions
4. Potential risks
5. Important implementation considerations

Do not claim you performed live web research.
Base your analysis on your existing knowledge and the supplied project brief.

Project goal:
{state.get("goal", "")}

Project Manager's brief:
{state.get("pm_plan", "")}

Return a practical technical research report.
"""
    result = invoke_llm(prompt)
    return {"research": result}
