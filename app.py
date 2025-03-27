import streamlit as st
import os
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_groq import ChatGroq
from outparser import Metrics
from functions import plot_radar_chart, career_options

# Set page configuration with icon
st.set_page_config(page_title="Spark", page_icon="Spark_Logo.png", layout="wide")

# Display the logo at the top
col1, col2, col3 = st.columns([2, 2, 1])  # Adjust column width

with col2:  # Place image in the center column
    st.image("Spark_Logo.png", width=200)

os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]
llm = ChatGroq(model='llama3-70b-8192')
# Define choices for radio button inputs
personality_options = ["Shy & Thoughtful", "Outgoing & Social", "Balanced", "Risk-Taker"]
learning_style_options = ["Visual Learner", "Hands-On Learner", "Listener", "Book Lover"]
emotional_intelligence_options = ["Empathetic Helper", "Confident Leader", "Resilient Achiever", "Team Player"]
skill_focus_options = ["Problem Solver", "Creative Thinker", "Organized Planner", "Communicator"]
work_preference_options = ["Structured Worker", "Flexible Thinker", "Research-Oriented", "Outdoor Explorer"]
values_goals_options = ["Money-Driven", "Social Changemaker", "Balanced Life", "Adventure Seeker"]

# Page Title with Emoji
st.title("Student Career Assessment Form 🎯")

with st.form("career_form"):
    col1, col2, col3 = st.columns(3)  # Create three columns for layout

    with col1:
        personality = st.radio("🧠 Personality Type:", personality_options)
        skill_focus = st.radio("🛠️ Skill Focus:", skill_focus_options)

    with col2:
        learning_style = st.radio("📖 Learning Style:", learning_style_options)
        work_preference = st.radio("💼 Work Preference:", work_preference_options)

    with col3:
        emotional_intelligence = st.radio("❤️ Emotional Intelligence:", emotional_intelligence_options)
        values_goals = st.radio("🌟 Values & Goals:", values_goals_options)

    # Text inputs for open-ended choices
    favorite_subjects = st.text_input("📚 Favorite Subjects (e.g., Math, Science, History)")
    extracurricular_activities = st.text_input("🎭 Extracurricular Activities (e.g., Sports, Coding, Music)")

    # Submit button
    submitted = st.form_submit_button("Submit ➤")

if submitted:
    all_params = f"""**🧠 Personality Type:** {personality}
                **📖 Learning Style:** {learning_style}")
                **❤️ Emotional Intelligence:** {emotional_intelligence}")
                **🛠️ Skill Focus:** {skill_focus}")
                **💼 Work Preference:** {work_preference}")
                **🌟 Values & Goals:** {values_goals}")
                **📚 Favorite Subjects:** {favorite_subjects}")
                **🎭 Extracurricular Activities:** {extracurricular_activities}"""
    parser = PydanticOutputParser(pydantic_object=Metrics)
    prompt = ChatPromptTemplate.from_template(f"""You are an expert in career guidance for school students. Based on a student's personality, learning style, emotional intelligence, skill focus, work preference, values & goals, favorite subjects, and extracurricular activities, generate 7 key metrics that best represent their skills, preferences, and tendencies.

    Each metric should be:
    - Short and meaningful for a school student
    - Quantifiable (rated between 0 and 10)
    - Relevant to career decision-making
    - Dynamically chosen based on the student's traits

    Input Parameters:
        {all_params}
    Output Format:
    Generate a JSON output with 7 dynamically chosen metrics based on the student’s inputs. The keys should be a metric and the values should be on a 0 to 10 scale, reflecting the student's strengths and areas of growth. Avoid generic terms and ensure the metrics are well-balanced across different skill domains."""+"\n\n{ins}")

    chain = prompt | llm | parser
    result = chain.invoke({"ins":parser.get_format_instructions()}).metrics
    metrics_string = "\n\n".join(f"{key}: {value}" for key, value in result.items())
    result = {key: int(value) for key, value in result.items()}
    st.subheader("Analysis 🔍📊:")
    plot_radar_chart(result)
    st.subheader("Suggested Career Options:")
    routes = career_options(metrics_string, all_params)
    # Unpack dictionary items
    col1, col2, col3 = st.columns(3)
    items = list(routes.items())
    # Display each key-value pair in a separate column
    with col1:
        st.markdown(f"### {items[0][0]}")
        st.write(items[0][1])

    with col2:
        st.markdown(f"### {items[1][0]}")
        st.write(items[1][1])

    with col3:
        st.markdown(f"### {items[2][0]}")
        st.write(items[2][1])