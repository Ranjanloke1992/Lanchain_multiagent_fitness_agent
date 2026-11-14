"""Streamlit UI for Self_dev/Langchain multi-agent fitness pipeline.

Run from the Langchain project root:
    python -m streamlit run app.py

Requires pipeline.run_research_pipeline(...) to return a dict with:
    analyse_results, exercise_results, diet_results, sleep_results, report
and pipeline.py to call writer_chain.invoke(...) for report creation.
"""

import contextlib
import io
import traceback

import streamlit as st
from dotenv import load_dotenv

from src.agents.pipeline import run_research_pipeline

load_dotenv()
st.set_page_config(page_title="AI Fitness & Wellness Planner", page_icon="💪", layout="wide")

st.title("💪 AI Fitness & Wellness Planner")
st.caption("Analysis → Exercise → Diet → Sleep & Stress → Final Report")
st.info("AI-generated wellness information is educational and may need review by a qualified professional, especially for injuries or medical conditions.")

with st.form("fitness_profile"):
    st.subheader("Personal details")
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Name", value="John Doe")
        age = st.number_input("Age (years)", min_value=13, max_value=110, value=30)
        gender = st.selectbox("Gender", ["Male", "Female", "Non-binary", "Prefer not to say"])
    with col2:
        height = st.text_input("Height", value="5'10\"")
        weight = st.number_input("Weight (kg)", min_value=20.0, max_value=350.0, value=80.0, step=0.5)
        muscle_fat = st.text_input("Muscle / body fat information (optional)", value="Unknown")
    with col3:
        fitness_goal = st.text_area("Fitness goal", value="Build muscle and reduce fat")
        cuisine = st.text_input("Preferred cuisine", value="Indian - North Indian")
        restrictions = st.text_input("Dietary restrictions", value="Lactose intolerant")

    st.subheader("Lifestyle & recovery")
    left, right = st.columns(2)
    with left:
        sleep = st.text_input("Sleep patterns", value="Average 6 hours per night")
        lifestyle = st.text_input("Lifestyle", value="Sedentary job, active on weekends")
    with right:
        conditions = st.text_area("Medical conditions or injuries (optional)", value="None")
        motivation = st.selectbox("Motivation level", ["High", "Medium", "Low"])

    submitted = st.form_submit_button("Generate fitness report", type="primary", use_container_width=True)

if submitted:
    if not name.strip() or not fitness_goal.strip():
        st.error("Enter a name and fitness goal.")
    else:
        user_info = {
            "Name": name.strip(),
            "Age": age,
            "Gender": gender,
            "Height": height,
            "Weight": f"{weight:g} kg",
            "Muscle to Fat Ratio": muscle_fat or "Unknown",
            "Fitness Goal": fitness_goal.strip(),
            "Preferred Cuisine": cuisine,
            "Dietary Restrictions": restrictions,
            "Sleep Patterns": sleep,
            "Medical Conditions or Injuries": conditions or "Not provided",
            "Lifestyle": lifestyle,
            "Motivation Level": motivation,
        }
        user_info_str = "\n".join(f"{key}: {value}" for key, value in user_info.items())
        logs = io.StringIO()
        try:
            with st.spinner("Running your agents and drafting the report (may incur API charges)..."):
                with contextlib.redirect_stdout(logs):
                    result = run_research_pipeline(user_info_str)
            if not isinstance(result, dict):
                raise TypeError("Pipeline must return a dictionary containing the 'report' field.")
            report = result.get("report")
            if not isinstance(report, str):
                raise TypeError(
                    "Pipeline 'report' must be plain text. In pipeline.py, import writer_chain "
                    "and set state['report'] = writer_chain.invoke({...}), not writer_prompt.invoke({...})."
                )
            st.session_state["fitness_result"] = result
            st.session_state["fitness_logs"] = logs.getvalue()
        except Exception as exc:
            st.error(f"Unable to generate report: {type(exc).__name__}: {exc}")
            with st.expander("Technical details"):
                st.code(traceback.format_exc(), language="text")
                st.code(logs.getvalue() or "No agent console output", language="text")

if "fitness_result" in st.session_state:
    result = st.session_state["fitness_result"]
    st.success("Fitness report generated successfully")
    tab_report, tab_analysis, tab_exercise, tab_diet, tab_sleep = st.tabs(
        ["📋 Final Report", "🔎 Analysis", "🏋️ Exercise", "🥗 Diet", "🌙 Sleep & Stress"]
    )
    with tab_report:
        st.markdown(result["report"])
        st.download_button(
            "Download final report (.md)",
            data=result["report"],
            file_name="fitness_report.md",
            mime="text/markdown",
        )
    with tab_analysis:
        st.markdown(str(result.get("analyse_results", "No analysis returned")))
    with tab_exercise:
        st.markdown(str(result.get("exercise_results", "No exercise recommendations returned")))
    with tab_diet:
        st.markdown(str(result.get("diet_results", "No diet recommendations returned")))
    with tab_sleep:
        st.markdown(str(result.get("sleep_results", "No sleep recommendations returned")))
    with st.expander("Agent execution logs"):
        st.code(st.session_state.get("fitness_logs", "No logs"), language="text")
