import os
import streamlit as st
from dotenv import load_dotenv

def render_sidebar():
    """Renders the settings sidebar with 22 experiment buttons and global configuration settings."""
    load_dotenv()
    with st.sidebar:
        # Display current logged-in user card with logout button inline
        username = st.session_state.get("username", "")
        user_col, logout_col = st.columns([3, 1])
        with user_col:
            st.markdown(f"<div style='background-color: rgba(255, 255, 255, 0.03); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05); height: 42px; display: flex; align-items: center;'><span style='color: #a5b4fc; font-weight: 600; font-size: 0.85rem;'><i class=\"fa-solid fa-user\" style=\"color: #a5b4fc; margin-right: 5px;\"></i> User:</span> <span style='font-weight: 500; font-size: 0.85rem; margin-left: 5px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;' title='{username}'>{username}</span></div>", unsafe_allow_html=True)
        with logout_col:
            logout_button = st.button("", key="logout_btn", icon=":material/logout:", help="Log Out", use_container_width=True)
            if logout_button:
                st.session_state.authenticated = False
                st.session_state.username = ""
                st.session_state.processed = False
                st.session_state.messages = []
                st.session_state.doc_info = {"name": "", "pages": 0, "chunks": 0}
                st.session_state.selected_experiment = 1
                st.rerun()
        
        # 1. Title
        st.markdown("<h2 style='font-size: 1.35rem; font-weight: 700; color: #ffffff; margin-bottom: 4px; margin-top: 10px;'><i class=\"fa-solid fa-graduation-cap\" style=\"margin-right: 8px; color: #818cf8;\"></i> Laboratory Works</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size: 0.8rem; margin-bottom: 20px;'>Select an experiment to open its dedicated workspace.</p>", unsafe_allow_html=True)
        
        # Experiment names map
        EXP_NAMES = {
            1: "Employee Handbook (RAG)",
            2: "Multilingual RAG Translator",
            3: "Call Center Assistant"
        }
        
        # 2. Render flat experiment selector buttons
        active_exp = st.session_state.get("selected_experiment", 1)
        
        # Scrollable container for the flat list of 22 buttons
        st.markdown("<div style='max-height: 380px; overflow-y: auto; padding-right: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        for i in range(1, 23):
            if i in EXP_NAMES:
                btn_label = f"Exp{i}_{EXP_NAMES[i]}"
            else:
                btn_label = f"Exp{i}"
            
            if st.button(btn_label, key=f"sidebar_exp_btn_{i}", use_container_width=True):
                st.session_state.selected_experiment = i
                st.session_state.messages = []  # Clear chat history on switching experiments
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
                        
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
        
        # 4. Global Settings Panel
        with st.expander("System Configurations", expanded=True, icon=":material/settings:"):
            # API Key Setup
            env_api_key = os.environ.get("GOOGLE_API_KEY", "")
            if env_api_key:
                st.success("API Key loaded from environment", icon=":material/key:")
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
                    st.warning("API Key required.", icon=":material/warning:")
                    
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
                st.success("Groq API Key loaded", icon=":material/bolt:")
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
                    st.warning("Groq API Key missing.", icon=":material/warning:")
                
        # 5. Conditionally Render PDF Uploader for RAG-based experiments
        uploaded_file = None
        if active_exp in [1, 2]:
            st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-size: 0.9rem; font-weight: 700; color: #ffffff; margin-bottom: 10px;'><i class=\"fa-solid fa-folder-open\" style=\"margin-right: 8px; color: #818cf8;\"></i> Document Uploader</h3>", unsafe_allow_html=True)
            
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
                
        # (Log Out control moved inline with user card at the top)
            
    return active_api_key, selected_model, uploaded_file, active_groq_key
