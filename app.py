from itertools import zip_longest
import streamlit as st
from streamlit_chat import message
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
openai_key = st.secrets['OPENAI_KEY']

# Configure streamlit app page title, title and text
st.set_page_config(page_title="AI Chatbot")
st.title("Custom AI Chatbot")
st.write("You can ask questions related to AI from this chatbot.")

# Define initial states and assign values
initialStates = {
    'generated': [],
    'past': [],
    'entered_prompt': ''
}

for key, value in initialStates.items():
    if key not in st.session_state:
        st.session_state[key] = value


# Define LLM (Large Language Model / OpenAI) object
chat = ChatOpenAI(temperature=0.5, model='gpt-3.5-turbo',
                  max_tokens=100, openai_api_key=openai_key)


# Create a messages list
# You can consider it a prompt which we will give to the LLM
def messages_list():
    instructions = """your name is AI Mentor. You are an AI Technical Expert for Artificial Intelligence, here to guide and assist students with their AI-related questions and concerns. Please provide accurate and helpful information, and always maintain a polite and professional tone.

                1. Greet the user politely ask user name and ask how you can assist them with AI-related queries.
                2. Provide informative and relevant responses to questions about artificial intelligence, machine learning, deep learning, natural language processing, computer vision, and related topics.
                3. you must Avoid discussing sensitive, offensive, or harmful content. Refrain from engaging in any form of discrimination, harassment, or inappropriate behavior.
                4. If the user asks about a topic unrelated to AI, politely steer the conversation back to AI or inform them that the topic is outside the scope of this conversation.
                5. Be patient and considerate when responding to user queries, and provide clear explanations.
                6. If the user expresses gratitude or indicates the end of the conversation, respond with a polite farewell.
                7. Do Not generate the long paragarphs in response. Maximum Words should be 100.

                Remember, your primary goal is to assist and educate students in the field of Artificial Intelligence. Always prioritize their learning experience and well-being."""

    zip_messages = [SystemMessage(content=instructions)]

    # Append 'past' and 'generated' session values to zip_messages, if existed
    for h_m, a_m in zip_longest(st.session_state['past'], st.session_state['generated']):
        if h_m:
            zip_messages.append(HumanMessage(content=h_m))
        if a_m:
            zip_messages.append(AIMessage(content=a_m))

    return zip_messages


# Generate the response from LLM
def generate_response():
    output = chat(messages_list())
    return output.content


# Define submit function and input field
def submit():
    st.session_state.entered_prompt = st.session_state.input_prompt
    st.session_state.input_prompt = ''


st.text_input("Enter Prompt", key="input_prompt", on_change=submit)


# Check if 'entered_prompt' is empty or not
if st.session_state.entered_prompt != "":
    st.session_state['past'].append(st.session_state.entered_prompt)
    st.session_state['generated'].append(generate_response())

# Display Messages
if st.session_state['generated']:
    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state['generated'][i], key=str(i))
        message(st.session_state['past'][i],
                is_user=True, key=f"{str(i)}_user")
