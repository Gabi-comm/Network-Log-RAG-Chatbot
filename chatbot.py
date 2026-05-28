import streamlit as st
import ollama
from retriever import retrieve_corporate_context

st.set_page_config(page_title="SOC AI Assistant",)
st.title("Rivan AI Assistant")
st.caption("Powered by Local RAG (ChromaDB) and Secure SLMs (Ollama)")
st.divider()


# put your system prompt here :)) 

SYSTEM_PROMPT = """
You are a highly secure, strict Tier 1 SOC (Security Operations Center) Analyst Assistant for ACME Corp.
Your job is to analyze the provided security and network logs to answer the user's questions.

CRITICAL RULES:
1. You must ONLY base your answers on the provided log context. 
2. If the answer cannot be found in the provided logs, you must reply: "I do not have authorization or data to answer this."
3. Do not make up IP addresses, usernames, or ticket numbers (No Hallucinations).
4. If a log mentions "[SSN_REDACTED]" or "[EMAIL_REDACTED]", you must explicitly state in your answer that the data was safely redacted by the DLP system.
"""

#session state management --memoryy
# 'messages' holds the actual data sent to Ollama includes hidden logs
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# 'display_messages' holds only what we want the human user to see on screen
if "display_messages" not in st.session_state:
    st.session_state.display_messages = []

# render the chat history on the screen
for msg in st.session_state.display_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


if user_query := st.chat_input("Ask a question about the security logs..."):
    

    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.display_messages.append({"role": "user", "content": user_query})

    #RAG INTEGRATION - fetches the logs silently in the background
    with st.spinner("Searching ChromaDB for relevant logs..."):
        retrieved_logs = retrieve_corporate_context(user_query)
        
    #PROMPT AUGMENTATION - merges logs and question for the AI
    augmented_prompt = f"Relevant Logs:\n{retrieved_logs}\n\nAnalyst Question: {user_query}"
    st.session_state.messages.append({"role": "user", "content": augmented_prompt})

    #AI GENERATION - stream the response back to the UI
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            # ollama
            response = ollama.chat(
                model='phi3',  # could also use llama3
                messages=st.session_state.messages,
                stream=True
            )
            
            # stream the output chunks to create a typing effect
            for chunk in response:
                full_response += chunk['message']['content']
                response_placeholder.markdown(full_response + "▌")
            
            # finalize the text block
            response_placeholder.markdown(full_response)
            
            # saves the AI's response to both memory states
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.session_state.display_messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Connection to Ollama failed: {e}. Please ensure the Ollama app is running.")