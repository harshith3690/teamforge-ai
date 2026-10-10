
from graph.workflow import build_graph

def main():
    print("=" * 60)
    print("TEAMFORGE AI — Local Multi-Agent Project Manager")
    print("=" * 60)

    goal = input("\nDescribe your project: ").strip()

    if not goal:
        print("Please enter a project goal.")
        return

    initial_state = {
        "goal": goal,
        "revision_count": 0,
        "feedback": "",
    }

    print("\nRunning the local AI agents. Please wait...\n")

    try:
        result = build_graph().invoke(initial_state)
        print(result.get("final_output", "No output was generated."))
    except Exception as exc:
        print(f"\nWorkflow failed: {exc}")
        print(
            "\nCheck that Ollama is running, the model is downloaded, "
            "and your Python dependencies are installed."
        )

if __name__ == "__main__":
    main()
