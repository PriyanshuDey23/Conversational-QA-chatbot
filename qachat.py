from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai

# Load the env
load_dotenv()

# Load the api key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load  model and get reponse

model = genai.GenerativeModel(model_name="gemini-1.5-pro-002")
chat_session = model.start_chat(
  history=[]
)


def get_gemini_response(question):
    response=chat_session.send_message(question,stream=True) # stream=Display the ouputs
    return response


## Initialize Streamlit app
st.set_page_config(page_title="Q&A ChatBot")
st.header("Q&A ChatBot")

# Initialize the session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state: # Put all the chat in session state
    st.session_state['chat_history']=[]


input=st.text_input("Start the Chat",key="Input")

submit=st.button("Ask The Question")

if submit and input:
    response=get_gemini_response(input)

    # Add user query and response to session chat history
    # session_state :-  Saving
    st.session_state['chat_history'].append(("You",input)) # Storing all the session in you variable
    st.subheader("The Response is") # The output from llm will be displayed in front end screen
    for chunk in response:
        st.write(chunk.text)  # Display the text part by part
        st.session_state['chat_history'].append(("BOT",chunk.text))

# Save the history
st.header("The Chat History is")

for role,text in st.session_state['chat_history']:
    st.write(f"{role}:{text}")
    