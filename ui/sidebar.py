import os
import streamlit as st

def render_sidebar():
    """Renders the settings sidebar and returns the active settings and file uploader."""
    with st.sidebar:
        st.markdown("<h2 style='font-size: 1.35rem; font-weight: 700; color: #ffffff; margin-bottom: 4px; margin-top: 10px;'>⚙️ RAG Settings</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #64748b; font-size: 0.8rem; margin-bottom: 25px;'>Configure API connections and parameters.</p>", unsafe_allow_html=True)
        
        # 1. API Key Setup
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
                
        # 2. Model Selection
        st.markdown("<p style='font-size: 0.8rem; font-weight: 600; color: #e2e8f0; margin-top: 15px; margin-bottom: 4px;'>Gemini Model Selection</p>", unsafe_allow_html=True)
        model_options = [
            "gemini-3.5-flash",
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
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
            selected_model = st.text_input("Custom Model Name", value="gemini-3.5-flash", placeholder="e.g. gemini-3.5-flash")
        else:
            selected_model = selected_option
            
        # 3. Document Uploader
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
        st.markdown("<h3 style='font-size: 0.9rem; font-weight: 700; color: #ffffff; margin-bottom: 10px;'>📁 Document Uploader</h3>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type=["pdf"],
            help="Upload the PDF document you want to query.",
            label_visibility="collapsed",
            key="sidebar_uploader"
        )
        
        # 4. Status Panel
        st.markdown("<hr style='border-color: rgba(255,255,255,0.05); margin: 20px 0;'>", unsafe_allow_html=True)
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
            <div class="stat-container">
                <div class="stat-label">Model</div>
                <div class="stat-value">{st.session_state.current_model}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="status-pill">
                <span class="status-dot waiting"></span>
                <span style="color: #f59e0b;">Awaiting Upload</span>
            </div>
            """, unsafe_allow_html=True)
            
        # 5. Clear Chat Control
        if len(st.session_state.messages) > 0:
            st.markdown("<br>", unsafe_allow_html=True)
            clear_button = st.button("🧹 Start New Chat")
            if clear_button:
                st.session_state.messages = []
                st.toast("Start a new chat thread!", icon="🧹")
                st.rerun()
                
    return active_api_key, selected_model, uploaded_file
