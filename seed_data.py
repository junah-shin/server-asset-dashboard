"""
Database Seed Script
====================
Populate your Supabase database with realistic SaaS sample data.

Usage:
    python seed_data.py

What it does:
- Generates 12 months of realistic revenue data
- Creates plan tier breakdowns (Starter/Pro/Enterprise)
- Builds cohort retention analysis (6 cohorts)
- Includes realistic growth curves and churn patterns

Data Characteristics:
- Growing MRR with slight monthly variance
- Realistic churn rates (3-8%)
- Plan distribution: 50% Starter, 35% Pro, 15% Enterprise
- Cohort retention curves with natural drop-off

Prerequisites:
- Supabase database with schema.sql executed
- .env file configured with SUPABASE_URL and SUPABASE_KEY

Author: Your Company Name
"""

import os
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import random
import numpy as np
from supabase import create_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# CONFIGURATION
# ============================================================================

# Plan pricing (monthly)
PLAN_PRICES = {
    'starter': 29,
    'pro': 99,
    'enterprise': 299
}

# Data generation settings
MONTHS_TO_GENERATE = 12
COHORTS_TO_GENERATE = 6
BASE_CUSTOMERS = 50  # Starting customer count
BASE_MRR = 5000  # Starting MRR


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_supabase_client():
    """
    Initialize Supabase client with credentials from .env
    
    Returns:
        Client: Configured Supabase client
        
    Raises:
        ValueError: If credentials are missing
    """
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        raise ValueError(
            "Missing Supabase credentials. Please check your .env file.\n"
            "Required: SUPABASE_URL and SUPABASE_KEY"
        )
    
    return create_client(url, key)


def generate_monthly_data(months: int = MONTHS_TO_GENERATE) -> list:
    """
    Generate realistic monthly revenue data with growth trends.
    
    Args:
        months (int): Number of months to generate
        
    Returns:
        list: Monthly revenue records
        
    Data Pattern:
        - Compound growth with variance
        - Increasing churn rate with scale
        - New customer acquisition to sustain growth
    """
    data = []
    
    # Start date (N months ago from today)
    start_date = datetime.now() - relativedelta(months=months-1)
    
    for i in range(months):
        month_date = start_date + relativedelta(months=i)
        
        # Growth with realistic variance
        # Base growth ~8% per month with +/- 5% randomness
        growth_factor = 1 + (i * 0.08) + random.uniform(-0.05, 0.1)
        customers = int(BASE_CUSTOMERS * growth_factor)
        
        # MRR calculation with additional variance
        mrr = BASE_MRR * growth_factor * random.uniform(0.95, 1.05)
        
        # Churn increases slightly with scale (2-8%)
        churn_rate = min(0.05 + (i * 0.002), 0.08)
        churn_count = int(customers * churn_rate * random.uniform(0.8, 1.2))
        
        # New customers = growth + churn replacement
        if i > 0:
            prev_customers = data[i-1]['customer_count']
            new_customers = max(customers - prev_customers + churn_count, 0)
        else:
            new_customers = int(customers * 0.15)  # 15% of base for first month
        
        data.append({
            'month': month_date.strftime('%Y-%m-01'),
            'mrr': round(mrr, 2),
            'customer_count': customers,
            'churn_count': churn_count,
            'new_customers': new_customers
        })
    
    return data


def generate_plan_data(monthly_data: list) -> list:
    """
    Generate revenue breakdown by plan tier for each month.
    
    Args:
        monthly_data (list): Monthly revenue data
        
    Returns:
        list: Plan breakdown records (3 per month)
        
    Distribution:
        - Starter: 50% of customers
        - Pro: 35% of customers
        - Enterprise: 15% of customers
        
    Note:
        Revenue is normalized to match total MRR from monthly_data
    """
    plan_data = []
    
    for month_data in monthly_data:
        total_customers = month_data['customer_count']
        total_mrr = month_data['mrr']
        
        # Customer distribution by tier
        starter_customers = int(total_customers * 0.50)
        pro_customers = int(total_customers * 0.35)
        enterprise_customers = total_customers - starter_customers - pro_customers
        
        # Calculate ideal revenue (with variance for realism)
        starter_revenue = starter_customers * PLAN_PRICES['starter'] * random.uniform(0.95, 1.05)
        pro_revenue = pro_customers * PLAN_PRICES['pro'] * random.uniform(0.95, 1.05)
        enterprise_revenue = enterprise_customers * PLAN_PRICES['enterprise'] * random.uniform(0.95, 1.05)
        
        # Normalize to match total MRR exactly
        total_calc = starter_revenue + pro_revenue + enterprise_revenue
        if total_calc > 0:
            ratio = total_mrr / total_calc
            starter_revenue *= ratio
            pro_revenue *= ratio
            enterprise_revenue *= ratio
        
        # Add records for each plan tier
        plan_data.extend([
            {
                'month': month_data['month'],
                'plan_tier': 'starter',
                'revenue': round(starter_revenue, 2),
                'customer_count': starter_customers
            },
            {
                'month': month_data['month'],
                'plan_tier': 'pro',
                'revenue': round(pro_revenue, 2),
                'customer_count': pro_customers
            },
            {
                'month': month_data['month'],
                'plan_tier': 'enterprise',
                'revenue': round(enterprise_revenue, 2),
                'customer_count': enterprise_customers
            }
        ])
    
    return plan_data


