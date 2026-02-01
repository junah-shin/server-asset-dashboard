"""
Authentication Module
=====================
Handles user authentication using Supabase Auth.

Features:
- Email/password login
- User registration
- Secure session management
- Logout functionality

Dependencies:
- Supabase client library
- Streamlit for session state

Configuration:
Set these environment variables in your .env file:
- SUPABASE_URL: Your Supabase project URL
- SUPABASE_KEY: Your Supabase anon/public key
"""

import streamlit as st
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_supabase_client() -> Client:
    """
    Initialize and return Supabase client.
    
    Returns:
        Client: Configured Supabase client instance
        
    Raises:
        Stops Streamlit execution if credentials are missing
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        st.error("⚠️ Supabase credentials not found. Please check your .env file.")
        st.stop()
    
    return create_client(url, key)


def login(email: str, password: str) -> bool:
    """
    Authenticate user with email and password.
    
    Args:
        email (str): User's email address
        password (str): User's password
        
    Returns:
        bool: True if login successful, False otherwise
        
    Side Effects:
        Updates st.session_state.user and st.session_state.authenticated on success
    """
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if response.user:
            # Store user info in session state
            st.session_state.user = response.user
            st.session_state.authenticated = True
            return True
        return False
        
    except Exception as e:
        st.error(f"❌ Login failed: {str(e)}")
        return False


def signup(email: str, password: str) -> bool:
    """
    Register a new user account.
    
    Args:
        email (str): User's email address
        password (str): User's password (min. 6 characters)
        
    Returns:
        bool: True if signup successful, False otherwise
        
    Note:
        Users will receive a confirmation email from Supabase.
        Email verification is required before login.
    """
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        if response.user:
            st.success("✅ Account created! Please check your email to verify your account.")
            return True
        return False
        
    except Exception as e:
        st.error(f"❌ Signup failed: {str(e)}")
        return False


def logout():
    """
    Log out the current user.
    
    Side Effects:
        Clears Supabase session and resets st.session_state
    """
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
        
        # Clear session state
        st.session_state.authenticated = False
        st.session_state.user = None
        
    except Exception as e:
        st.error(f"❌ Logout failed: {str(e)}")


def check_authentication() -> bool:
    """
    Check if a user is currently authenticated.
    
    Returns:
        bool: True if user is authenticated, False otherwise
    """
    return st.session_state.get("authenticated", False)


# Optional: Add password reset functionality
def request_password_reset(email: str) -> bool:
    """
    Send password reset email to user.
    
    Args:
        email (str): User's email address
        
    Returns:
        bool: True if reset email sent successfully
        
    Note:
        This is an optional feature you can add to your login page.
    """
    try:
        supabase = get_supabase_client()
        supabase.auth.reset_password_for_email(email)
        st.success("✅ Password reset email sent! Check your inbox.")
        return True
        
    except Exception as e:
        st.error(f"❌ Failed to send reset email: {str(e)}")
        return False
