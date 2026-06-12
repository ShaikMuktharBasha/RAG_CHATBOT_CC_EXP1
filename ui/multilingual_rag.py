import streamlit as st
import textwrap
import time
from rag_engine import RAGEngine
from langchain_groq import ChatGroq

def render_multilingual_rag_page(active_api_key, selected_model, active_groq_key):
    """Renders the Multilingual RAG Translator workspace supporting both RAG and direct Groq translation."""
    
    # Session state for target language
    if "target_language" not in st.session_state:
        st.session_state.target_language = "Hindi"
        
    # Page Header
    st.markdown("""
    <div class="header-container" style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding-bottom: 10px;">
        <div>
            <h1 class="main-title" style="font-size: 1.6rem; margin: 0;">🌐 Multilingual RAG & Groq Translator</h1>
            <p class="subtitle" style="font-size: 0.8rem; margin: 0;">Cross-lingual PDF search (Gemini) and ultra-fast sentence-by-sentence translator (Groq).</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Core Tab Selector
    tab_rag, tab_direct = st.tabs(["📄 Document RAG Translator", "⚡ Direct Text Translator (Groq)"])

    # Languages List
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

    # ==================== TAB A: DOCUMENT RAG TRANSLATOR ====================
    with tab_rag:
        # Clean Language Selector UI Card
        col_l1, col_l2 = st.columns([2, 1])
        with col_l1:
            try:
                current_idx = [l.split(" ")[0].lower() for l in languages].index(st.session_state.target_language.lower())
            except ValueError:
                current_idx = 0
                
            selected_lang_full = st.selectbox(
                "RAG Target Translation Language:",
                options=languages,
                index=current_idx,
                key="rag_lang_selector"
            )
            st.session_state.target_language = selected_lang_full.split(" ")[0]
            
        with col_l2:
            st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)
            if st.button("🧹 Clear Chat History", key="clear_multilingual_chat"):
                st.session_state.messages = []
                st.toast("Chat history cleared!", icon="🧹")
                st.rerun()

        # Active Document check
        if not st.session_state.processed:
            st.warning("⚠️ Please upload a PDF document in the sidebar to activate the Document RAG Translator.")
        else:
            # Sub-case: Empty chat history
            if len(st.session_state.messages) == 0:
                st.markdown(f"""
                <div class="centered-welcome" style="margin-top: 30px;">
                    <div style="font-size: 2.2rem; margin-bottom: 8px;">🌍</div>
                    <h2 class="welcome-title" style="font-size: 1.5rem;">Document: {st.session_state.doc_info['name']}</h2>
                    <p class="welcome-subtitle" style="font-size: 0.9rem;">Ready for cross-lingual query retrieval. Select a quick action or write a query below.</p>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="prompt-grid">', unsafe_allow_html=True)
                col1, col2 = st.columns(2)
                lang = st.session_state.target_language
                with col1:
                    if st.button(f"📝 Summarize Document in {lang}", key="prompt_sum_lang"):
                        st.session_state.messages.append({
                            "role": "user", 
                            "content": f"Can you summarize the main contents of this document in 3 paragraphs? Please write the response in {lang}."
                        })
                        st.rerun()
                    if st.button(f"❓ FAQ List in {lang}", key="prompt_faq_lang"):
                        st.session_state.messages.append({
                            "role": "user", 
                            "content": f"Generate a list of 5 frequently asked questions and answers based on this document. Please write the response in {lang}."
                        })
                        st.rerun()
                with col2:
                    if st.button(f"🔑 Key Takeaways in {lang}", key="prompt_takeaways_lang"):
                        st.session_state.messages.append({
                            "role": "user", 
                            "content": f"What are the 5 most important insights or takeaways from this document? Please write the response in {lang}."
                        })
                        st.rerun()
                    if st.button(f"🔍 Term definitions in {lang}", key="prompt_def_lang"):
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
            query = st.chat_input(f"Ask a question about the PDF in English or {st.session_state.target_language}...")
            if query:
                st.session_state.messages.append({"role": "user", "content": query})
                st.rerun()

    # ==================== TAB B: DIRECT TEXT TRANSLATOR (GROQ) ====================
    with tab_direct:
        st.markdown("<h3 style='font-size: 1.15rem; font-weight: 600; color: #ffffff; margin-bottom: 5px; margin-top: 10px;'>⚡ Fast Translation Engine</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size: 0.8rem; margin-bottom: 20px;'>Type any phrase, sentence, or paragraph to translate it directly using high-performance models on Groq.</p>", unsafe_allow_html=True)
        
        # 1. Inputs
        direct_input = st.text_area(
            "Enter Text to Translate:",
            placeholder="Type your text here... e.g. I am working now",
            key="direct_translator_input",
            height=110
        )
        
        col_params1, col_params2 = st.columns(2)
        with col_params1:
            try:
                current_direct_idx = [l.split(" ")[0].lower() for l in languages].index(st.session_state.target_language.lower())
            except ValueError:
                current_direct_idx = 0
            
            direct_lang_full = st.selectbox(
                "Target Language:",
                options=languages,
                index=current_direct_idx,
                key="direct_lang_selector"
            )
            direct_target_lang = direct_lang_full.split(" ")[0]
            
        with col_params2:
            groq_models = [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant",
                "mixtral-8x7b-32768",
                "gemma2-9b-it"
            ]
            selected_groq_model = st.selectbox(
                "Groq Model Endpoint:",
                options=groq_models,
                index=0,
                key="groq_model_selector"
            )
            
        col_run_t, col_clear_t = st.columns([4, 1])
        with col_run_t:
            run_trans_btn = st.button("🚀 Translate Text", key="run_direct_translation", use_container_width=True)
        with col_clear_t:
            clear_trans_btn = st.button("🧹 Clear Output", key="clear_direct_translation", use_container_width=True)
            
        # Session state for direct translation history
        if "direct_translation_result" not in st.session_state or clear_trans_btn:
            st.session_state.direct_translation_result = None
            
        if run_trans_btn:
            if not direct_input.strip():
                st.error("❌ Please provide text to translate.")
            elif not active_groq_key:
                st.error("❌ Groq API Key required. Please configure it in the 'System Configurations' expander in the sidebar.")
            else:
                with st.spinner("Processing Groq API request..."):
                    try:
                        # 2. Initialize ChatGroq
                        t_start = time.time()
                        llm = ChatGroq(
                            api_key=active_groq_key,
                            model_name=selected_groq_model,
                            temperature=0.1
                        )
                        
                        system_msg = (
                            "You are a professional, accurate translator. "
                            f"Translate the text provided exactly into the target language: '{direct_target_lang}'. "
                            "Output ONLY the final translated text. Do not add any introductory or closing remarks, "
                            "do not write quotes, do not say 'Here is the translation'. Only output the translation."
                        )
                        
                        messages = [
                            ("system", system_msg),
                            ("human", direct_input)
                        ]
                        
                        response = llm.invoke(messages)
                        translation = response.content.strip()
                        t_end = time.time()
                        
                        st.session_state.direct_translation_result = {
                            "input": direct_input,
                            "output": translation,
                            "model": selected_groq_model,
                            "lang": direct_target_lang,
                            "latency": f"{(t_end - t_start) * 1000:.0f} ms",
                            "chars": len(direct_input)
                        }
                        st.toast("Translation completed successfully!", icon="✅")
                    except Exception as e:
                        st.error(f"❌ Groq translation failed: {str(e)}")
                        
        # 3. Output Panel
        if st.session_state.direct_translation_result:
            res = st.session_state.direct_translation_result
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background-color: rgba(99, 102, 241, 0.05); padding: 22px; border-radius: 14px; border: 1px solid rgba(99, 102, 241, 0.15); margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding-bottom: 8px; margin-bottom: 12px;">
                    <span style="font-size: 0.75rem; text-transform: uppercase; font-weight: 700; color: #818cf8; letter-spacing: 0.05em;">Translation Output ({res['lang']})</span>
                    <span style="font-size: 0.7rem; color: #64748b; font-weight: 500;">⚡ Groq Speed: {res['latency']}</span>
                </div>
                <p style="font-size: 1.25rem; font-weight: 600; color: #ffffff; line-height: 1.5; margin: 0; margin-bottom: 15px;">{res['output']}</p>
                <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                    <span class="clean-source-tag" style="font-size: 0.65rem;">🤖 Model: {res['model']}</span>
                    <span class="clean-source-tag" style="font-size: 0.65rem;">📏 Length: {res['chars']} characters</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
