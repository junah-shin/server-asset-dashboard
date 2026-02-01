"""
AI Insights Module
==================
AI-powered analytics using Anthropic's Claude API.

Features:
- Executive summary generation
- Natural language metric queries
- Trend analysis
- Actionable recommendations

Configuration:
Set ANTHROPIC_API_KEY in your .env file to enable AI features.
Get your API key from: https://console.anthropic.com/

Models Used:
- claude-3-5-sonnet-20241022 (balanced performance and cost)
- Upgrade to claude-opus for more detailed analysis if needed

Cost Optimization:
- Summaries use ~200-300 tokens
- Q&A uses ~150-250 tokens
- At $3/$15 per 1M tokens, very affordable for typical usage
"""

import os
from anthropic import Anthropic
import streamlit as st
from typing import Dict
import pandas as pd


def get_claude_client():
    """
    Initialize and return Claude API client.
    
    Returns:
        Anthropic: Configured Claude client, or None if API key missing
        
    Note:
        Displays user-friendly error if API key not configured.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        st.error("⚠️ Claude API key not found. Please add ANTHROPIC_API_KEY to your .env file.")
        st.info("💡 Get your API key from: https://console.anthropic.com/")
        return None
    return Anthropic(api_key=api_key)


def generate_executive_summary(metrics: Dict, revenue_df: pd.DataFrame) -> str:
    """
    Generate an AI-powered executive summary of current business health.
    
    Args:
        metrics (dict): Current month's key metrics
        revenue_df (pd.DataFrame): Historical revenue data
        
    Returns:
        str: 3-4 sentence executive summary
        
    Features:
        - Highlights overall business health
        - Identifies key trends
        - Provides one actionable insight
        - Professional tone suitable for sharing with stakeholders
        
    Example Output:
        "Your SaaS business is showing strong momentum with MRR up 12.3% to $47,250. 
        Customer growth of 8.5% outpaces a healthy churn rate of 3.2%. The recent 
        acceleration in enterprise plan adoption is driving above-average revenue per 
        customer. Focus: Continue investing in enterprise sales while maintaining 
        strong onboarding to preserve low churn."
    """
    client = get_claude_client()
    if not client:
        return "AI insights unavailable. Please configure your Claude API key in .env"
    
    # Prepare context for Claude
    recent_months = revenue_df.tail(3) if not revenue_df.empty else pd.DataFrame()
    recent_mrr = recent_months[['month', 'mrr']].to_string(index=False) if not recent_months.empty else 'No data'
    
    context = f"""
Based on the following SaaS metrics, provide a brief executive summary (3-4 sentences):

Current Metrics:
- MRR: ${metrics.get('mrr', 0):,.2f} ({metrics.get('mrr_growth', 0):+.1f}% vs last month)
- Customers: {metrics.get('customers', 0):,} ({metrics.get('customer_growth', 0):+.1f}% growth)
- Churn Rate: {metrics.get('churn_rate', 0):.1f}%
- New Customers This Month: {metrics.get('new_customers', 0)}

Recent Trend (last 3 months MRR):
{recent_mrr}

Focus on: overall business health, key trends, and one actionable insight.
Keep it professional and concise - suitable for sharing with stakeholders.
"""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[
                {"role": "user", "content": context}
            ]
        )
        return message.content[0].text
        
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def answer_metric_question(
    question: str, 
    metrics: Dict, 
    revenue_df: pd.DataFrame, 
    plan_df: pd.DataFrame
) -> str:
    """
    Answer natural language questions about SaaS metrics using AI.
    
    Args:
        question (str): User's question in natural language
        metrics (dict): Current month's key metrics
        revenue_df (pd.DataFrame): Historical revenue data
        plan_df (pd.DataFrame): Revenue breakdown by plan
        
    Returns:
        str: 2-3 sentence actionable answer
        
    Example Questions:
        - "What's driving my revenue growth?"
        - "Should I be worried about churn?"
        - "Which plan tier is most profitable?"
        - "What should I focus on this month?"
        - "How does my growth compare to industry benchmarks?"
        
    Example Answer:
        "Your revenue growth is primarily driven by strong enterprise plan adoption, 
        which grew 25% while contributing 60% of total MRR. Consider doubling down on 
        enterprise sales and creating upgrade paths from pro to enterprise."
    """
    client = get_claude_client()
    if not client:
        return "AI insights unavailable. Please configure your Claude API key in .env"
    
    # Prepare data context
    monthly_history = revenue_df[['month', 'mrr', 'customer_count']].tail(6).to_string(index=False) \
        if not revenue_df.empty else 'No data'
    
    plan_breakdown = plan_df.tail(3)[['plan_tier', 'revenue', 'customer_count']].to_string(index=False) \
        if not plan_df.empty else 'No data'
    
    context = f"""
