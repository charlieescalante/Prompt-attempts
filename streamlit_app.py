import streamlit as st
from prompts import (
    get_overview_prompt,
    get_earliest_records_prompt,
    get_historical_periods_prompt,
    get_modern_history_prompt,
    get_landmarks_prompt,
    get_conclusion_prompt,
)
import openai

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_Key"]

# Function to query the LLM
def query_llm(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Streamlit app
st.title("Interactive Historical Tour Guide")
st.sidebar.title("Tour Guide Prompts")

# Location input
location = st.text_input("Enter the location for the historical tour:")

# Prompt options
options = [
    "Overview of the Area",
    "Earliest Known Records",
    "Development Through Key Historical Periods",
    "Modern History",
    "Key Sites or Landmarks",
    "Conclusion for the Tour",
]
choice = st.sidebar.radio("Choose a section of the tour:", options)

# Period input for historical periods
period = ""
if choice == "Development Through Key Historical Periods":
    period = st.text_input("Enter the historical period to focus on (e.g., 'Medieval Era'):")    

# Generate prompt
if st.button("Generate Response"):
    if not location:
        st.error("Please enter a location.")
    else:
        if choice == "Overview of the Area":
            prompt = get_overview_prompt(location)
        elif choice == "Earliest Known Records":
            prompt = get_earliest_records_prompt(location)
        elif choice == "Development Through Key Historical Periods" and period:
            prompt = get_historical_periods_prompt(location, period)
        elif choice == "Modern History":
            prompt = get_modern_history_prompt(location)
        elif choice == "Key Sites or Landmarks":
            prompt = get_landmarks_prompt(location)
        elif choice == "Conclusion for the Tour":
            prompt = get_conclusion_prompt(location)
        else:
            st.error("Please provide additional details for this section.")
            prompt = None

        if prompt:
            with st.spinner("Generating response..."):
                response = query_llm(prompt)
                st.text_area("Response from the Tour Guide:", response, height=300)
