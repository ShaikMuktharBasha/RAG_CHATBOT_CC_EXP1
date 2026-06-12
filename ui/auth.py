import streamlit as st
import sqlite3
import hashlib
import os
import base64
import textwrap

DB_FILE = "users.db"

def hash_password(password, salt="documind_salt_123"):
    """Hash password using SHA-256 and salt."""
    return hashlib.sha256((password + salt).encode()).hexdigest()

def init_db():
    """Initialize database and create users table if not exists."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def signup_user(username, password):
    """Add user to database."""
    if not username or not password:
        return False, "Username and password cannot be empty."
    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                  (username.strip().lower(), hash_password(password)))
        conn.commit()
        return True, "Account created successfully! Please log in."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def login_user(username, password):
    """Verify user credentials."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username.strip().lower(),))
    row = c.fetchone()
    conn.close()
    
    if row and row[0] == hash_password(password):
        return True
    return False

def get_base64_image(image_path):
    """Read a local image and convert it to a base64 string for background CSS inclusion."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

def render_auth_page():
    """Render the high-end split-screen login and signup page."""
    init_db()
    
    # Session state for auth toggle
    if "auth_mode" not in st.session_state:
        st.session_state.auth_mode = "login"
        
    # CSS overrides for the split-screen design
    st.markdown("""
        <style>
        /* Hide default Streamlit sidebar during login/signup */
        [data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        
        /* Centered login widget main wrapper */
        .login-main-card {
            background-color: transparent !important;
            margin-top: 40px;
            margin-bottom: 40px;
            animation: fadeInUp 0.6s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        /* Form Header label */
        .upper-header {
            color: #9ca3af !important;
            font-size: 0.75rem !important;
            font-weight: 700 !important;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 8px;
        }
        
        /* Style the native Streamlit Form container box to look like a premium white card */
        div[data-testid="stForm"] {
            background-color: #ffffff !important;
            border-radius: 16px !important;
            padding: 30px !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.25) !important;
            border: 1px solid rgba(0, 0, 0, 0.05) !important;
            min-height: 440px;
        }
        
        /* Force light theme colors inside the white form card */
        div[data-testid="stForm"] p,
        div[data-testid="stForm"] h2,
        div[data-testid="stForm"] label,
        div[data-testid="stForm"] span {
            color: #1f2937 !important;
        }
        
        /* Redesign Streamlit input elements inside the form container to be clean light inputs */
        div[data-testid="stForm"] div[data-baseweb="input"] {
            background-color: #ffffff !important;
            color: #1f2937 !important;
            border: 1px solid #d1d5db !important;
            border-radius: 8px !important;
        }
        div[data-testid="stForm"] input {
            color: #1f2937 !important;
            background-color: transparent !important;
        }
        div[data-testid="stForm"] div[data-baseweb="input"]:focus-within {
            border-color: #ea580c !important;
            box-shadow: 0 0 0 2px rgba(234, 88, 12, 0.1) !important;
        }
        
        /* Redesign Streamlit buttons inside the white form container to be solid Orange */
        div[data-testid="stForm"] button {
            background: linear-gradient(135deg, #e05615 0%, #f97316 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 20px !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            box-shadow: 0 4px 15px rgba(224, 86, 21, 0.35) !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
        }
        div[data-testid="stForm"] button:hover {
            background: linear-gradient(135deg, #ea580c 0%, #fb923c 100%) !important;
            box-shadow: 0 6px 20px rgba(224, 86, 21, 0.45) !important;
            transform: translateY(-2px) !important;
        }
        div[data-testid="stForm"] button * {
            color: #ffffff !important;
            font-weight: 700 !important;
        }
        
        /* Style the header switch buttons */
        div.stButton > button[data-testid="baseButton-secondary"] {
            background: rgba(255, 255, 255, 0.03) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 6px 14px !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        div.stButton > button[data-testid="baseButton-secondary"]:hover {
            background: rgba(255, 255, 255, 0.08) !important;
            border-color: rgba(255, 255, 255, 0.2) !important;
            color: #ffffff !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Centering container
    col_space_l, col_main, col_space_r = st.columns([1, 10, 1])
    
    with col_main:
        st.markdown('<div class="login-main-card">', unsafe_allow_html=True)
        
        # Split layout: 1.3 for the visual banner, 1 for the form
        col_banner, col_form = st.columns([1.3, 1], gap="medium")
        
        # ----------------- LEFT PANEL: VISUAL BANNER WITH OVERLAY -----------------
        with col_banner:
            banner_path = os.path.join("assets", "login_banner.png")
            banner_base64 = get_base64_image(banner_path)
            
            if banner_base64:
                background_css = f"background-image: url(data:image/png;base64,{banner_base64});"
            else:
                background_css = "background-color: #e05615;"  # Fallback solid color
                
            # Use textwrap.dedent to strip indentation so markdown doesn't treat the HTML string as a code block
            st.markdown(textwrap.dedent(f"""
            <div style="{background_css} background-size: cover; background-position: center; border-radius: 16px; min-height: 520px; padding: 40px; display: flex; align-items: flex-end; position: relative;">
                <!-- Dark Gradient Overlay for text readability -->
                <div style="position: absolute; top:0; left:0; right:0; bottom:0; background: linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.7) 100%); border-radius: 16px;"></div>
                
                <!-- Glassmorphic Details Card -->
                <div style="position: relative; z-index: 2; background: rgba(255, 255, 255, 0.08); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.15); border-radius: 16px; padding: 28px; width: 100%; box-shadow: 0 8px 32px rgba(0,0,0,0.25);">
                    <div style="font-size: 0.725rem; text-transform: uppercase; font-weight: 700; color: #ffedd5; letter-spacing: 0.08em; margin-bottom: 8px;">Knowledge at your fingertips</div>
                    <h2 style="font-family: 'Outfit', sans-serif; font-size: 1.95rem; font-weight: 800; color: #ffffff; line-height: 1.25; margin: 0 0 10px 0; letter-spacing: -0.02em;">Simplify Document Intelligence</h2>
                    <p style="color: #ffedd5; font-size: 0.85rem; line-height: 1.5; margin: 0 0 22px 0; font-weight: 300; opacity: 0.9;">Discover a faster way to query employee handbooks, translate documents, and run machine learning experiments from a single portal.</p>
                    
                    <!-- Feature Lists -->
                    <div style="display: flex; flex-direction: column; gap: 12px;">
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <span style="background: rgba(255,255,255,0.15); width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; flex-shrink: 0;">💡</span>
                            <span style="color: #ffffff; font-size: 0.85rem; font-weight: 600;">Instant AI-Powered Summaries</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <span style="background: rgba(255,255,255,0.15); width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; flex-shrink: 0;">💬</span>
                            <span style="color: #ffffff; font-size: 0.85rem; font-weight: 600;">Interactive PDF & RAG Q&A</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 12px;">
                            <span style="background: rgba(255,255,255,0.15); width: 26px; height: 26px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; flex-shrink: 0;">🎓</span>
                            <span style="color: #ffffff; font-size: 0.85rem; font-weight: 600;">22 Laboratory Experiments</span>
                        </div>
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)
            
        # ----------------- RIGHT PANEL: CLEAN LOGIN/SIGNUP FORM -----------------
        with col_form:
            # Form Header & Toggle (Outside of Form Card)
            col_hdr1, col_hdr2 = st.columns([1, 1])
            with col_hdr1:
                if st.session_state.auth_mode == "login":
                    st.markdown('<div class="upper-header">Secure Login</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="upper-header">Secure Sign Up</div>', unsafe_allow_html=True)
            with col_hdr2:
                # Text-based toggle switch
                if st.session_state.auth_mode == "login":
                    if st.button("Create account →", key="switch_to_signup", help="Register a new login"):
                        st.session_state.auth_mode = "signup"
                        st.rerun()
                else:
                    if st.button("← Back to login", key="switch_to_login", help="Go back to sign in"):
                        st.session_state.auth_mode = "login"
                        st.rerun()
            
            # Form Card container (using st.form so elements stay inside cleanly)
            if st.session_state.auth_mode == "login":
                with st.form(key="login_form"):
                    st.markdown("<h2 style='font-size: 2.1rem; font-weight: 700; margin-top: 0px; margin-bottom: 2px;'>Log in</h2>", unsafe_allow_html=True)
                    st.markdown("<p style='color: #6b7280; font-size: 0.85rem; margin-bottom: 20px;'>Open your saved uploads, summaries, and 22 NLP experiments from one unified workspace.</p>", unsafe_allow_html=True)
                    
                    login_username = st.text_input("USERNAME / EMAIL", key="login_user_input", placeholder="you@example.com").strip()
                    login_password = st.text_input("PASSWORD", type="password", key="login_pass_input", placeholder="Enter your password")
                    
                    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                    submit_login = st.form_submit_button("Log in")
                    
                    if submit_login:
                        if not login_username or not login_password:
                            st.error("Please fill in all fields.")
                        elif login_user(login_username, login_password):
                            st.session_state.authenticated = True
                            st.session_state.username = login_username
                            st.toast("Successfully signed in!", icon="🚀")
                            st.rerun()
                        else:
                            st.error("Invalid username or password.")
                            
            # Signup Form rendering
            else:
                with st.form(key="signup_form"):
                    st.markdown("<h2 style='font-size: 2.1rem; font-weight: 700; margin-top: 0px; margin-bottom: 2px;'>Sign up</h2>", unsafe_allow_html=True)
                    st.markdown("<p style='color: #6b7280; font-size: 0.85rem; margin-bottom: 20px;'>Register a secure account to save model configurations and track your experiment completions.</p>", unsafe_allow_html=True)
                    
                    signup_username = st.text_input("USERNAME / EMAIL", key="signup_user_input", placeholder="choose@example.com").strip()
                    signup_password = st.text_input("PASSWORD", type="password", key="signup_pass_input", placeholder="Choose password")
                    signup_confirm = st.text_input("CONFIRM PASSWORD", type="password", key="signup_confirm_input", placeholder="Confirm password")
                    
                    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
                    submit_signup = st.form_submit_button("Create Account")
                    
                    if submit_signup:
                        if not signup_username or not signup_password or not signup_confirm:
                            st.error("Please fill in all fields.")
                        elif signup_password != signup_confirm:
                            st.error("Passwords do not match.")
                        else:
                            success, message = signup_user(signup_username, signup_password)
                            if success:
                                st.success(message)
                                st.session_state.auth_mode = "login"
                                st.rerun()
                            else:
                                st.error(message)
            
        st.markdown('</div>', unsafe_allow_html=True)
