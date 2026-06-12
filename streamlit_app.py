import os
import tempfile
import streamlit as st
from rag_engine import RAGEngine
from ui.styles import apply_custom_styles
from ui.sidebar import render_sidebar
from ui.landing_page import render_landing_page
from ui.chat_interface import render_chat_interface
from ui.multilingual_rag import render_multilingual_rag_page
from ui.sandbox_playground import render_sandbox_playground
from ui import render_auth_page

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="DocuMind RAG Assistant",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply Global Custom CSS Styles (Glassmorphism & animations)
apply_custom_styles()

# ----------------- SESSION STATE INITIALIZATION -----------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "messages" not in st.session_state:
    st.session_state.messages = []

if "processed" not in st.session_state:
    st.session_state.processed = False

if "doc_info" not in st.session_state:
    st.session_state.doc_info = {
        "name": "",
        "pages": 0,
        "chunks": 0
    }

if "engine" not in st.session_state:
    st.session_state.engine = None

if "current_api_key" not in st.session_state:
    st.session_state.current_api_key = ""

if "current_model" not in st.session_state:
    st.session_state.current_model = ""

if "selected_experiment" not in st.session_state:
    st.session_state.selected_experiment = 1

# ----------------- MAIN UI ROUTING & FLOW -----------------

if not st.session_state.authenticated:
    render_auth_page()
else:
    # ----------------- SIDEBAR CONTROLS -----------------
    active_api_key, selected_model, uploaded_file, active_groq_key = render_sidebar()

    # ----------------- MAIN PROCESSING LOGIC -----------------
    def process_uploaded_pdf(file_to_process):
        """Callback to extract text, chunk, and index the uploaded PDF using the RAG Engine."""
        if not active_api_key:
            st.error("❌ Google API Key required to initialize RAG Engine.")
            return
        
        with st.spinner("Extracting text and indexing document..."):
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(file_to_process.getvalue())
                    temp_path = tmp_file.name
                
                # Re-initialize engine if settings changed or first run
                if (st.session_state.engine is None or 
                        active_api_key != st.session_state.current_api_key or 
                        selected_model != st.session_state.current_model):
                    st.session_state.engine = RAGEngine(google_api_key=active_api_key, model=selected_model)
                    st.session_state.current_api_key = active_api_key
                    st.session_state.current_model = selected_model
                
                result = st.session_state.engine.process_document(temp_path)
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
                if result.get("success"):
                    st.session_state.processed = True
                    st.session_state.doc_info = {
                        "name": file_to_process.name,
                        "pages": result["num_pages"],
                        "chunks": result["num_chunks"]
                    }
                    st.session_state.messages = [] # Clear history on new upload
                    st.toast("Document processed successfully!", icon="✅")
                    st.rerun()
                else:
                    st.error(f"❌ Error processing document: {result.get('error')}")
            except Exception as e:
                st.error(f"❌ Failed to process document: {str(e)}")

    # Check if sidebar file uploaded but not processed yet (only for Exp 1 and 2)
    if st.session_state.selected_experiment in [1, 2]:
        if uploaded_file is not None and (not st.session_state.processed or uploaded_file.name != st.session_state.doc_info["name"]):
            process_uploaded_pdf(uploaded_file)

    # ----------------- MAIN UI ROUTING -----------------
    if st.session_state.selected_experiment == 1:
        if not st.session_state.processed:
            render_landing_page(process_uploaded_pdf)
        else:
            render_chat_interface(active_api_key, selected_model)
    elif st.session_state.selected_experiment == 2:
        render_multilingual_rag_page(active_api_key, selected_model, active_groq_key)
    else:
        render_sandbox_playground(st.session_state.selected_experiment, active_api_key, selected_model)



