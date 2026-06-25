import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from utils.database import get_server_inventory, get_server_stats, add_server, delete_server, get_supabase_client
from utils.charts import (
    create_location_chart,
    create_env_chart,
    create_status_chart,
    create_location_env_chart,
)

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="Server Asset Dashboard",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_css():
    css_file = Path(__file__).parent / "assets" / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# ============================================================================
# DASHBOARD
# ============================================================================

def show_dashboard():
    with st.sidebar:
        st.title("🖥️ Server Dashboard")
        st.markdown("---")

        page = st.radio(
            "Navigation",
            ["Overview", "Server List", "Add Server"],
            label_visibility="collapsed"
        )

    supabase = get_supabase_client()

    if page == "Overview":
        show_overview_page(supabase)
    elif page == "Server List":
        show_server_list_page(supabase)
    elif page == "Add Server":
        show_add_server_page(supabase)

# ============================================================================
# OVERVIEW PAGE
# ============================================================================

def show_overview_page(supabase):
    logo_col, title_col = st.columns([0.4, 2])
    with logo_col:
        st.image(str(Path(__file__).parent / "assets" / "logo.png"), width=150)
    with title_col:
        st.title("서버 자산 현황")
        st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    stats = get_server_stats(supabase)
    df = get_server_inventory(supabase)

    if not stats:
        st.warning("No data available. Please run the schema.sql in Supabase SQL Editor first.")
        return

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Servers", f"{stats['total']}")
    with col2:
        st.metric("Normal", f"{stats['normal']}", delta=f"{stats['normal']}/{stats['total']}")
    with col3:
        st.metric("Fault", f"{stats['fault']}", delta=f"{stats['fault']}", delta_color="inverse")
    with col4:
        st.metric("Maintenance", f"{stats['maintenance']}")

    st.markdown("---")

    # Charts Row 1
    col1, col2 = st.columns(2)
    with col1:
        fig = create_location_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = create_env_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

    # Charts Row 2
    col1, col2 = st.columns(2)
    with col1:
        fig = create_status_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = create_location_env_chart(df)
        if fig:
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SERVER LIST PAGE
# ============================================================================

def show_server_list_page(supabase):
    st.title("📋 Server Inventory")

    df = get_server_inventory(supabase)

    if df.empty:
        st.warning("No servers found.")
        return

    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        location_filter = st.multiselect("Location", options=['IDC', 'HQ'], default=['IDC', 'HQ'])
    with col2:
        env_filter = st.multiselect("Environment", options=['PRD', 'STG', 'DEV'], default=['PRD', 'STG', 'DEV'])
    with col3:
        status_filter = st.multiselect("Status", options=['정상', '장애', '점검'], default=['정상', '장애', '점검'])

    filtered_df = df[
        (df['location'].isin(location_filter)) &
        (df['env'].isin(env_filter)) &
        (df['status'].isin(status_filter))
    ]

    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} servers**")

    display_df = filtered_df[['location', 'env', 'hostname', 'ip', 'owner', 'status']].copy()
    display_df.columns = ['Location', 'Env', 'Hostname', 'IP', 'Owner', 'Status']

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Status": st.column_config.TextColumn(
                "Status",
                help="정상 / 장애 / 점검"
            )
        }
    )

# ============================================================================
# ADD SERVER PAGE
# ============================================================================

def show_add_server_page(supabase):
    st.title("➕ Add Server")

    with st.form("add_server_form"):
        col1, col2 = st.columns(2)
        with col1:
            location = st.selectbox("Location", options=['IDC', 'HQ'])
            env = st.selectbox("Environment", options=['PRD', 'STG', 'DEV'])
            hostname = st.text_input("Hostname", placeholder="web-prd-01")
        with col2:
            ip = st.text_input("IP Address", placeholder="10.10.1.11")
            owner = st.text_input("Owner", placeholder="홍길동")
            status = st.selectbox("Status", options=['정상', '장애', '점검'])

        submit = st.form_submit_button("Add Server", use_container_width=True, type="primary")

        if submit:
            if hostname and ip and owner:
                server_data = {
                    'location': location,
                    'env': env,
                    'hostname': hostname,
                    'ip': ip,
                    'owner': owner,
                    'status': status,
                }
                if add_server(supabase, server_data):
                    st.success(f"Server '{hostname}' added successfully!")
                    st.rerun()
            else:
                st.warning("Please fill in all required fields (Hostname, IP, Owner)")

# ============================================================================
# MAIN
# ============================================================================

def main():
    show_dashboard()

if __name__ == "__main__":
    main()
