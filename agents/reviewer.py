
from agents.llm import invoke_llm

def run_reviewer(state: dict) -> dict:
    prompt = f"""
You are the Quality Reviewer agent in TeamForge AI.

Review the developer's proposal for:
- Alignment with the project goal
- Completeness
- Technical consistency
- Risks and missing requirements
- Practicality

Project goal:
{state.get("goal", "")}

Plan:
{state.get("plan", "")}

Developer proposal:
{state.get("developer_output", "")}

Return your answer in exactly this format:

STATUS: PASS
FEEDBACK: The proposal meets the requirements.

Use STATUS: PASS only if the proposal is sufficiently complete.
Otherwise use STATUS: REVISE and provide specific actionable feedback.
The STATUS must be either PASS or REVISE.
"""
    result = invoke_llm(prompt)

    status = "REVISE"
    feedback = result.strip()

    for line in result.splitlines():
        if line.strip().upper() == "STATUS: PASS":
            status = "PASS"
        elif line.strip().upper() == "STATUS: REVISE":
            status = "REVISE"

    for line in result.splitlines():
        if line.strip().upper().startswith("FEEDBACK:"):
            feedback = line.split(":", 1)[1].strip()
            break

    current_count = int(state.get("revision_count", 0))
    new_count = current_count + 1 if status == "REVISE" else current_count

    return {
        "review": {
            "status": status,
            "feedback": feedback,
            "full_response": result,
        },
        "feedback": feedback,
        "revision_count": new_count,
    }
