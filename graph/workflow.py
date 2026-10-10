
from langgraph.graph import StateGraph, END

from graph.state import ProjectState
from config import MAX_REVISIONS

from agents.project_manager import run_project_manager
from agents.researcher import run_researcher
from agents.planner import run_planner
from agents.developer import run_developer
from agents.reviewer import run_reviewer


def finalize_project(state: ProjectState) -> dict:
    review = state.get("review", {})
    status = review.get("status", "NOT REVIEWED")

    final_output = f"""
# TeamForge AI — Project Deliverables

## Project Goal
{state.get("goal", "")}

## 1. Project Manager's Brief
{state.get("pm_plan", "")}

## 2. Research and Requirements
{state.get("research", "")}

## 3. Architecture and Implementation Plan
{state.get("plan", "")}

## 4. Developer's Proposal
{state.get("developer_output", "")}

## 5. Quality Review
Status: {status}

Feedback:
{review.get("feedback", "No feedback available.")}

## Workflow Summary
Revision rounds used: {state.get("revision_count", 0)}

Note: These are AI-generated planning deliverables. The workflow has not
automatically created or executed a software project.
"""
    return {"final_output": final_output}


def route_after_review(state: ProjectState) -> str:
    review = state.get("review", {})
    revision_count = state.get("revision_count", 0)

    if (
        review.get("status") == "REVISE"
        and revision_count <= MAX_REVISIONS
    ):
        return "developer"

    return "finalize"


def build_graph():
    workflow = StateGraph(ProjectState)

    workflow.add_node("project_manager", run_project_manager)
    workflow.add_node("researcher", run_researcher)
    workflow.add_node("planner", run_planner)
    workflow.add_node("developer", run_developer)
    workflow.add_node("reviewer", run_reviewer)
    workflow.add_node("finalize", finalize_project)

    workflow.set_entry_point("project_manager")

    workflow.add_edge("project_manager", "researcher")
    workflow.add_edge("researcher", "planner")
    workflow.add_edge("planner", "developer")
    workflow.add_edge("developer", "reviewer")

    workflow.add_conditional_edges(
        "reviewer",
        route_after_review,
        {
            "developer": "developer",
            "finalize": "finalize",
        },
    )

    workflow.add_edge("finalize", END)

    return workflow.compile()
