import streamlit as st
from chatbot import chatbot
from langchain_core.messages import HumanMessage

config = {
    "configurable": {
        "thread_id": "waris"
    }
}
if 'message_history' not in st.session_state:
    st.session_state['message_history']=[]


#print old messages
for messages in st.session_state['message_history']:
    with st.chat_message(messages['role']):
        st.write(messages['content'])

user_message = st.chat_input("What do you want to ask?")
if user_message:
    st.session_state['message_history'].append({
        "role":"user","content":user_message
    })

    with st.chat_message("user"):
        st.write(user_message)


    #now get the streaming reposne form ai and append them into the message history
    with st.chat_message("assistant"):
        ai_response=st.write_stream(
        message_chunk.content for message_chunk,metadata in chatbot.stream(
            {"messages":[HumanMessage(content=user_message)]},
            config=config,
            stream_mode="messages"
        )
    )

    st.session_state['message_history'].append({
        "role":"assistant","content":ai_response
    })