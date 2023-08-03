import boto3
import streamlit as st
from streamlit_chat import message
from streamlit.components.v1 import html

# Amazon Lex credentials
aws_access_key_id = ''
aws_secret_access_key = ''
region_name = 'us-west-2'

# Create a client for Amazon Lex
lex_client = boto3.client('lex-runtime', 
                        aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key,
                        region_name=region_name)

#session_state = st.session_state.get(key=0)

def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)

    #session_state.key += 1
    st.session_state["user_input"] = ""

    response = lex_client.post_text(
                botName='RealEstBot',
                botAlias='RealEstChatBot',
                userId='123',
                inputText=user_input,
                activeContexts=[
                    {
                        'name': 'string',
                        'timeToLive': {
                            'timeToLiveInSeconds': 123,
                            'turnsToLive': 4
                        },
                        'parameters': {
                            'string': 'string'
                        }
                    }
                ]
            )

    # Extract and display chatbot response
    bot_response = response['message']

    st.session_state.generated.append(bot_response)


def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

    

def render_page():
    
    # Streamlit app

    st.session_state.setdefault('past', [])
    st.session_state.setdefault('generated', [])
    #st.session_state.setdefault('key', [])

    st.title('Amazon Lex Chatbot')

    chat_placeholder = st.empty()

    with chat_placeholder.container():    
        for i in range(len(st.session_state['generated'])):                
            message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
            message(
                st.session_state['generated'][i], 
                key=f"{i}", 
                allow_html=True,
                is_table=False
            )
        
        st.button("Clear message", on_click=on_btn_click)

    with st.container():
        st.text_input("User Input:", on_change=on_input_change, key='user_input')
