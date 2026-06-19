import streamlit as st

def apply_custom_styles():
    """Injects high-end CSS into Streamlit for a clean, decent, and professional corporate UI."""
    st.html("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    /* Premium Google Font imports */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    h1, h2, h3, h4, .main-title, .welcome-title {
        font-family: 'Outfit', sans-serif !important;
    }
    
    /* 1. Global Page Background - Refined Dark Slate */
    .stApp, div.stApp, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #0b0f19 !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.05) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(99, 102, 241, 0.03) 0px, transparent 50%) !important;
        color: #e2e8f0 !important;
    }
    
    /* 2. Global Text Color Overrides for Visibility */
    h1, h2, h3, h4, h5, h6, .main-title, .welcome-title, p, span, label, li, div {
        color: #e2e8f0 !important;
    }
    
    /* Secondary text elements */
    .subtitle, .welcome-subtitle, .stat-label, .subtitle strong {
        color: #94a3b8 !important;
    }

    /* 3. Elegant Dark Sidebar Container */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"],
    .stSidebar,
    [data-testid="stSidebarContent"] {
        background-color: #0f172a !important;
        background-image: none !important;
        border-right: 1px solid rgba(148, 163, 184, 0.08) !important;
        color: #cbd5e1 !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #cbd5e1 !important;
    }

    /* Input box and Select dropdown wrappers in Sidebar */
    [data-testid="stSidebar"] div[data-baseweb="input"],
    [data-testid="stSidebar"] div[data-baseweb="select"],
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(148, 163, 184, 0.1) !important;
        border-radius: 6px !important;
        color: #ffffff !important;
    }
    
    /* Header Container styling */
    .header-container {
        padding-top: 15px;
        padding-bottom: 20px;
        margin-bottom: 25px;
        border-bottom: 1px solid rgba(148, 163, 184, 0.08);
    }
    
    .main-title {
        background: linear-gradient(135deg, #ffffff 0%, #93c5fd 50%, #60a5fa 100%) !important;
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
        animation: fadeInUp 0.5s ease-out;
    }
    
    .welcome-title {
        font-size: 2.6rem;
        font-weight: 800;
        color: #ffffff !important;
        margin-bottom: 12px;
        letter-spacing: -0.03em;
        background: linear-gradient(120deg, #ffffff 40%, #cbd5e1 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    .welcome-subtitle {
        font-size: 1.05rem;
        margin-bottom: 30px;
        font-weight: 300;
        line-height: 1.6;
        color: #94a3b8 !important;
    }
    
    /* Prompt Suggestions Grid Container */
    .prompt-grid {
        max-width: 750px;
        margin: 20px auto;
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Glassmorphism prompt buttons override */
    .prompt-grid div[data-testid="column"] button {
        background-color: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(148, 163, 184, 0.08) !important;
        border-radius: 10px !important;
        padding: 14px 18px !important;
        text-align: left !important;
        min-height: 80px !important;
        color: #cbd5e1 !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05) !important;
        display: block !important;
        white-space: pre-line !important;
        line-height: 1.4 !important;
        width: 100% !important;
        backdrop-filter: blur(8px) !important;
    }
    
    .prompt-grid div[data-testid="column"] button:hover {
        background-color: rgba(30, 41, 59, 0.6) !important;
        border-color: rgba(59, 130, 246, 0.3) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.08) !important;
        color: #ffffff !important;
    }
    
    /* Status Badge & Indicator */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(148, 163, 184, 0.08) !important;
        border-radius: 100px !important;
        padding: 4px 12px !important;
        font-size: 0.75rem !important;
        font-weight: 600 !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(6px) !important;
    }
    
    .status-dot {
        width: 6px !important;
        height: 6px !important;
        border-radius: 50% !important;
    }
    
    .status-dot.active {
        background-color: #10b981 !important;
        box-shadow: 0 0 8px #10b981 !important;
        animation: pulseReady 2s infinite !important;
    }
    
    .status-dot.waiting {
        background-color: #f59e0b !important;
        box-shadow: 0 0 8px #f59e0b !important;
        animation: pulseWaiting 2s infinite !important;
    }
    
    /* Stats grid container in sidebar */
    .stat-container {
        background-color: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(148, 163, 184, 0.06) !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        backdrop-filter: blur(6px) !important;
        margin-bottom: 8px !important;
        transition: border-color 0.2s ease !important;
    }
    
    .stat-container:hover {
        border-color: rgba(148, 163, 184, 0.12) !important;
    }
    
    .stat-value {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
    }
    
    /* Reference output cards with dynamic borders & tags */
    .clean-source-box {
        background-color: rgba(30, 41, 59, 0.3) !important;
        border-left: 3px solid #3b82f6 !important;
        padding: 14px 18px !important;
        margin: 12px 0 !important;
        border-radius: 0 8px 8px 0 !important;
        border-top: 1px solid rgba(148, 163, 184, 0.06) !important;
        border-right: 1px solid rgba(148, 163, 184, 0.06) !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.06) !important;
        font-size: 0.88rem !important;
        line-height: 1.55 !important;
        color: #cbd5e1 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
    }
    
    .clean-source-header {
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        margin-bottom: 8px !important;
        border-bottom: 1px solid rgba(148, 163, 184, 0.06) !important;
        padding-bottom: 4px !important;
    }
 
    .clean-source-title {
        font-size: 0.725rem !important;
        font-weight: 700 !important;
        color: #60a5fa !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
 
    .clean-source-tag {
        background: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        border-radius: 4px !important;
        padding: 1px 6px !important;
        font-size: 0.68rem !important;
        color: #93c5fd !important;
        font-weight: 600 !important;
    }
    
    /* Standard Button Customizations - decent slate design */
    div.stButton > button {
        background: rgba(30, 41, 59, 0.7) !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(148, 163, 184, 0.12) !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        width: 100% !important;
        transition: all 0.2s ease !important;
        backdrop-filter: blur(4px) !important;
    }
    
    div.stButton > button:hover {
        background: #3b82f6 !important;
        border-color: #3b82f6 !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.18) !important;
        transform: translateY(-1px) !important;
    }
    
    /* 4. File Uploader Dropzone and Layout Custom styling */
    div.stApp section[role="presentation"],
    div.stApp .st-key-main_uploader section,
    div.stApp .st-key-sidebar_uploader section,
    div.stApp div[data-testid="stFileUploader"] section,
    div.stApp section[data-testid="stFileUploader"],
    div.stApp .stFileUploader section {
        background-color: rgba(30, 41, 59, 0.35) !important;
        border: 1.5px dashed rgba(148, 163, 184, 0.15) !important;
        border-radius: 10px !important;
        padding: 20px !important;
        backdrop-filter: blur(6px) !important;
        transition: all 0.2s ease !important;
    }
    
    div.stApp section[role="presentation"]:hover,
    div.stApp .st-key-main_uploader section:hover,
    div.stApp .st-key-sidebar_uploader section:hover,
    div.stApp div[data-testid="stFileUploader"] section:hover,
    div.stApp section[data-testid="stFileUploader"]:hover,
    div.stApp .stFileUploader section:hover {
        border-color: rgba(59, 130, 246, 0.4) !important;
        background-color: rgba(30, 41, 59, 0.5) !important;
    }
    
    div.stApp [data-testid="stFileUploaderDropzoneInstructions"] {
        color: #cbd5e1 !important;
    }
    
    /* 5. Custom Upload Button inside Uploader - forces clean styling */
    div.stApp section[role="presentation"] button,
    div.stApp .st-key-main_uploader button,
    div.stApp .st-key-sidebar_uploader button,
    div.stApp div[data-testid="stFileUploader"] button,
    div.stApp section[data-testid="stFileUploader"] button,
    div.stApp .stFileUploader button,
    div.stApp [data-testid="stBaseButton-secondary"] {
        background: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 10px rgba(59, 130, 246, 0.15) !important;
        transition: all 0.2s ease !important;
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
    div.stApp [data-testid="stBaseButton-secondary"]:hover {
        background: #2563eb !important;
        box-shadow: 0 6px 14px rgba(59, 130, 246, 0.25) !important;
        transform: translateY(-1px) !important;
    }
 
    div.stApp section[role="presentation"] button *,
    div.stApp .st-key-main_uploader button *,
    div.stApp .st-key-sidebar_uploader button *,
    div.stApp div[data-testid="stFileUploader"] button *,
    div.stApp section[data-testid="stFileUploader"] button *,
    div.stApp [data-testid="stBaseButton-secondary"] * {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    
    /* 6. Chat Input container styling */
    [data-testid="stChatInput"] {
        border-radius: 10px !important;
        border: 1px solid rgba(148, 163, 184, 0.12) !important;
        background-color: rgba(15, 23, 42, 0.8) !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.15) !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: rgba(59, 130, 246, 0.3) !important;
    }
    
    /* Expander override */
    .streamlit-expanderHeader {
        background-color: rgba(30, 41, 59, 0.2) !important;
        border: 1px solid rgba(148, 163, 184, 0.06) !important;
        border-radius: 6px !important;
        color: #94a3b8 !important;
        font-size: 0.825rem !important;
        padding: 6px 10px !important;
    }
    
    .streamlit-expanderContent {
        background-color: transparent !important;
        border: none !important;
    }
    
    /* Alert styling overrides */
    div[data-testid="stNotification"] {
        background-color: rgba(30, 41, 59, 0.5) !important;
        border: 1px solid rgba(148, 163, 184, 0.08) !important;
        border-radius: 10px !important;
        backdrop-filter: blur(6px) !important;
    }
    
    /* Custom chat bubbles overrides for ChatGPT aesthetic */
    div[data-testid="stChatMessage"] {
        background-color: rgba(30, 41, 59, 0.35) !important;
        border: 1px solid rgba(148, 163, 184, 0.06) !important;
        border-radius: 12px !important;
        padding: 16px 20px !important;
        margin-bottom: 15px !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05) !important;
        animation: slideInUp 0.3s ease-out;
    }
    
    div[data-testid="stChatMessage"] p {
        color: #cbd5e1 !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }
    
    /* Scrollbars design */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: #0b0f19;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(148, 163, 184, 0.15);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(59, 130, 246, 0.3);
    }
    
    /* Keyframe Animations */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulseReady {
        0% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.5);
        }
        70% {
            box-shadow: 0 0 0 6px rgba(16, 185, 129, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }
    
    @keyframes pulseWaiting {
        0% {
            box-shadow: 0 0 0 0 rgba(245, 158, 11, 0.5);
        }
        70% {
            box-shadow: 0 0 0 6px rgba(245, 158, 11, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(245, 158, 11, 0);
        }
    }
    
    /* 7. Sidebar Experiment Navigation Custom styling */
    [data-testid="stSidebar"] div.stButton > button {
        background: transparent !important;
        border: 1px solid transparent !important;
        color: #94a3b8 !important;
        text-align: left !important;
        padding: 8px 12px !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        border-radius: 6px !important;
        transition: all 0.15s ease !important;
        margin-bottom: 2px !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
    }
    
    [data-testid="stSidebar"] div.stButton > button:hover {
        background: rgba(148, 163, 184, 0.06) !important;
        color: #f1f5f9 !important;
        transform: translateX(2px) !important;
        box-shadow: none !important;
    }
    
    /* Active button indicator */
    [data-testid="stSidebar"] div.stButton > button:active,
    [data-testid="stSidebar"] div.stButton > button:focus {
        background: rgba(59, 130, 246, 0.1) !important;
        border-left: 3px solid #3b82f6 !important;
        color: #3b82f6 !important;
    }
 
    /* 8. Experiment Dashboard Cards & Badges */
    .exp-header-card {
        background: rgba(30, 41, 59, 0.4) !important;
        border: 1px solid rgba(148, 163, 184, 0.08) !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        margin-bottom: 20px !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1) !important;
        position: relative;
        overflow: hidden;
    }
    
    .exp-header-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
    }
    
    .exp-title {
        font-size: 2rem !important;
        font-weight: 800 !important;
        margin-bottom: 6px !important;
        background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
    }
    
    .exp-meta-container {
        display: flex;
        gap: 8px;
        margin-bottom: 12px;
        flex-wrap: wrap;
    }
    
    .exp-badge {
        font-size: 0.7rem !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        padding: 3px 8px !important;
        border-radius: 100px !important;
        display: inline-flex;
        align-items: center;
    }
    
    .exp-badge.category {
        background-color: rgba(59, 130, 246, 0.1) !important;
        border: 1px solid rgba(59, 130, 246, 0.2) !important;
        color: #60a5fa !important;
    }
    
    .exp-badge.status-ready {
        background-color: rgba(16, 185, 129, 0.1) !important;
        border: 1px solid rgba(16, 185, 129, 0.2) !important;
        color: #34d399 !important;
    }
    
    .exp-badge.status-template {
        background-color: rgba(245, 158, 11, 0.1) !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
        color: #fbbf24 !important;
    }
    
    .learning-objectives-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 12px;
        margin: 16px 0;
    }
    
    .objective-card {
        background: rgba(30, 41, 59, 0.2) !important;
        border: 1px solid rgba(148, 163, 184, 0.06) !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        transition: all 0.2s ease !important;
        display: flex;
        gap: 10px;
        align-items: flex-start;
    }
    
    .objective-card:hover {
        border-color: rgba(59, 130, 246, 0.2) !important;
        background: rgba(30, 41, 59, 0.3) !important;
    }
    
    .objective-number {
        font-family: 'Outfit', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #3b82f6 !important;
        background: rgba(59, 130, 246, 0.1) !important;
        border-radius: 50% !important;
        width: 24px !important;
        height: 24px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        flex-shrink: 0 !important;
    }
    
    .objective-text {
        font-size: 0.825rem !important;
        color: #cbd5e1 !important;
        line-height: 1.35 !important;
    }
    
    /* Playground Panel Layouts */
    .playground-section {
        background: rgba(30, 41, 59, 0.25) !important;
        border: 1px solid rgba(148, 163, 184, 0.06) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 20px !important;
    }
</style>
""")
