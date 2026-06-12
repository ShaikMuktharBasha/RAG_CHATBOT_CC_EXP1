import streamlit as st
import textwrap
from rag_engine import RAGEngine

def render_multilingual_rag_page(active_api_key, selected_model):
    """Renders the Multilingual RAG Translator page."""
    
    # Session state for target language
    if "target_language" not in st.session_state:
        st.session_state.target_language = "Hindi"
        
    # Page Header with Language Selector
    st.markdown("""
    <div class="header-container" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 10px;">
        <div>
            <h1 class="main-title" style="font-size: 1.6rem; margin: 0;">🌐 Multilingual RAG Translator</h1>
            <p class="subtitle" style="font-size: 0.8rem; margin: 0;">Query documents in English and receive responses translated to your chosen language.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Clean Language Selector UI Card
    col_l1, col_l2 = st.columns([2, 1])
    with col_l1:
        languages = [
            "Hindi (हिन्दी)", 
            "Telugu (తెలుగు)", 
            "Spanish (Español)", 
            "French (Français)", 
            "German (Deutsch)", 
            "Japanese (日本語)", 
            "Arabic (العربية)", 
            "Mandarin (中文)",
            "Russian (Русский)",
            "Portuguese (Português)",
            "English (English)"
        ]
        
        # Find index of previous selection
        try:
            current_idx = [l.split(" ")[0].lower() for l in languages].index(st.session_state.target_language.lower())
        except ValueError:
            current_idx = 0
            
        selected_lang_full = st.selectbox(
            "Select Target Language for Output:",
            options=languages,
            index=current_idx,
            key="lang_selector"
        )
        # Extract English name
        st.session_state.target_language = selected_lang_full.split(" ")[0]
        
    with col_l2:
        st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
        if st.button("🧹 Clear Chat History", key="clear_multilingual_chat"):
            st.session_state.messages = []
            st.toast("Chat history cleared!", icon="🧹")
            st.rerun()

    # Active Document check
    if not st.session_state.processed:
        st.warning("⚠️ Please upload a PDF document in the sidebar to activate the Multilingual RAG Translator.")
        return

    # Sub-case: Empty chat history
    if len(st.session_state.messages) == 0:
        st.markdown(f"""
        <div class="centered-welcome" style="margin-top: 50px;">
            <div style="font-size: 2.5rem; margin-bottom: 12px;">🌍</div>
            <h2 class="welcome-title" style="font-size: 1.7rem;">Document: {st.session_state.doc_info['name']}</h2>
            <p class="welcome-subtitle" style="font-size: 0.95rem;">Ready for translation. Select a quick action or type a custom question below.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="prompt-grid">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        lang = st.session_state.target_language
        with col1:
            if st.button(f"📝 Summarize Document in {lang}\nGet a quick summary in your selected language.", key="prompt_sum_lang"):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": f"Can you summarize the main contents of this document in 3 paragraphs? Please write the response in {lang}."
                })
                st.rerun()
            if st.button(f"❓ FAQ List in {lang}\nDraft frequently asked questions in {lang}.", key="prompt_faq_lang"):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": f"Generate a list of 5 frequently asked questions and answers based on this document. Please write the response in {lang}."
                })
                st.rerun()
        with col2:
            if st.button(f"🔑 Key Takeaways in {lang}\nExtract insights in {lang}.", key="prompt_takeaways_lang"):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": f"What are the 5 most important insights or takeaways from this document? Please write the response in {lang}."
                })
                st.rerun()
            if st.button(f"🔍 Term definitions in {lang}\nIdentify and translate jargon.", key="prompt_def_lang"):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": f"Identify and define key terms or acronyms used here. Explain their meanings in {lang}."
                })
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Sub-case: Active chat history
    else:
        # Show message log
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                
                # Show sources if assistant has them
                if message["role"] == "assistant" and "sources" in message and message["sources"]:
                    with st.expander("🔍 References (Original Source Passages)"):
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
                                    <span class="clean-source-title">Reference Passage #{idx + 1} (English)</span>
                                    {badge_html}
                                </div>
                                <div>{content}</div>
                            </div>
                            """), unsafe_allow_html=True)

    # Response generation trigger
    if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
        query = st.session_state.messages[-1]["content"]
        with st.chat_message("assistant"):
            with st.spinner(f"Searching document and translating to {st.session_state.target_language}..."):
                # Initialize engine if needed
                if (st.session_state.engine is None or 
                        active_api_key != st.session_state.current_api_key or 
                        selected_model != st.session_state.current_model):
                    st.session_state.engine = RAGEngine(google_api_key=active_api_key, model=selected_model)
                    st.session_state.current_api_key = active_api_key
                    st.session_state.current_model = selected_model
                
                # Retrieve and answer in chosen language
                response = st.session_state.engine.answer_question(
                    query, 
                    language=st.session_state.target_language
                )
                
                if "error" in response:
                    st.error(f"Error generating response: {response['error']}")
                    # Remove the failed user message
                    st.session_state.messages.pop()
                else:
                    st.markdown(response["answer"])
                    
                    if "context" in response and response["context"]:
                        with st.expander("🔍 References (Original Source Passages)"):
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
                                        <span class="clean-source-title">Reference Passage #{idx + 1} (English)</span>
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
    query = st.chat_input(f"Ask a question in English or {st.session_state.target_language}...")
    if query:
        st.session_state.messages.append({"role": "user", "content": query})
        st.rerun()
