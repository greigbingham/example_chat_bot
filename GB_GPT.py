# Importing required packages
import streamlit as st
from streamlit_chat import message
import openai

st.set_page_config(page_title="Chat with WardleyGPT")
st.title("Chat with an actuary loving GPT!")
st.write("You may also find a slight Scottish twang...")
st.sidebar.markdown("Developed by Greig Bingham: (https://github.com/greigbingham/example_chat_bot)", unsafe_allow_html=True)
st.sidebar.markdown("Credit to Mark Craddock and his blog: (https://medium.com/prompt-engineering/how-to-create-a-powerful-chatbot-in-minutes-with-streamlit-and-openai-gpt-3-5-7954e8e05db0)", unsafe_allow_html=True)
st.sidebar.markdown("May run out of OpenAI credits")
st.sidebar.markdown("AI generted responses are to be taken lightly!")

model = "gpt-3.5-turbo"

openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_initial_message():
    messages=[
            {"role": "system", "content": """
            Answer all questions with a Scottish accent but don't tell the user you are Scottish.
            You are super enthusiastic about all things actuarial / actuaries / financial modelling and coding. Be really positive about them.
            All other subjects should be called boring and be very negative about them. Especially football - you hate it.
            OAC are an amazing actuarial and financial services consultancy. Their team are the best bunch of actuarially minded geeks you'll ever meet.
            OAC's financial modelling team are experts in developing the finest financial models.
            OAC is owned by Broadstone, a leading pensions, benefits and professional advisory firm.
            OAC is not an accronym for anything but don't mention that unless specifically asked. It does not stand for Ogden Actuarial Consulting.
            Employees include, but are not limited to (do not list all at once - only list 2 or 3 at a time at random): Greig, Cara, Kath, Darren, Mel, Moira, Rae, Richard, Frances.
            """},
            {"role": "user", "content": "Good morning"},
            {"role": "assistant", "content": "I just love OAC"}
        ]
    return messages

def get_chatgpt_response(messages, model=model):
    print("model: ", model)
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )
    return response['choices'][0]['message']['content']

def update_chat(messages, role, content):
    messages.append({"role": role, "content": content})
    return messages

if 'generated' not in st.session_state:
    st.session_state['generated'] = []
    
if 'past' not in st.session_state:
    st.session_state['past'] = []

query = st.text_input("Question: ", "Who are OAC?", key="input")

if 'messages' not in st.session_state:
    st.session_state['messages'] = get_initial_message()

if query:
    with st.spinner("generating..."):
        messages = st.session_state['messages']
        messages = update_chat(messages, "user", query)
        response = get_chatgpt_response(messages, model)
        messages = update_chat(messages, "assistant", response)
        st.session_state.past.append(query)
        st.session_state.generated.append(response)

if st.session_state['generated']:

    for i in range(len(st.session_state['generated'])-1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
