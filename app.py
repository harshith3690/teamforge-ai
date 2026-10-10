
import html
import streamlit as st
from graph.workflow import build_graph

st.set_page_config(
    page_title="TeamForge AI",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    #MainMenu,
    footer,
    [data-testid="stToolbar"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] {
        display: none !important;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }

    .stApp {
        background:
            radial-gradient(
                ellipse at 10% 0%,
                #19213d 0%,
                transparent 42%
            ),
            #0b0e19;
        color: #f1f5f9;
    }

    .block-container {
        max-width: 1450px;
        padding: 1.5rem 2rem 2rem;
    }

    .brand {
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.8px;
        color: #f8fafc;
        margin-bottom: 25px;
    }

    .brand span {
        color: #8b9cff;
    }

    .panel {
        background: #121827;
        border: 1px solid #29334c;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 20px;
    }

    .heading {
        font-size: 1.25rem;
        font-weight: 750;
        color: #f8fafc;
        margin-bottom: 8px;
    }

    .muted {
        color: #9ba8bf;
        font-size: 0.94rem;
        line-height: 1.7;
        margin-bottom: 0;
    }

    .stTextArea textarea {
        background: #0c1220 !important;
        color: #f1f5f9 !important;
        border: 1px solid #35415c !important;
        border-radius: 11px !important;
    }

    .stTextArea textarea:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 1px #818cf8 !important;
    }

    .stFormSubmitButton button,
    .stDownloadButton button {
        background: linear-gradient(
            100deg, #6577f5, #8b5cf6
        ) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        min-height: 46px;
        font-weight: 650;
        width: 100%;
    }

    .stFormSubmitButton button:hover,
    .stDownloadButton button:hover {
        filter: brightness(1.1);
    }

    [data-testid="stExpander"] {
        background: #111827;
        border: 1px solid #29334c;
        border-radius: 11px;
        margin-bottom: 10px;
    }

    .empty-state {
        background: rgba(18, 25, 39, 0.7);
        border: 1px dashed #35415c;
        border-radius: 18px;
        padding: 48px 22px;
        text-align: center;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .brand {
            font-size: 1.5rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="brand">✦ TeamForge <span>AI</span></div>',
    unsafe_allow_html=True,
)

if "project_result" not in st.session_state:
    st.session_state.project_result = None

if "project_goal" not in st.session_state:
    st.session_state.project_goal = ""

if "project_error" not in st.session_state:
    st.session_state.project_error = None


left, right = st.columns([0.85, 1.45], gap="large")

with left:
    st.markdown(
        """
        <div class="panel">
            <div class="heading">✦ Create a project</div>
            <p class="muted">
                Describe your idea. Your AI agents will work
                together to turn it into an actionable project plan.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("create_project_form"):
        goal = st.text_area(
            "Project description",
            value=st.session_state.project_goal,
            placeholder=(
                "Example: Build a student task management website "
                "using Python and Streamlit. Include login, task "
                "priorities, deadlines, and a progress dashboard."
            ),
            height=210,
        )

        generate = st.form_submit_button(
            "✦ Generate project deliverables",
            use_container_width=True,
        )

    if st.button("Clear project", use_container_width=True):
        st.session_state.project_result = None
        st.session_state.project_goal = ""
        st.session_state.project_error = None
        st.rerun()

if generate:
    if not goal.strip():
        st.session_state.project_error = (
            "Please enter a project description."
        )
    else:
        st.session_state.project_goal = goal.strip()
        st.session_state.project_error = None

        try:
            initial_state = {
                "goal": goal.strip(),
                "revision_count": 0,
                "feedback": "",
            }

            with st.spinner(
                "Your AI team is generating the deliverables..."
            ):
                result = build_graph().invoke(initial_state)

            st.session_state.project_result = result

        except Exception as exc:
            st.session_state.project_error = str(exc)

with right:
    st.markdown(
        """
        <div class="panel">
            <div class="heading">▤ Project output</div>
            <p class="muted">
                Your generated deliverables appear here without
                leaving the project creation screen.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.session_state.project_error:
        st.error(st.session_state.project_error)

    result = st.session_state.project_result

    if not result:
        st.markdown(
            """
            <div class="empty-state">
                <div style="font-size:2.5rem; margin-bottom:15px;">
                    ✧
                </div>
                <div style="
                    font-size:1.15rem;
                    font-weight:750;
                    color:#e2e8f0;
                    margin-bottom:12px;
                ">
                    Your project starts here
                </div>
                <div style="color:#94a3b8; line-height:1.8;">
                    Describe your idea on the left and click
                    <b>Generate project deliverables</b>.<br>
                    Your AI team's results will appear here.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        ) 
    else:
        review = result.get("review", {})
        status = review.get("status", "NOT REVIEWED")

        sections = [
            ("01 · Project Manager's Brief", "pm_plan"),
            ("02 · Research and Requirements", "research"),
            ("03 · Architecture and Plan", "plan"),
            ("04 · Developer's Proposal", "developer_output"),
        ]

        for title, key in sections:
            content = result.get(key, "")

            with st.expander(
                title,
                expanded=(key == "pm_plan"),
            ):
                if content:
                    st.markdown(content)
                else:
                    st.info(
                        "No content was generated for this section."
                    )

        with st.expander("05 · Reviewer Feedback", expanded=True):
            st.markdown(f"**Review status:** {status}")
            st.markdown(
                review.get(
                    "feedback",
                    "No reviewer feedback available.",
                )
            )

        final_output = result.get("final_output", "")

        if final_output:
            st.download_button(
                label="↓ Download project deliverables",
                data=final_output,
                file_name="teamforge_deliverables.md",
                mime="text/markdown",
                use_container_width=True,
            )