def generate_cohort_data(cohorts: int = COHORTS_TO_GENERATE) -> list:
    """
    Generate cohort retention analysis data.
    
    Args:
        cohorts (int): Number of cohorts to create
        
    Returns:
        list: Cohort retention records
        
    Retention Pattern:
        - Month 0: 100% (all customers active at signup)
        - Month 1: ~85% retention
        - Month 2: ~75% retention
        - Month 6: ~60% retention (floor)
        
    Use Case:
        Analyze how well different signup cohorts retain over time.
        Newer cohorts have less data (fewer month_numbers).
    """
    cohort_data = []
    
    # Start N cohorts ago
    start_date = datetime.now() - relativedelta(months=cohorts-1)
    
    for cohort_idx in range(cohorts):
        cohort_month = start_date + relativedelta(months=cohort_idx)
        cohort_month_str = cohort_month.strftime('%Y-%m-01')
        
        # Initial cohort size (varies for realism)
        initial_customers = random.randint(20, 50)
        
        # Generate retention for available months
        # Newer cohorts have fewer data points
        max_months = min(6, cohorts - cohort_idx)
        
        for month_num in range(max_months):
            # Retention curve: exponential decay with floor
            # Formula: 100% - (month_num * 8%) - random variance
            base_retention = 100 - (month_num * 8) - random.uniform(0, 5)
            base_retention = max(base_retention, 60)  # 60% retention floor
            
            customers_remaining = int(initial_customers * (base_retention / 100))
            
            cohort_data.append({
                'cohort_month': cohort_month_str,
                'month_number': month_num,
                'customers_remaining': customers_remaining,
                'retention_rate': round(base_retention, 2)
            })
    
    return cohort_data


# ============================================================================
# MAIN SEEDING FUNCTION
# ============================================================================

def seed_database():
    """
    Main function to seed the database with sample data.
    
    Steps:
        1. Connect to Supabase
        2. Generate sample data
        3. Clear existing data
        4. Insert new data
        5. Display summary
        
    Returns:
        bool: True if successful, False otherwise
    """
    print("🌱 Starting database seeding...")
    print("=" * 60)
    
    try:
        # Connect to Supabase
        supabase = get_supabase_client()
        print("✅ Connected to Supabase")
        
        # Generate sample data
        print("\n📊 Generating sample data...")
        monthly_data = generate_monthly_data(months=MONTHS_TO_GENERATE)
        plan_data = generate_plan_data(monthly_data)
        cohort_data = generate_cohort_data(cohorts=COHORTS_TO_GENERATE)
        
        print(f"  ✓ {len(monthly_data)} monthly revenue records")
        print(f"  ✓ {len(plan_data)} plan breakdown records")
        print(f"  ✓ {len(cohort_data)} cohort retention records")
        
        # Clear existing data
        print("\n🧹 Clearing existing data...")
        # Use a non-existent UUID to trigger delete all
        null_uuid = '00000000-0000-0000-0000-000000000000'
        supabase.table("monthly_revenue").delete().neq('id', null_uuid).execute()
        supabase.table("revenue_by_plan").delete().neq('id', null_uuid).execute()
        supabase.table("cohort_retention").delete().neq('id', null_uuid).execute()
        print("  ✓ Tables cleared")
        
        # Insert new data
        print("\n💾 Inserting data...")
        
        print("  → Monthly revenue...")
        supabase.table("monthly_revenue").insert(monthly_data).execute()
        
        print("  → Revenue by plan...")
        supabase.table("revenue_by_plan").insert(plan_data).execute()
        
        print("  → Cohort retention...")
        supabase.table("cohort_retention").insert(cohort_data).execute()
        
        # Success summary
        print("\n" + "=" * 60)
        print("✨ Database seeded successfully!")
        print("=" * 60)
        
        print("\n📈 Sample metrics from latest month:")
        latest = monthly_data[-1]
        print(f"  • MRR: ${latest['mrr']:,.2f}")
        print(f"  • Customers: {latest['customer_count']:,}")
        print(f"  • New Customers: {latest['new_customers']}")
        print(f"  • Churned: {latest['churn_count']}")
        
        print("\n🚀 Ready to launch!")
        print("   Run: streamlit run app.py")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ Error: {str(e)}")
        print("=" * 60)
        print("\n💡 Troubleshooting:")
        print("  1. Run schema.sql in Supabase SQL Editor")
        print("  2. Check .env has SUPABASE_URL and SUPABASE_KEY")
        print("  3. Verify Supabase project is active")
        print("=" * 60)
        return False


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    seed_database()
