"""
Charts Module
=============
Plotly chart generation utilities for SaaS metrics visualization.

Features:
- MRR trend charts
- Customer growth visualization
- Churn rate analysis
- Plan revenue breakdown
- Cohort retention heatmaps

Styling:
All charts use a consistent dark theme that matches the dashboard CSS.
Colors are optimized for clarity and professional appearance.

Dependencies:
- plotly.graph_objects for advanced charts
- plotly.express for quick visualizations
- pandas for data manipulation
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional


def create_mrr_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create a Monthly Recurring Revenue trend line chart.
    
    Args:
        df (pd.DataFrame): Revenue data with 'month' and 'mrr' columns
        
    Returns:
        go.Figure: Plotly figure object, or None if data is empty
        
    Features:
        - Line + markers for easy reading
        - Fill gradient under the line
        - Hover showing exact values
        - Dark theme compatible
        
    Example:
        >>> fig = create_mrr_chart(revenue_df)
        >>> st.plotly_chart(fig, use_container_width=True)
    """
    if df.empty:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['month'],
        y=df['mrr'],
        mode='lines+markers',
        name='MRR',
        line=dict(color='#00C853', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(0, 200, 83, 0.1)',
        hovertemplate='<b>%{x|%B %Y}</b><br>MRR: $%{y:,.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Monthly Recurring Revenue Trend',
        xaxis_title='Month',
        yaxis_title='MRR ($)',
        hovermode='x unified',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    return fig


def create_customer_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create a customer count trend chart.
    
    Args:
        df (pd.DataFrame): Revenue data with 'month' and 'customer_count' columns
        
    Returns:
        go.Figure: Plotly figure object, or None if data is empty
        
    Features:
        - Smooth line chart
        - Gradient markers
        - Clear growth trend visualization
    """
    if df.empty:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['month'],
        y=df['customer_count'],
        mode='lines+markers',
        name='Customers',
        line=dict(color='#2196F3', width=3),
        marker=dict(size=8),
        hovertemplate='<b>%{x|%B %Y}</b><br>Customers: %{y:,}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Customer Growth',
        xaxis_title='Month',
        yaxis_title='Total Customers',
        hovermode='x unified',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    return fig


def create_churn_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create a churn rate visualization as a bar chart.
    
    Args:
        df (pd.DataFrame): Revenue data with 'month', 'churn_count', 'customer_count'
        
    Returns:
        go.Figure: Plotly figure object, or None if data is empty
        
    Note:
        Churn rate is calculated as: (churn_count / customer_count) * 100
        Lower is better, so red color is used to indicate concern.
    """
    if df.empty:
        return None
    
    # Calculate churn rate percentage
    df_copy = df.copy()
    df_copy['churn_rate'] = (df_copy['churn_count'] / df_copy['customer_count'] * 100).round(2)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_copy['month'],
        y=df_copy['churn_rate'],
        name='Churn Rate',
        marker=dict(color='#FF5252'),
        hovertemplate='<b>%{x|%B %Y}</b><br>Churn Rate: %{y:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        title='Monthly Churn Rate',
        xaxis_title='Month',
        yaxis_title='Churn Rate (%)',
        hovermode='x unified',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    return fig


def create_plan_revenue_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create a pie chart showing revenue breakdown by plan tier.
    
    Args:
        df (pd.DataFrame): Plan data with 'month', 'plan_tier', 'revenue' columns
        
    Returns:
        go.Figure: Plotly figure object, or None if data is empty
        
    Features:
        - Donut chart (hole in middle for modern look)
        - Color-coded by tier
        - Shows both percentage and dollar amounts
        
    Note:
        Only shows the latest month's data for clarity.
    """
    if df.empty:
        return None
    
    # Get latest month data only
    latest_month = df['month'].max()
    latest_data = df[df['month'] == latest_month]
    
    fig = go.Figure()
    fig.add_trace(go.Pie(
        labels=latest_data['plan_tier'],
        values=latest_data['revenue'],
        hole=0.4,
        marker=dict(colors=['#00C853', '#2196F3', '#FF9800']),
        hovertemplate='<b>%{label}</b><br>Revenue: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Revenue by Plan Tier (Current Month)',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0')
    )
    
    return fig


def create_cohort_retention_table(df: pd.DataFrame) -> Optional[pd.DataFrame]:
    """
    Create a cohort retention pivot table for heatmap visualization.
    
    Args:
        df (pd.DataFrame): Cohort data with columns:
            - cohort_month: When cohort signed up
            - month_number: Months since signup (0, 1, 2, ...)
            - retention_rate: Percentage retained
            
    Returns:
        pd.DataFrame: Pivot table with:
            - Rows: Cohort months
            - Columns: Month numbers (0, 1, 2, ...)
            - Values: Retention rates (%)
            
    Use with Streamlit:
        >>> cohort_table = create_cohort_retention_table(cohort_df)
        >>> styled = cohort_table.style.format("{:.1f}%")
        >>>     .background_gradient(cmap='RdYlGn', vmin=0, vmax=100)
        >>> st.dataframe(styled)
        
    Interpretation:
        - 100% in month 0 (everyone starts active)
        - Declining values show retention drop-off
        - Green = good retention, Red = poor retention
    """
    if df.empty:
        return None
    
    # Create pivot table
    pivot = df.pivot(
        index='cohort_month',
        columns='month_number',
        values='retention_rate'
    )
    
    # Format cohort months as readable strings
    pivot.index = pivot.index.strftime('%Y-%m')
    
    # Sort by cohort month (most recent first)
    pivot = pivot.sort_index(ascending=False)
    
    return pivot


# Optional: Add more chart types as needed
def create_growth_comparison_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """
    Create a comparison chart showing MRR growth vs customer growth.
    
    Args:
        df (pd.DataFrame): Revenue data
        
    Returns:
        go.Figure: Dual-axis chart
        
    Note:
        This is an optional chart type you can add to your dashboard.
        Useful for seeing if revenue is growing faster than customer count (good!)
        or slower (may indicate plan downgrades).
    """
    if df.empty or len(df) < 2:
        return None
    
    # Calculate month-over-month growth
    df_copy = df.copy()
    df_copy['mrr_growth'] = df_copy['mrr'].pct_change() * 100
    df_copy['customer_growth'] = df_copy['customer_count'].pct_change() * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_copy['month'],
        y=df_copy['mrr_growth'],
        name='MRR Growth (%)',
        line=dict(color='#00C853', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df_copy['month'],
        y=df_copy['customer_growth'],
        name='Customer Growth (%)',
        line=dict(color='#2196F3', width=2)
    ))
    
    fig.update_layout(
        title='Growth Rate Comparison',
        xaxis_title='Month',
        yaxis_title='Growth Rate (%)',
        hovermode='x unified',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#E0E0E0'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    
    return fig
