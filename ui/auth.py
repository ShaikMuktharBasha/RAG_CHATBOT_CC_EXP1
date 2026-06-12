import streamlit as st
import sqlite3
import hashlib
import os

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

def render_auth_page():
    """Render the login and signup page."""
    init_db()
    
    # Custom CSS for the login page
    st.markdown("""
        <style>
        .auth-container {
            max-width: 480px;
            margin: 40px auto;
            padding: 30px;
            background: rgba(17, 24, 39, 0.45) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
            text-align: center;
        }
        .auth-logo {
            font-size: 3rem;
            margin-bottom: 10px;
        }
        .auth-title {
            font-family: 'Outfit', sans-serif !important;
            font-size: 2.2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #a5b4fc 0%, #c084fc 50%, #f472b6 100%) !important;
            -webkit-background-clip: text !important;
            -webkit-text-fill-color: transparent !important;
            margin-bottom: 5px;
        }
        .auth-subtitle {
            color: #9ca3af !important;
            font-size: 0.95rem;
            margin-bottom: 25px;
        }
        div[data-testid="stImage"] img {
            border-radius: 12px !important;
            margin-bottom: 15px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        .stTabs [data-baseweb="tab"] {
            color: #9ca3af !important;
            font-weight: 600 !important;
        }
        .stTabs [aria-selected="true"] {
            color: #a5b4fc !important;
            border-bottom-color: #a5b4fc !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Layout wrapper
    st.markdown('<div class="auth-container">', unsafe_allow_html=True)
    
    # Render the banner image if it exists
    banner_path = os.path.join("assets", "auth_banner.png")
    if os.path.exists(banner_path):
        st.image(banner_path, use_container_width=True)
    else:
        st.markdown('<div class="auth-logo">💬</div>', unsafe_allow_html=True)
        
    st.markdown('<div class="auth-title">DocuMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="auth-subtitle">Secure Access to your Employee Handbook Assistant</div>', unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔑 Login", "📝 Sign Up"])
    
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        login_username = st.text_input("Username", key="login_user_input", placeholder="Enter username").strip()
        login_password = st.text_input("Password", type="password", key="login_pass_input", placeholder="Enter password")
        
        if st.button("Sign In", key="login_btn"):
            if not login_username or not login_password:
                st.error("Please fill in all fields.")
            elif login_user(login_username, login_password):
                st.session_state.authenticated = True
                st.session_state.username = login_username
                st.success("Successfully logged in!")
                st.rerun()
            else:
                st.error("Invalid username or password.")
                
    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        signup_username = st.text_input("Username", key="signup_user_input", placeholder="Choose username").strip()
        signup_password = st.text_input("Password", type="password", key="signup_pass_input", placeholder="Choose password")
        signup_confirm = st.text_input("Confirm Password", type="password", key="signup_confirm_input", placeholder="Confirm password")
        
        if st.button("Create Account", key="signup_btn"):
            if not signup_username or not signup_password or not signup_confirm:
                st.error("Please fill in all fields.")
            elif signup_password != signup_confirm:
                st.error("Passwords do not match.")
            else:
                success, message = signup_user(signup_username, signup_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)
                    
    st.markdown('</div>', unsafe_allow_html=True)
