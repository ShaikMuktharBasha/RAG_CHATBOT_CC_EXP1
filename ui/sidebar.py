import os
import streamlit as st
from dotenv import load_dotenv
from experiments_config import EXPERIMENTS

def render_sidebar():
    """Renders the settings sidebar with 22 experiment buttons and global configuration settings."""
    load_dotenv()
    with st.sidebar:
        # Display current logged-in user
        st.markdown(f"<div style='background-color: rgba(255, 255, 255, 0.03); padding: 10px 14px; border-radius: 8px; margin-bottom: 20px; border: 1px solid rgba(255,255,255,0.05);'><span style='color: #a5b4fc; font-weight: 600; font-size: 0.85rem;'>👤 User:</span> <span style='font-weight: 500; font-size: 0.85rem;'>{st.session_state.get('username', '')}</span></div>", unsafe_allow_html=True)
        
        # 1. Title
        st.markdown("<h2 style='font-size: 1.35rem; font-weight: 700; color: #ffffff; margin-bottom: 4px; margin-top: 10px;'>🎓 College Experiments</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size: 0.8rem; margin-bottom: 20px;'>Select an experiment to open its dedicated workspace.</p>", unsafe_allow_html=True)
        
        # 2. Group experiments by category
        categories = {}
        for exp_id, exp in EXPERIMENTS.items():
            cat = exp["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((exp_id, exp))
            
        # 3. Render experiment selector buttons
        active_exp = st.session_state.get("selected_experiment", 1)
        
        for cat_name, items in categories.items():
            # Check if this category contains the active experiment, default to open it
            is_expanded = any(exp_id == active_exp for exp_id, _ in items)
            with st.expander(f"📁 {cat_name}", expanded=is_expanded):
                for exp_id, exp in items:
                    is_active = (active_exp == exp_id)
                    btn_label = f"👉 Exp {exp_id}: {exp['title']}" if is_active else f"{exp['icon']} Exp {exp_id}: {exp['title']}"
                    
                    if st.button(btn_label, key=f"sidebar_exp_btn_{exp_id}", use_container_width=True):
                        st.session_state.selected_experiment = exp_id
                        st.session_state.messages = []  # Clear chat history on switching experiments
                        st.rerun()
                        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
        
        # 4. Global Settings Panel
        with st.expander("⚙️ System Configurations", expanded=True):
            # API Key Setup
            env_api_key = os.environ.get("GOOGLE_API_KEY", "")
            if env_api_key:
                st.success("🔑 API Key loaded from environment")
                active_api_key = env_api_key
            else:
                st.markdown("<p style='font-size: 0.8rem; font-weight: 600; color: #e2e8f0; margin-bottom: 4px;'>Google Gemini API Key</p>", unsafe_allow_html=True)
                sidebar_key = st.text_input(
                    label="Google API Key",
                    type="password",
                    placeholder="AIzaSy...",
                    help="Enter your Gemini API key from Google AI Studio.",
                    label_visibility="collapsed"
                )
                active_api_key = sidebar_key
                if not sidebar_key:
                    st.warning("⚠️ API Key required.")
                    
            # Model Selection
            st.markdown("<p style='font-size: 0.8rem; font-weight: 600; color: #e2e8f0; margin-top: 15px; margin-bottom: 4px;'>Gemini Model Selection</p>", unsafe_allow_html=True)
            model_options = [
                "gemini-1.5-flash",
                "gemini-1.5-pro",
                "gemini-2.5-flash",
                "gemini-2.5-pro",
                "Other (Custom)"
            ]
            selected_option = st.selectbox(
                "Gemini Model Selection",
                options=model_options,
                index=0,
                label_visibility="collapsed"
            )
            if selected_option == "Other (Custom)":
                selected_model = st.text_input("Custom Model Name", value="gemini-1.5-flash", placeholder="e.g. gemini-1.5-flash")
            else:
                selected_model = selected_option
                
            # Groq API Key Setup
            env_groq_key = os.environ.get("GROQ_API_KEY", "")
            if env_groq_key:
                st.success("⚡ Groq API Key loaded")
                active_groq_key = env_groq_key
            else:
                st.markdown("<p style='font-size: 0.8rem; font-weight: 600; color: #e2e8f0; margin-top: 15px; margin-bottom: 4px;'>Groq API Key</p>", unsafe_allow_html=True)
                sidebar_groq_key = st.text_input(
                    label="Groq API Key",
                    type="password",
                    placeholder="gsk_...",
                    help="Enter your Groq API key for translation acceleration.",
                    label_visibility="collapsed",
                    key="sidebar_groq_key"
                )
                active_groq_key = sidebar_groq_key
                if not sidebar_groq_key:
                    st.warning("⚠️ Groq API Key missing.")
                
        # 5. Conditionally Render PDF Uploader for RAG-based experiments
        uploaded_file = None
        if active_exp in [1, 2]:
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 0.9rem; font-weight: 700; color: #ffffff; margin-bottom: 10px;'>📁 Document Uploader</h3>", unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Upload PDF",
                type=["pdf"],
                help="Upload the PDF document you want to query.",
                label_visibility="collapsed",
                key="sidebar_uploader"
            )
            
            # Status Panel for RAG
            st.markdown("<br>", unsafe_allow_html=True)
            if st.session_state.processed:
                st.markdown("""
                <div class="status-pill">
                    <span class="status-dot active"></span>
                    <span style="color: #10b981;">Ready</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="stat-container">
                    <div class="stat-label">Document</div>
                    <div class="stat-value" title="{st.session_state.doc_info['name']}">{st.session_state.doc_info['name']}</div>
                </div>
                <div class="stat-container">
                    <div class="stat-label">Pages</div>
                    <div class="stat-value">{st.session_state.doc_info['pages']}</div>
                </div>
                <div class="stat-container">
                    <div class="stat-label">Chunks</div>
                    <div class="stat-value">{st.session_state.doc_info['chunks']}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="status-pill">
                    <span class="status-dot waiting"></span>
                    <span style="color: #f59e0b;">Awaiting Upload</span>
                </div>
                """, unsafe_allow_html=True)
                
        # 6. Log Out Control
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
        logout_button = st.button("🚪 Log Out", key="logout_btn")
        if logout_button:
            st.session_state.authenticated = False
            st.session_state.username = ""
            st.session_state.processed = False
            st.session_state.messages = []
            st.session_state.doc_info = {"name": "", "pages": 0, "chunks": 0}
            st.session_state.selected_experiment = 1
            st.rerun()
            
    return active_api_key, selected_model, uploaded_file, active_groq_key
