import streamlit as st
import textwrap
from rag_engine import RAGEngine

def render_chat_interface(active_api_key, selected_model):
    """Renders the chat interface workspace including messages, suggestions, references, and input."""
    # Page Header (small, out of the way)
    st.markdown(f"""
<div class="header-container" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
    <div>
        <h1 class="main-title" style="font-size: 1.6rem; margin: 0;">DocuMind Chat</h1>
        <p class="subtitle" style="font-size: 0.8rem; margin: 0;">Active document: <strong>{st.session_state.doc_info['name']}</strong></p>
    </div>
</div>
""", unsafe_allow_html=True)

    # Sub-case B1: Empty chat history (ChatGPT style suggestion cards)
    if len(st.session_state.messages) == 0:
        st.markdown(f"""
<div class="centered-welcome" style="margin-top: 80px;">
    <div style="font-size: 2.5rem; margin-bottom: 12px;">📊</div>
    <h2 class="welcome-title" style="font-size: 1.9rem;">{st.session_state.doc_info['name']}</h2>
    <p class="welcome-subtitle" style="font-size: 0.95rem;">Document is processed and ready. Select a starting point below or write a query.</p>
</div>
""", unsafe_allow_html=True)
        
        st.markdown('<div class="prompt-grid">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📝 Summarize Document\nGet a quick 3-paragraph executive summary.", key="prompt_sum"):
                st.session_state.messages.append({"role": "user", "content": "Can you summarize the main contents of this document in 3 paragraphs?"})
                st.rerun()
            if st.button("❓ Draft FAQ List\nGenerate frequently asked questions.", key="prompt_faq"):
                st.session_state.messages.append({"role": "user", "content": "Generate a list of 5 frequently asked questions and answers based on this document."})
                st.rerun()
        with col2:
            if st.button("🔑 Key Takeaways\nExtract the top 5 insights.", key="prompt_takeaways"):
                st.session_state.messages.append({"role": "user", "content": "What are the 5 most important insights or takeaways from this document?"})
                st.rerun()
            if st.button("🔍 Term Definitions\nDefine key terms and acronyms.", key="prompt_def"):
                st.session_state.messages.append({"role": "user", "content": "Identify and define any key terms, jargon, or acronyms used in this document."})
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Sub-case B2: Active chat history
    else:
        # Show message log
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources if assistant has them
                if message["role"] == "assistant" and "sources" in message and message["sources"]:
                    with st.expander("🔍 References"):
                        for idx, src in enumerate(message["sources"]):
                            page_text = ""
                            if isinstance(src, dict):
                                content = src.get("content", "")
                                metadata = src.get("metadata", {})
                                page = metadata.get("page")
                                if page is not None:
                                    page_text = f"Page {page + 1}"
                            else:
                                content = src
                                
                            badge_html = f'<span class="clean-source-tag">📄 {page_text}</span>' if page_text else ""
                            
                            st.markdown(textwrap.dedent(f"""
                            <div class="clean-source-box">
                                <div class="clean-source-header">
                                    <span class="clean-source-title">Reference Passage #{idx + 1}</span>
                                    {badge_html}
                                </div>
                                <div>{content}</div>
                            </div>
                            """), unsafe_allow_html=True)

    # Response generation trigger
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        query = st.session_state.messages[-1]["content"]
        with st.chat_message("assistant"):
            with st.spinner("Searching document and thinking..."):
                # Initialize engine if needed
                if (st.session_state.engine is None or 
                        active_api_key != st.session_state.current_api_key or 
                        selected_model != st.session_state.current_model):
                    st.session_state.engine = RAGEngine(google_api_key=active_api_key, model=selected_model)
                    st.session_state.current_api_key = active_api_key
                    st.session_state.current_model = selected_model
                
                response = st.session_state.engine.answer_question(query)
                
                if "error" in response:
                    st.error(f"Error generating response: {response['error']}")
                    # Remove the failed user message
                    st.session_state.messages.pop()
                else:
                    st.markdown(response["answer"])
                    
                    if "context" in response and response["context"]:
                        with st.expander("🔍 References"):
                            for idx, src in enumerate(response["context"]):
                                page_text = ""
                                if isinstance(src, dict):
                                    content = src.get("content", "")
                                    metadata = src.get("metadata", {})
                                    page = metadata.get("page")
                                    if page is not None:
                                        page_text = f"Page {page + 1}"
                                else:
                                    content = src
                                    
                                badge_html = f'<span class="clean-source-tag">📄 {page_text}</span>' if page_text else ""
                                
                                st.markdown(textwrap.dedent(f"""
                                <div class="clean-source-box">
                                    <div class="clean-source-header">
                                        <span class="clean-source-title">Reference Passage #{idx + 1}</span>
                                        {badge_html}
                                    </div>
                                    <div>{content}</div>
                                </div>
                                """), unsafe_allow_html=True)
                                
                    # Save response to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response.get("context", [])
                    })
                    st.rerun()

    # Chat Input Box at bottom
    query = st.chat_input("Ask a question about the active document...")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()
