from src.langgraphagenticai.state.state import State
import streamlit as st 
from langchain_core.messages import HumanMessage, AIMessage
from src.langgraphagenticai.appConfig import MAX_HISTORY_LENGTH

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    def __init__(self,model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response with tool integration
        """
        user_input = state["messages"][-1] if state["messages"] else ""

        # Ensure chat history is initialized in session state
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Append latest user input to chat history
        st.session_state.chat_history.append(HumanMessage(content=str(user_input))) 

        # Generate LLM response
        response = self.llm.invoke(st.session_state.chat_history)

        # Store LLM response in session history
        st.session_state.chat_history.append(AIMessage(content=str(response.content))) 

        # Trim history if it exceeds the limit
        if len(st.session_state.chat_history) > MAX_HISTORY_LENGTH:
            st.session_state.chat_history = st.session_state.chat_history[-MAX_HISTORY_LENGTH:]

        # Simulate tool-specific logic
        tools_response = f"Tool integration for: '{user_input}'"

        return {"messages": [response, tools_response]}
    
    def create_chatbot(self, tools):
        """
        Returns a chatbot node function.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chatbot_node(state: State):
            """
            Chatbot logic for processing the input state and returning a response.
            """
            user_input = state["messages"][-1] if state["messages"] else ""

            # Ensure chat history is initialized
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            # Append user input to history
            st.session_state.chat_history.append(HumanMessage(content=str(user_input)))

            # Invoke LLM with full chat history
            response = llm_with_tools.invoke(st.session_state.chat_history)

            # Append response to history
            st.session_state.chat_history.append(AIMessage(content=str(response.content)))

            # Trim history if it exceeds the limit
            if len(st.session_state.chat_history) > MAX_HISTORY_LENGTH:
                st.session_state.chat_history = st.session_state.chat_history[-MAX_HISTORY_LENGTH:]
                
            return {"messages": [response]}
           #return {"messages": [llm_with_tools.invoke(state["messages"])]}

        return chatbot_node
 
        

        
    
    
    
    
    
