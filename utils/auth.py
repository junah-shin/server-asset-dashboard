import ssl
import os

_orig_create_default_context = ssl.create_default_context

def _create_unverified_context(*args, **kwargs):
    ctx = _orig_create_default_context(*args, **kwargs)
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

ssl.create_default_context = _create_unverified_context
ssl._create_default_https_context = ssl._create_unverified_context

import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        st.error("Supabase credentials not found. Please check your .env file.")
        st.stop()

    return create_client(url, key)


def login(email: str, password: str) -> bool:
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        if response.user:
            st.session_state.user = response.user
            st.session_state.authenticated = True
            return True
        return False

    except Exception as e:
        st.error(f"Login failed: {str(e)}")
        return False


def signup(email: str, password: str) -> bool:
    try:
        supabase = get_supabase_client()
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if response.user:
            st.success("Account created! Please check your email to verify.")
            return True
        return False

    except Exception as e:
        st.error(f"Signup failed: {str(e)}")
        return False


def logout():
    try:
        supabase = get_supabase_client()
        supabase.auth.sign_out()
        st.session_state.authenticated = False
        st.session_state.user = None
    except Exception as e:
        st.error(f"Logout failed: {str(e)}")


def check_authentication() -> bool:
    return st.session_state.get("authenticated", False)
