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

import pandas as pd
from supabase import create_client, Client
from typing import Dict, List
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_supabase_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key:
        st.error("Supabase credentials not found. Please check your .env file.")
        st.stop()

    return create_client(url, key)


def get_server_inventory(supabase: Client) -> pd.DataFrame:
    try:
        response = supabase.table("server_inventory")\
            .select("*")\
            .order("location")\
            .execute()

        df = pd.DataFrame(response.data)
        return df

    except Exception as e:
        st.error(f"Error fetching server inventory: {str(e)}")
        return pd.DataFrame()


def get_server_stats(supabase: Client) -> Dict:
    try:
        response = supabase.table("server_inventory")\
            .select("*")\
            .execute()

        data = response.data
        if not data:
            return {}

        df = pd.DataFrame(data)
        total = len(df)
        normal = len(df[df['status'] == '정상'])
        fault = len(df[df['status'] == '장애'])
        maintenance = len(df[df['status'] == '점검'])

        return {
            'total': total,
            'normal': normal,
            'fault': fault,
            'maintenance': maintenance,
            'idc_count': len(df[df['location'] == 'IDC']),
            'hq_count': len(df[df['location'] == 'HQ']),
            'prd_count': len(df[df['env'] == 'PRD']),
            'stg_count': len(df[df['env'] == 'STG']),
            'dev_count': len(df[df['env'] == 'DEV']),
        }

    except Exception as e:
        st.error(f"Error fetching server stats: {str(e)}")
        return {}


def add_server(supabase: Client, server_data: Dict) -> bool:
    try:
        supabase.table("server_inventory").insert(server_data).execute()
        return True
    except Exception as e:
        st.error(f"Error adding server: {str(e)}")
        return False


def update_server(supabase: Client, server_id: str, server_data: Dict) -> bool:
    try:
        supabase.table("server_inventory")\
            .update(server_data)\
            .eq("id", server_id)\
            .execute()
        return True
    except Exception as e:
        st.error(f"Error updating server: {str(e)}")
        return False


def delete_server(supabase: Client, server_id: str) -> bool:
    try:
        supabase.table("server_inventory")\
            .delete()\
            .eq("id", server_id)\
            .execute()
        return True
    except Exception as e:
        st.error(f"Error deleting server: {str(e)}")
        return False
