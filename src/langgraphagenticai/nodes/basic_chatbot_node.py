from src.langgraphagenticai.state.state import State
import streamlit as st  
from langchain_core.messages import HumanMessage, AIMessage  
from src.langgraphagenticai.appConfig import MAX_HISTORY_LENGTH


class BasicChatbotNode:
    """
    Basic chatbot logic implementation.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a chatbot response.
        """

        # Ensure chat history is initialized
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []  # Initialize as an empty list  

        messages = state["messages"]

        # Retrieve chat history if available
        messages = st.session_state.chat_history + [HumanMessage(content=state["messages"][-1].content)]

        response = self.llm.invoke(messages)

        # Store response in session state
        st.session_state.chat_history.append(AIMessage(content=response.content))

        # Trim history if it exceeds the limit
        if len(st.session_state.chat_history) > MAX_HISTORY_LENGTH:
            st.session_state.chat_history = st.session_state.chat_history[-MAX_HISTORY_LENGTH:]

        return {"messages": response}
    
        #return {"messages":self.llm.invoke(state['messages'])}