import streamlit as st

def apply_custom_styles():
    """Injects high-end CSS into Streamlit for a premium ChatGPT-style UI."""
    st.html("""
<style>
    /* Premium Google Font imports - loaded as the first rule */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    h1, h2, h3, h4, .main-title, .welcome-title {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* 1. Global Page Background - Forces Dark Mode background regardless of Streamlit theme settings */
    .stApp, div.stApp, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #030712 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(167, 139, 250, 0.07) 0px, transparent 50%) !important;
        color: #f3f4f6 !important;
    }
    
    /* 2. Global Text Color Overrides for Visibility */
    h1, h2, h3, h4, h5, h6, .main-title, .welcome-title, p, span, label, li, div {
        color: #f3f4f6 !important;
    }
    
    /* Secondary text elements */
    .subtitle, .welcome-subtitle, .stat-label, .subtitle strong {
        color: #9ca3af !important;
    }

    /* 3. Elegant Dark Sidebar Container */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"],
    .stSidebar,
    [data-testid="stSidebarContent"] {
        background-color: #080c14 !important;
        background-image: none !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        color: #e2e8f0 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #e2e8f0 !important;
    }

    /* Input box and Select dropdown wrappers in Sidebar */
    [data-testid="stSidebar"] div[data-baseweb="input"],
    [data-testid="stSidebar"] div[data-baseweb="select"],
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select {
        background-color: rgba(17, 24, 39, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    /* Header Container styling */
    .header-container {
        padding-top: 15px;
        padding-bottom: 20px;
        margin-bottom: 25px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .main-title {
        background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 50%, #f472b6 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 2.4rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 4px;
    }
    
    /* Centered Welcome / Landing Screen */
    .centered-welcome {
        max-width: 750px;
        margin: 60px auto 30px auto;
        text-align: center;
        animation: fadeInUp 0.6s ease-out;
    }
    
    .welcome-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 12px;
        letter-spacing: -0.03em;
        background: linear-gradient(120deg, #ffffff 40%, #e2e8f0 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    .welcome-subtitle {
        font-size: 1.1rem;
        margin-bottom: 30px;
        font-weight: 300;
        line-height: 1.6;
    }
    
    /* Prompt Suggestions Grid Container */
    .prompt-grid {
        max-width: 750px;
        margin: 20px auto;
        animation: fadeInUp 0.8s ease-out;
    }
    
    /* Glassmorphism prompt buttons override */
    .prompt-grid div[data-testid="column"] button {
        background-color: rgba(17, 24, 39, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        padding: 18px 22px !important;
        text-align: left !important;
        min-height: 95px !important;
        color: #e2e8f0 !important;
        font-weight: 500 !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1) !important;
        display: block !important;
        white-space: pre-line !important;
        line-height: 1.5 !important;
        width: 100% !important;
        backdrop-filter: blur(10px) !important;
    }
    
    .prompt-grid div[data-testid="column"] button:hover {
        background-color: rgba(31, 41, 55, 0.55) !important;
        border-color: rgba(129, 140, 248, 0.4) !important;
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.12) !important;
        color: #ffffff !important;
    }
    
    /* Status Badge & Indicator */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: rgba(17, 24, 39, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 100px !important;
        padding: 6px 14px !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .status-dot {
        width: 8px !important;
        height: 8px !important;
        border-radius: 50% !important;
    }
    
    .status-dot.active {
        background-color: #10b981 !important;
        box-shadow: 0 0 10px #10b981 !important;
        animation: pulseReady 2s infinite !important;
    }
    
    .status-dot.waiting {
        background-color: #f59e0b !important;
        box-shadow: 0 0 10px #f59e0b !important;
        animation: pulseWaiting 2s infinite !important;
    }
    
    /* Stats grid container in sidebar */
    .stat-container {
        background-color: rgba(17, 24, 39, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 10px !important;
        padding: 12px 14px !important;
        backdrop-filter: blur(8px) !important;
        margin-bottom: 10px !important;
        transition: border-color 0.3s ease !important;
    }
    
    .stat-container:hover {
        border-color: rgba(255, 255, 255, 0.08) !important;
    }
    
    .stat-value {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        color: #f1f5f9 !important;
    }
    
    /* Reference output cards with dynamic borders & tags */
    .clean-source-box {
        background-color: rgba(17, 24, 39, 0.4) !important;
        border-left: 3px solid #818cf8 !important;
        padding: 16px 20px !important;
        margin: 14px 0 !important;
        border-radius: 0 10px 10px 0 !important;
        border-top: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
        font-size: 0.9rem !important;
        line-height: 1.6 !important;
        color: #d1d5db !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
    }
    
    .clean-source-header {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 10px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.04) !important;
        padding-bottom: 6px !important;
    }

    .clean-source-title {
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        color: #818cf8 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
    }

    .clean-source-tag {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(167, 139, 250, 0.15) 100%) !important;
        border: 1px solid rgba(129, 140, 248, 0.3) !important;
        border-radius: 4px !important;
        padding: 2px 8px !important;
        font-size: 0.7rem !important;
        color: #a5b4fc !important;
        font-weight: 600 !important;
    }
    
    /* Standard Button Customizations */
    div.stButton > button {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(167, 139, 250, 0.15) 100%) !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(129, 140, 248, 0.2) !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-size: 0.875rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(4px) !important;
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        border-color: transparent !important;
        color: #ffffff !important;
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.25) !important;
        transform: translateY(-2px) !important;
    }
    
    /* 4. File Uploader Dropzone and Layout Custom styling (High Specificity) */
    div.stApp section[role="presentation"],
    div.stApp .st-key-main_uploader section,
    div.stApp .st-key-sidebar_uploader section,
    div.stApp div[data-testid="stFileUploader"] section,
    div.stApp section[data-testid="stFileUploader"],
    div.stApp .stFileUploader section,
    div.stApp .e3v525e0 {
        background-color: rgba(17, 24, 39, 0.5) !important;
        border: 1.5px dashed rgba(129, 140, 248, 0.25) !important;
        border-radius: 14px !important;
        padding: 24px !important;
        backdrop-filter: blur(8px) !important;
        transition: all 0.3s ease !important;
    }
    
    div.stApp section[role="presentation"]:hover,
    div.stApp .st-key-main_uploader section:hover,
    div.stApp .st-key-sidebar_uploader section:hover,
    div.stApp div[data-testid="stFileUploader"] section:hover,
    div.stApp section[data-testid="stFileUploader"]:hover,
    div.stApp .stFileUploader section:hover,
    div.stApp .e3v525e0:hover {
        border-color: rgba(129, 140, 248, 0.5) !important;
        background-color: rgba(17, 24, 39, 0.65) !important;
        box-shadow: 0 4px 25px rgba(99, 102, 241, 0.05) !important;
    }
    
    div.stApp [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #e2e8f0 !important;
    }
    
    /* 5. Custom Upload Button inside Uploader - forces gradient and high visibility */
    div.stApp section[role="presentation"] button,
    div.stApp .st-key-main_uploader button,
    div.stApp .st-key-sidebar_uploader button,
    div.stApp div[data-testid="stFileUploader"] button,
    div.stApp section[data-testid="stFileUploader"] button,
    div.stApp .stFileUploader button,
    div.stApp [data-testid="stBaseButton-secondary"],
    div.stApp .e12tamyi2 {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 26px !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s ease !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    div.stApp section[role="presentation"] button:hover,
    div.stApp .st-key-main_uploader button:hover,
    div.stApp .st-key-sidebar_uploader button:hover,
    div.stApp div[data-testid="stFileUploader"] button:hover,
    div.stApp section[data-testid="stFileUploader"] button:hover,
    div.stApp .stFileUploader button:hover,
    div.stApp [data-testid="stBaseButton-secondary"]:hover,
    div.stApp .e12tamyi2:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* wildcard selector to force all button text (including Streamlit nested tags) to be white */
    div.stApp section[role="presentation"] button *,
    div.stApp .st-key-main_uploader button *,
    div.stApp .st-key-sidebar_uploader button *,
    div.stApp div[data-testid="stFileUploader"] button *,
    div.stApp section[data-testid="stFileUploader"] button *,
    div.stApp [data-testid="stBaseButton-secondary"] *,
    div.stApp .e12tamyi2 * {
        color: #ffffff !important;
        font-weight: 700 !important;
    }


    
    /* 6. Chat Input container styling */
    [data-testid="stChatInput"] {
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        background-color: rgba(11, 15, 26, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(129, 140, 248, 0.4) !important;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.15) !important;
    }
    
    /* Expander override */
    .streamlit-expanderHeader {
        background-color: rgba(17, 24, 39, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        color: #9ca3af !important;
        font-size: 0.85rem !important;
        padding: 8px 12px !important;
    }
    
    .streamlit-expanderContent {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Alert styling overrides */
    div[data-testid="stNotification"] {
        background-color: rgba(17, 24, 39, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(8px) !important;
    }
    
    /* Custom chat bubbles overrides for ChatGPT aesthetic */
    div[data-testid="stChatMessage"] {
        background-color: rgba(17, 24, 39, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        border-radius: 16px !important;
        padding: 20px 24px !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05) !important;
        animation: slideInUp 0.4s ease-out;
    }
    
    div[data-testid="stChatMessage"] p {
        color: #e2e8f0 !important;
        font-size: 0.98rem !important;
        line-height: 1.65 !important;
    }
    
    /* Scrollbars design */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #030712;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(129, 140, 248, 0.3);
    }
    
    /* Keyframe Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulseReady {
        0% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        }
        70% {
            box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }
    
    @keyframes pulseWaiting {
        0% {
            box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.7);
        }
        70% {
            box-shadow: 0 0 0 8px rgba(245, 158, 11, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(245, 158, 11, 0);
        }
    }
</style>
""")