You are a SaaS analytics assistant helping a founder understand their metrics. 
Answer the user's question based on this data. Be concise, actionable, and specific.

Current Metrics:
- MRR: ${metrics.get('mrr', 0):,.2f} (Growth: {metrics.get('mrr_growth', 0):+.1f}%)
- Customers: {metrics.get('customers', 0):,} (Growth: {metrics.get('customer_growth', 0):+.1f}%)
- Churn Rate: {metrics.get('churn_rate', 0):.1f}%
- New Customers This Month: {metrics.get('new_customers', 0)}

Monthly Revenue History (last 6 months):
{monthly_history}

Revenue by Plan (latest month):
{plan_breakdown}

User Question: {question}

Provide a concise, actionable answer (2-3 sentences max). Include specific numbers where relevant.
"""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=250,
            messages=[
                {"role": "user", "content": context}
            ]
        )
        return message.content[0].text
        
    except Exception as e:
        return f"Error: {str(e)}"


# Optional: Add trend prediction
def predict_next_month(revenue_df: pd.DataFrame) -> str:
    """
    Use AI to predict next month's performance based on trends.
    
    Args:
        revenue_df (pd.DataFrame): Historical revenue data
        
    Returns:
        str: Prediction with confidence level and reasoning
        
    Note:
        This is an optional feature for advanced dashboards.
        Requires at least 6 months of historical data for accuracy.
    """
    client = get_claude_client()
    if not client or revenue_df.empty or len(revenue_df) < 6:
        return "Insufficient data for prediction (need 6+ months)"
    
    recent_data = revenue_df.tail(6)[['month', 'mrr', 'customer_count', 'churn_count']].to_string(index=False)
    
    context = f"""
Based on this 6-month SaaS revenue history, predict next month's MRR and customer count.

Historical Data:
{recent_data}

Provide:
1. Predicted MRR (with range)
2. Predicted customer count
3. Confidence level (high/medium/low)
4. Key assumptions

Keep it brief (3-4 sentences).
"""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            messages=[{"role": "user", "content": context}]
        )
        return message.content[0].text
        
    except Exception as e:
        return f"Error: {str(e)}"


# Optional: Industry benchmark comparison
def compare_to_benchmarks(metrics: Dict) -> str:
    """
    Compare your metrics to industry benchmarks using AI knowledge.
    
    Args:
        metrics (dict): Your current metrics
        
    Returns:
        str: Comparison with industry standards and recommendations
        
    Note:
        Claude has knowledge of typical SaaS benchmarks:
        - Good churn: <5% monthly, <7% acceptable
        - Good growth: 10-20% MoM for early stage
        - CAC payback: <12 months ideal
    """
    client = get_claude_client()
    if not client:
        return "AI insights unavailable"
    
    context = f"""
Compare these SaaS metrics to industry benchmarks:

- MRR Growth: {metrics.get('mrr_growth', 0):+.1f}%
- Customer Growth: {metrics.get('customer_growth', 0):+.1f}%
- Churn Rate: {metrics.get('churn_rate', 0):.1f}%

Provide:
1. How each metric compares to typical SaaS benchmarks
2. Which metrics are strong vs need improvement
3. One specific recommendation

Keep it brief (3-4 sentences).
"""
    
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=200,
            messages=[{"role": "user", "content": context}]
        )
        return message.content[0].text
        
    except Exception as e:
        return f"Error: {str(e)}"
