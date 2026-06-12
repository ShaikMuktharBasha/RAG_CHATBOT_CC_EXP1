import streamlit as st

def render_landing_page(process_pdf_callback):
    """Renders the landing view for document uploads when no document is processed yet."""
    st.markdown("""
<div class="centered-welcome">
    <div style="font-size: 3.2rem; margin-bottom: 20px; text-shadow: 0 10px 25px rgba(99, 102, 241, 0.2);">💬</div>
    <h1 class="welcome-title">What would you like to analyze?</h1>
    <p class="welcome-subtitle">
        Upload a PDF handbook or corporate document to activate the AI assistant, summarize its contents, or extract key takeaways.
    </p>
</div>
""", unsafe_allow_html=True)
    
    # Centered file uploader
    col_u1, col_u2, col_u3 = st.columns([1, 2, 1])
    with col_u2:
        main_uploaded_file = st.file_uploader(
            "Upload PDF Handbook",
            type=["pdf"],
            key="main_uploader",
            label_visibility="collapsed"
        )
        if main_uploaded_file is not None:
            process_pdf_callback(main_uploaded_file)
            
    # Suggestion previews (Visual cards, disabled until upload)
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<div class="prompt-grid">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.button("📝 Summarize Document\nUpload a PDF file to activate this prompt.", key="pre_sum", disabled=True)
        st.button("❓ Draft FAQ List\nUpload a PDF file to activate this prompt.", key="pre_faq", disabled=True)
    with col2:
        st.button("🔑 Key Takeaways\nUpload a PDF file to activate this prompt.", key="pre_takeaways", disabled=True)
        st.button("🔍 Term Definitions\nUpload a PDF file to activate this prompt.", key="pre_def", disabled=True)
    st.markdown('</div>', unsafe_allow_html=True)
