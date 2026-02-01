-- ============================================================================
-- SaaS Dashboard Database Schema
-- ============================================================================
-- 
-- Instructions:
-- 1. Go to your Supabase project dashboard
-- 2. Navigate to SQL Editor
-- 3. Copy and paste this entire file
-- 4. Click "Run" to create all tables
--
-- Tables Created:
-- - customers: User accounts and subscription info
-- - monthly_revenue: Aggregated monthly metrics
-- - revenue_by_plan: Revenue breakdown by tier
-- - cohort_retention: Customer retention analysis
--
-- ============================================================================

-- ----------------------------------------------------------------------------
-- CUSTOMERS TABLE
-- Stores individual customer records
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    signup_date DATE NOT NULL,
    plan_tier VARCHAR(50) NOT NULL, -- 'starter', 'pro', 'enterprise'
    status VARCHAR(50) NOT NULL DEFAULT 'active', -- 'active', 'churned', 'paused'
    churn_date DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- ----------------------------------------------------------------------------
-- MONTHLY REVENUE TABLE
-- Aggregated metrics by month
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS monthly_revenue (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    month DATE NOT NULL,
    mrr DECIMAL(10, 2) NOT NULL, -- Monthly Recurring Revenue
    customer_count INTEGER NOT NULL, -- Total active customers
    churn_count INTEGER DEFAULT 0, -- Customers lost this month
    new_customers INTEGER DEFAULT 0, -- New signups this month
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    UNIQUE(month)
);

-- ----------------------------------------------------------------------------
-- REVENUE BY PLAN TABLE
-- Monthly revenue breakdown by plan tier
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS revenue_by_plan (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    month DATE NOT NULL,
    plan_tier VARCHAR(50) NOT NULL, -- 'starter', 'pro', 'enterprise'
    revenue DECIMAL(10, 2) NOT NULL, -- Revenue from this plan tier
    customer_count INTEGER NOT NULL, -- Customers on this plan
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    UNIQUE(month, plan_tier)
);

-- ----------------------------------------------------------------------------
-- COHORT RETENTION TABLE
-- Track how well cohorts retain over time
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cohort_retention (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cohort_month DATE NOT NULL, -- Month when cohort signed up
    month_number INTEGER NOT NULL, -- 0 = signup month, 1 = 1 month later, etc.
    customers_remaining INTEGER NOT NULL, -- Active customers from this cohort
    retention_rate DECIMAL(5, 2) NOT NULL, -- Percentage still active (0-100)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    UNIQUE(cohort_month, month_number)
);

-- ----------------------------------------------------------------------------
-- INDEXES FOR PERFORMANCE
-- These speed up common queries
-- ----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_customers_signup_date ON customers(signup_date);
CREATE INDEX IF NOT EXISTS idx_customers_status ON customers(status);
CREATE INDEX IF NOT EXISTS idx_customers_plan_tier ON customers(plan_tier);
CREATE INDEX IF NOT EXISTS idx_monthly_revenue_month ON monthly_revenue(month);
CREATE INDEX IF NOT EXISTS idx_revenue_by_plan_month ON revenue_by_plan(month);
CREATE INDEX IF NOT EXISTS idx_cohort_retention_cohort ON cohort_retention(cohort_month);

-- ----------------------------------------------------------------------------
-- TRIGGERS FOR UPDATED_AT TIMESTAMPS
-- Automatically update 'updated_at' when rows change
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all tables
CREATE TRIGGER update_customers_updated_at BEFORE UPDATE ON customers
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_monthly_revenue_updated_at BEFORE UPDATE ON monthly_revenue
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_revenue_by_plan_updated_at BEFORE UPDATE ON revenue_by_plan
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_cohort_retention_updated_at BEFORE UPDATE ON cohort_retention
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- DONE!
-- ============================================================================
-- 
-- Next Steps:
-- 1. Run the seed_data.py script to populate sample data
-- 2. Launch your dashboard with: streamlit run app.py
--
-- Optional: Add Row Level Security (RLS) for multi-tenancy
-- See Supabase docs: https://supabase.com/docs/guides/auth/row-level-security
--
-- ============================================================================
