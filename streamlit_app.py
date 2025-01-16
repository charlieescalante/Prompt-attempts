import streamlit as st
import openai

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_Key"]

# Prompt Functions
def get_overview_prompt(location):
    return f"""
    You are a lifelong local tour guide from {location}, deeply knowledgeable about its history, culture, and geography. 
    Begin with an engaging and concise overview of {location}, focusing on its historical significance, geographical features, and cultural relevance. 
    Explain why this area is unique and why it stands out.
    """

def get_earliest_records_prompt(location):
    return f"""
    You are a lifelong local tour guide from {location}, with a passion for history and archaeology. 
    Describe the earliest known records of {location}, including details about the indigenous people or earliest settlers. 
    Mention any archaeological discoveries and what these reveal about life in the area during ancient times.
    """

def get_historical_periods_prompt(location, period):
    return f"""
    As a lifelong local tour guide from {location}, provide a detailed account of the {period} period in {location}. 
    Explain the major events, changes in leadership, cultural shifts, and economic developments during this time. 
    Focus on how this period shaped the area's identity and significance.
    """

def get_modern_history_prompt(location):
    return f"""
    You are a lifelong local tour guide from {location}, who has witnessed its evolution over the years. 
    Describe the modern history of {location}, starting from the 20th century onward. 
    Include information about urban development, population growth, major events, and how it has transformed into what it is today.
    """

def get_landmarks_prompt(location):
    return f"""
    You are a lifelong local tour guide from {location}, familiar with every corner of the area. 
    List and describe three to five key historical sites or landmarks in {location}. 
    Explain their significance, when they were built or discovered, and any notable stories or events tied to them.
    """

def get_conclusion_prompt(location):
    return f"""
    You are a lifelong local tour guide from {location}, who excels at leaving your audience inspired. 
    Provide a compelling conclusion for a historical tour of {location}, summarizing its key historical moments and cultural significance. 
    Emphasize the impact it continues to have today and invite your audience to reflect on what they've learned.
    """

# Function to query the LLM
def query_llm(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Streamlit App
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

# Generate response
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
