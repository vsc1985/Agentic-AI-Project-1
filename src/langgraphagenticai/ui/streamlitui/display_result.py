import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage
import json
from langchain_core.messages import ToolMessage


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        ##  config={"configurable":{"thread_id":"1"}}   ## Dit not work as expected.

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if usecase =="Basic Chatbot":
                for event in graph.stream({'messages':("user",user_message)}): ##,config):
                    print(event.values())
                    for value in event.values():
                        response_text = value["messages"].content
                        ##print(value['messages'])

                        # Store messages in session state
                        st.session_state.chat_history.append(HumanMessage(content=user_message))
                        st.session_state.chat_history.append(AIMessage(content=response_text))

                        with st.chat_message("user"):
                            st.write(user_message)
                        with st.chat_message("assistant"):
                            st.write(value["messages"].content)

        elif usecase=="Chatbot with Tool":
            # Add user input to chat history before invoking graph
            st.session_state.chat_history.append(HumanMessage(content=user_message))

            # Invoke the graph with full history
            initial_state = {"messages": st.session_state.chat_history}
            res = graph.invoke(initial_state)

            for message in res['messages']:
                if isinstance(message, HumanMessage):
                    with st.chat_message("user"):
                        st.write(message.content)
                elif isinstance(message, ToolMessage):
                    with st.chat_message("ai"):
                        st.write("Tool Call Start")
                        st.write(message.content)
                        st.write("Tool Call End")
                elif isinstance(message, AIMessage) and message.content:
                    with st.chat_message("assistant"):
                        st.write(message.content)
                    # Append AI response to chat history
                    st.session_state.chat_history.append(AIMessage(content=message.content))


            #  # Prepare state and invoke the graph
            # initial_state = {"messages": [user_message]}
            # res = graph.invoke(initial_state)
            # for message in res['messages']:
            #     if type(message) == HumanMessage:
            #         with st.chat_message("user"):
            #             st.write(message.content)
            #     elif type(message)==ToolMessage:
            #         with st.chat_message("ai"):
            #             st.write("Tool Call Start")
            #             st.write(message.content)
            #             st.write("Tool Call End")
            #     elif type(message)==AIMessage and message.content:
            #         with st.chat_message("assistant"):
            #             st.write(message.content)