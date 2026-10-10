
from typing import TypedDict, Any

class ProjectState(TypedDict, total=False):
    goal: str
    pm_plan: str
    research: str
    plan: str
    developer_output: str
    review: dict[str, Any]
    feedback: str
    revision_count: int
    final_output: str
