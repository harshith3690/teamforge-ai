
from agents.llm import invoke_llm

def run_developer(state: dict) -> dict:
    prompt = f"""
You are the Developer agent in TeamForge AI.

Produce a detailed implementation proposal based on the plan.
Include:
1. Key implementation steps
2. Important code or pseudocode where useful
3. Module responsibilities
4. Error handling
5. Testing recommendations

Do not claim that you created files, executed code, or tested software.
You are generating an implementation proposal only.

Project goal:
{state.get("goal", "")}

Architecture and plan:
{state.get("plan", "")}

Previous proposal, if any:
{state.get("developer_output", "No previous proposal.")}

Reviewer feedback to address:
{state.get("feedback", "No reviewer feedback yet.")}

Improve the proposal based on the reviewer feedback.
Return the complete revised proposal, not just a list of changes.
"""
    result = invoke_llm(prompt)
    return {"developer_output": result}
