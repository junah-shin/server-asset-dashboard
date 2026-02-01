"""
Database Module
===============
Database query utilities for fetching SaaS metrics.

Features:
- Monthly revenue queries
- Revenue breakdown by plan tier
- Cohort retention analysis
- Current month metrics calculation

Tables Used:
- monthly_revenue: MRR, customer count, churn data
- revenue_by_plan: Plan tier breakdown
- cohort_retention: Customer retention by cohort

Note:
All queries use Supabase PostgREST API for secure data access.
"""

import pandas as pd
from supabase import Client
from typing import Dict
import streamlit as st


def get_monthly_revenue(supabase: Client, months: int = 12) -> pd.DataFrame:
    """
    Fetch monthly revenue data for the specified number of months.
    
    Args:
        supabase (Client): Supabase client instance
        months (int): Number of months to fetch (default: 12)
        
    Returns:
        pd.DataFrame: Monthly revenue data with columns:
            - month: Date (datetime)
            - mrr: Monthly Recurring Revenue (float)
            - customer_count: Total customers (int)
            - churn_count: Churned customers (int)
            - new_customers: New customers (int)
            
    Example:
        >>> supabase = get_supabase_client()
        >>> df = get_monthly_revenue(supabase, months=6)
        >>> print(df[['month', 'mrr']].head())
    """
    try:
        response = supabase.table("monthly_revenue")\
            .select("*")\
            .order("month", desc=True)\
            .limit(months)\
            .execute()
        
        df = pd.DataFrame(response.data)
        if not df.empty:
            df['month'] = pd.to_datetime(df['month'])
            df = df.sort_values('month')
        return df
        
    except Exception as e:
        st.error(f"❌ Error fetching revenue data: {str(e)}")
        return pd.DataFrame()


def get_revenue_by_plan(supabase: Client, months: int = 12) -> pd.DataFrame:
    """
    Fetch revenue breakdown by plan tier.
    
    Args:
        supabase (Client): Supabase client instance
        months (int): Number of months to fetch (default: 12)
        
    Returns:
        pd.DataFrame: Plan revenue data with columns:
            - month: Date (datetime)
            - plan_tier: Plan name (str)
            - revenue: Revenue for this plan (float)
            - customer_count: Customers on this plan (int)
            
    Note:
        Fetches data for all plan tiers (typically 3 tiers: starter, pro, enterprise)
        so the result will have months * 3 rows.
    """
    try:
        # Fetch data for all plans across the specified months
        response = supabase.table("revenue_by_plan")\
            .select("*")\
            .order("month", desc=True)\
            .limit(months * 3)\
            .execute()
        
        df = pd.DataFrame(response.data)
        if not df.empty:
            df['month'] = pd.to_datetime(df['month'])
            df = df.sort_values(['month', 'plan_tier'])
        return df
        
    except Exception as e:
        st.error(f"❌ Error fetching plan data: {str(e)}")
        return pd.DataFrame()


def get_cohort_retention(supabase: Client, cohorts: int = 6) -> pd.DataFrame:
    """
    Fetch cohort retention analysis data.
    
    Args:
        supabase (Client): Supabase client instance
        cohorts (int): Number of cohorts to analyze (default: 6)
        
    Returns:
        pd.DataFrame: Cohort retention data with columns:
            - cohort_month: Cohort signup month (datetime)
            - month_number: Months since signup (int)
            - customers_remaining: Active customers (int)
            - retention_rate: Retention percentage (float)
            
    Use Case:
        Analyze how well you retain customers over time.
        Month 0 = signup month (100% retention)
        Month 1 = 1 month later
        Month 6 = 6 months later
    """
    try:
        response = supabase.table("cohort_retention")\
            .select("*")\
            .order("cohort_month", desc=True)\
            .execute()
        
        df = pd.DataFrame(response.data)
        if not df.empty:
            df['cohort_month'] = pd.to_datetime(df['cohort_month'])
            
            # Filter to most recent cohorts
            recent_cohorts = df['cohort_month'].unique()[:cohorts]
            df = df[df['cohort_month'].isin(recent_cohorts)]
            df = df.sort_values(['cohort_month', 'month_number'])
        return df
        
    except Exception as e:
        st.error(f"❌ Error fetching cohort data: {str(e)}")
        return pd.DataFrame()


def get_current_metrics(supabase: Client) -> Dict:
    """
    Calculate current month's key performance indicators.
    
    Args:
        supabase (Client): Supabase client instance
        
    Returns:
        dict: Dictionary containing:
            - mrr: Current MRR (float)
            - mrr_growth: MRR growth vs previous month (%)
            - customers: Current customer count (int)
            - customer_growth: Customer growth vs previous month (%)
            - churn_rate: Current month churn rate (%)
            - new_customers: New customers this month (int)
            
    Example:
        >>> metrics = get_current_metrics(supabase)
        >>> print(f"MRR: ${metrics['mrr']:,.0f} ({metrics['mrr_growth']:+.1f}%)")
    """
    try:
        # Get latest 2 months for comparison
        response = supabase.table("monthly_revenue")\
            .select("*")\
            .order("month", desc=True)\
            .limit(2)\
            .execute()
        
        data = response.data
        if len(data) < 1:
            return {}
        
        current = data[0]
        previous = data[1] if len(data) > 1 else current
        
        # Calculate growth rates
        mrr_growth = (
            ((current['mrr'] - previous['mrr']) / previous['mrr'] * 100)
            if previous['mrr'] > 0 else 0
        )
        
        customer_growth = (
            ((current['customer_count'] - previous['customer_count']) 
             / previous['customer_count'] * 100)
            if previous['customer_count'] > 0 else 0
        )
        
        churn_rate = (
            (current['churn_count'] / current['customer_count'] * 100)
            if current['customer_count'] > 0 else 0
        )
        
        return {
            'mrr': current['mrr'],
            'mrr_growth': round(mrr_growth, 1),
            'customers': current['customer_count'],
            'customer_growth': round(customer_growth, 1),
            'churn_rate': round(churn_rate, 1),
            'new_customers': current['new_customers']
        }
        
    except Exception as e:
        st.error(f"❌ Error fetching current metrics: {str(e)}")
        return {}


# Optional: Custom query builder for advanced use cases
def execute_custom_query(supabase: Client, table: str, filters: Dict = None) -> pd.DataFrame:
    """
    Execute a custom query with filters.
    
    Args:
        supabase (Client): Supabase client instance
        table (str): Table name to query
        filters (dict): Optional filters to apply
        
    Returns:
        pd.DataFrame: Query results
        
    Example:
        >>> filters = {'plan_tier': 'enterprise'}
        >>> df = execute_custom_query(supabase, 'revenue_by_plan', filters)
        
    Note:
        This is a template for adding custom queries.
        Expand as needed for your specific use cases.
    """
    try:
        query = supabase.table(table).select("*")
        
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        
        response = query.execute()
        return pd.DataFrame(response.data)
        
    except Exception as e:
        st.error(f"❌ Custom query failed: {str(e)}")
        return pd.DataFrame()
