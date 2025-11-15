import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from outparser import Options

def plot_radar_chart(data):
    labels = list(data.keys())
    values = list(data.values())

    # Ensure the plot is circular by repeating the first value at the end
    values += values[:1]
    num_vars = len(labels)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(2, 2), subplot_kw=dict(polar=True))

    ax.fill(angles, values, color='blue', alpha=0.3)
    ax.plot(angles, values, color='blue', linewidth=2)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=4)

    # Set y-axis limits
    ax.set_ylim(0, 10)

    # Remove y-axis labels
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_yticklabels([])  # Remove y-axis labels

    st.pyplot(fig)

def career_options(metrics, first):
    parser = PydanticOutputParser(pydantic_object=Options)
    prompt = ChatPromptTemplate.from_template(f"""You are an expert career counselor for school students. Based on a student's unique strengths, interests, and tendencies, determine the 3 most viable career options for them.

    You will receive key metrics as input, representing different aspects of the student's personality, skills, preferences and extra-curricular activites.

    Input Parameters:
    {first}\n\n
    {metrics}
    
    Output Requirements:
    Suggest 3 career options that best fit the student's strengths.
    Provide a reason for each career choice based on the given metrics.
    Output in a JSON with each career option as a key and the reason as value."""+"\n\n{ins}")
    llm = ChatGroq(model="llama-3.3-70b-versatile")
    chain = prompt | llm | parser
    result = chain.invoke({"ins":parser.get_format_instructions()}).options
    return result
