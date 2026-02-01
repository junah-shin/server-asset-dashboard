# 🎨 Customization Guide

Complete guide to customizing your SaaS Dashboard Template.

---

## Table of Contents

1. [Branding & Colors](#branding--colors)
2. [Plan Tiers & Pricing](#plan-tiers--pricing)
3. [Adding New Metrics](#adding-new-metrics)
4. [Custom Charts](#custom-charts)
5. [Database Schema Changes](#database-schema-changes)
6. [Authentication Customization](#authentication-customization)
7. [AI Prompts & Behavior](#ai-prompts--behavior)
8. [Deployment Configuration](#deployment-configuration)

---

## Branding & Colors

### Change Primary Color

Edit `assets/style.css`:

```css
/* Find and replace all instances of #00C853 (green) with your brand color */
#00C853 → #YOUR_BRAND_COLOR

/* Example: Change to purple */
#00C853 → #9C27B0
```

### Change App Title & Icon

Edit `app.py`:

```python
st.set_page_config(
    page_title="Your Company Dashboard",  # Browser tab title
    page_icon="🚀",  # Emoji or path to .ico file
    layout="wide"
)
```

### Add Logo

1. Add your logo to `assets/logo.png`
2. Edit `app.py` sidebar:

```python
with st.sidebar:
    st.image("assets/logo.png", width=200)
    st.title("Dashboard")
```

### Customize Fonts

Edit `assets/style.css`:

```css
/* Add at the top */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

/* Apply to body */
* {
    font-family: 'Inter', sans-serif;
}
```

---

## Plan Tiers & Pricing

### Change Plan Names

**1. Update seed data** (`seed_data.py`):

```python
PLAN_PRICES = {
    'basic': 19,      # Renamed from 'starter'
    'premium': 79,    # Renamed from 'pro'
    'ultimate': 199   # Renamed from 'enterprise'
}
```

**2. Update database:**

```sql
-- In Supabase SQL Editor:
UPDATE revenue_by_plan SET plan_tier = 'basic' WHERE plan_tier = 'starter';
UPDATE revenue_by_plan SET plan_tier = 'premium' WHERE plan_tier = 'pro';
UPDATE revenue_by_plan SET plan_tier = 'ultimate' WHERE plan_tier = 'enterprise';

UPDATE customers SET plan_tier = 'basic' WHERE plan_tier = 'starter';
-- Repeat for other tiers
```

**3. Update chart colors** (`utils/charts.py`):

```python
def create_plan_revenue_chart(df: pd.DataFrame):
    # ...
    marker=dict(colors=['#FF5722', '#2196F3', '#9C27B0'])  # Match your brand
```

### Add a 4th Plan Tier

**1. Update schema** (Supabase SQL Editor):

```sql
-- No schema change needed, plan_tier is VARCHAR
-- Just start inserting new tier data
```

**2. Update seed script:**

```python
PLAN_PRICES = {
    'starter': 29,
    'pro': 99,
    'enterprise': 299,
    'platinum': 599  # New tier
}

# Update distribution in generate_plan_data():
starter_customers = int(total_customers * 0.40)
pro_customers = int(total_customers * 0.30)
enterprise_customers = int(total_customers * 0.20)
platinum_customers = total_customers - starter_customers - pro_customers - enterprise_customers

# Add platinum data
plan_data.append({
    'month': month_data['month'],
    'plan_tier': 'platinum',
    'revenue': round(platinum_revenue, 2),
    'customer_count': platinum_customers
})
```

**3. Update chart colors:**

```python
marker=dict(colors=['#00C853', '#2196F3', '#FF9800', '#9C27B0'])  # 4 colors
```

---

## Adding New Metrics

### Example: Add Customer Lifetime Value (LTV)

**Step 1: Update Database Schema**

```sql
-- Add to monthly_revenue table
ALTER TABLE monthly_revenue
ADD COLUMN avg_ltv DECIMAL(10, 2);

-- Backfill with sample data
UPDATE monthly_revenue
SET avg_ltv = mrr / customer_count * 24  -- Simple LTV = MRR per customer * 24 months
WHERE customer_count > 0;
```

**Step 2: Update Database Query** (`utils/database.py`):

```python
def get_ltv_data(supabase: Client, months: int = 12) -> pd.DataFrame:
    """Fetch LTV data."""
    try:
        response = supabase.table("monthly_revenue")\
            .select("month, avg_ltv, customer_count")\
            .order("month", desc=True)\
            .limit(months)\
            .execute()
        
        df = pd.DataFrame(response.data)
        if not df.empty:
            df['month'] = pd.to_datetime(df['month'])
            df = df.sort_values('month')
        return df
    except Exception as e:
        st.error(f"Error fetching LTV data: {str(e)}")
        return pd.DataFrame()
```

**Step 3: Create Chart** (`utils/charts.py`):

```python
def create_ltv_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """Create LTV trend chart."""
    if df.empty:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['month'],
        y=df['avg_ltv'],
        mode='lines+markers',
        name='Avg LTV',
        line=dict(color='#9C27B0', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Average Customer Lifetime Value',
        xaxis_title='Month',
        yaxis_title='LTV ($)',
        height=400,
        # ... copy layout from other charts
    )
    
    return fig
```

**Step 4: Add to Dashboard** (`app.py`):

```python
def show_overview_page(metrics, revenue_df, plan_df):
    # ... existing metrics ...
    
    col5, col6 = st.columns(2)
    with col5:
        ltv_df = get_ltv_data(supabase, months=12)
        ltv_chart = create_ltv_chart(ltv_df)
        if ltv_chart:
            st.plotly_chart(ltv_chart, use_container_width=True)
```

---

## Custom Charts

### Add a New Chart Type: Waterfall Chart

```python
# In utils/charts.py

def create_mrr_waterfall_chart(df: pd.DataFrame) -> Optional[go.Figure]:
    """Show MRR changes as waterfall (new, churn, net)."""
    if df.empty or len(df) < 2:
        return None
    
    # Calculate components
    df_copy = df.copy()
    df_copy['new_mrr'] = df_copy['new_customers'] * 99  # Avg price
    df_copy['churn_mrr'] = df_copy['churn_count'] * -99
    df_copy['net_new'] = df_copy['new_mrr'] + df_copy['churn_mrr']
    
    fig = go.Figure(go.Waterfall(
        x=df_copy['month'],
        y=df_copy['net_new'],
        measure=["relative"] * len(df_copy),
        text=[f"+${x:,.0f}" if x > 0 else f"-${abs(x):,.0f}" for x in df_copy['net_new']],
        connector={"line": {"color": "rgb(63, 63, 63)"}},
    ))
    
    fig.update_layout(
        title="MRR Net New (Waterfall)",
        showlegend=False,
        # ... standard layout
    )
    
    return fig
```

### Add Comparison Chart (This Month vs Last Month)

```python
def create_comparison_chart(current: dict, previous: dict) -> go.Figure:
    """Bar chart comparing current vs previous month."""
    metrics = ['MRR', 'Customers', 'New Customers']
    current_values = [current['mrr'], current['customers'], current['new_customers']]
    previous_values = [previous['mrr'], previous['customers'], previous['new_customers']]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Last Month', x=metrics, y=previous_values, marker_color='#64B5F6'))
    fig.add_trace(go.Bar(name='This Month', x=metrics, y=current_values, marker_color='#00C853'))
    
    fig.update_layout(
        title='Month-over-Month Comparison',
        barmode='group',
        # ... layout
    )
    
    return fig
```

---

## Database Schema Changes

### Add a New Table: User Activity Logs

```sql
CREATE TABLE IF NOT EXISTS user_activity (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id),
    action VARCHAR(100) NOT NULL,  -- 'login', 'view_dashboard', 'export_data'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

CREATE INDEX idx_user_activity_user_id ON user_activity(user_id);
CREATE INDEX idx_user_activity_created_at ON user_activity(created_at);
```

### Track It in Your App:

```python
# In utils/database.py

def log_user_activity(supabase: Client, action: str):
    """Log user activity."""
    try:
        user = st.session_state.get('user')
        if user:
            supabase.table("user_activity").insert({
                'user_id': user.id,
                'action': action
            }).execute()
    except Exception as e:
        # Silent fail - don't break UX for logging errors
        pass

# In app.py, track page views:
def show_overview_page(...):
    log_user_activity(supabase, 'view_overview')
    # ... rest of page
```

---

## Authentication Customization

### Add Password Reset

```python
# In app.py, add to login page:

def show_login_page():
    # ... existing tabs ...
    
    st.markdown("---")
    st.markdown("### Forgot Password?")
    
    with st.form("password_reset_form"):
        email = st.text_input("Email")
        submit = st.form_submit_button("Send Reset Link")
        
        if submit and email:
            if request_password_reset(email):  # Already in utils/auth.py
                st.success("Check your email for reset instructions")
```

### Add OAuth (Google, GitHub)

Supabase supports OAuth. Configure in Supabase dashboard:

1. Go to **Authentication → Providers**
2. Enable Google/GitHub
3. Add credentials

Then in `utils/auth.py`:

```python
def login_with_google():
    """Initiate Google OAuth flow."""
    supabase = get_supabase_client()
    response = supabase.auth.sign_in_with_oauth({
        "provider": "google",
        "options": {
            "redirect_to": "http://localhost:8501"
        }
    })
    return response.url  # Redirect user to this URL

# In app.py:
if st.button("Login with Google"):
    oauth_url = login_with_google()
    st.markdown(f'<meta http-equiv="refresh" content="0;url={oauth_url}">', unsafe_allow_html=True)
```

---

## AI Prompts & Behavior

### Customize AI Summary Tone

Edit `utils/ai_insights.py`:

```python
def generate_executive_summary(metrics, revenue_df):
    context = f"""
You are a friendly, optimistic business advisor helping a founder understand their SaaS metrics.

[... existing context ...]

Tone: Encouraging but honest. Celebrate wins. Frame challenges as opportunities.
Format: 2-3 sentences. Start with a headline-style observation.
"""
```

### Add Custom AI Functions

```python
def generate_growth_recommendations(metrics: dict, revenue_df: pd.DataFrame) -> str:
    """Get AI recommendations for improving growth."""
    client = get_claude_client()
    if not client:
        return "AI unavailable"
    
    context = f"""
Based on these metrics, provide 3 specific, actionable recommendations to improve growth:

Metrics:
- MRR: ${metrics['mrr']:,.0f} ({metrics['mrr_growth']:+.1f}%)
- Customers: {metrics['customers']} ({metrics['customer_growth']:+.1f}%)
- Churn: {metrics['churn_rate']:.1f}%

Format: Numbered list, 1-2 sentences each.
"""
    
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=300,
        messages=[{"role": "user", "content": context}]
    )
    return message.content[0].text

# Use in dashboard:
st.subheader("Growth Recommendations")
recs = generate_growth_recommendations(metrics, revenue_df)
st.info(recs)
```

---

## Deployment Configuration

### Environment-Specific Settings

Create `config.py`:

```python
import os

class Config:
    # Detect environment
    IS_PRODUCTION = os.getenv("ENVIRONMENT") == "production"
    
    # Feature flags
    ENABLE_AI = os.getenv("ENABLE_AI", "true").lower() == "true"
    ENABLE_SIGNUP = os.getenv("ENABLE_SIGNUP", "true").lower() == "true"
    
    # Branding
    APP_NAME = os.getenv("APP_NAME", "SaaS Dashboard")
    SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", "support@yourcompany.com")
    
    # Rate limiting (if implemented)
    MAX_API_CALLS_PER_HOUR = 100 if IS_PRODUCTION else 1000

# Use in app.py:
from config import Config

if Config.ENABLE_AI:
    show_ai_insights_page()
else:
    st.info("AI features disabled")
```

### Add Docker Support

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  dashboard:
    build: .
    ports:
      - "8501:8501"
    env_file:
      - .env
    restart: unless-stopped
```

Run with: `docker-compose up`

---

## Advanced Customizations

### Multi-Tenancy (Multiple Companies)

1. **Add company_id to all tables:**

```sql
ALTER TABLE monthly_revenue ADD COLUMN company_id UUID;
ALTER TABLE customers ADD COLUMN company_id UUID;
-- etc.

-- Link to auth
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255),
    owner_id UUID REFERENCES auth.users(id)
);
```

2. **Enable Supabase RLS:**

```sql
ALTER TABLE monthly_revenue ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view their company's data"
    ON monthly_revenue FOR SELECT
    USING (company_id IN (
        SELECT company_id FROM user_companies WHERE user_id = auth.uid()
    ));
```

3. **Update all queries to filter by company:**

```python
def get_monthly_revenue(supabase, company_id, months=12):
    response = supabase.table("monthly_revenue")\
        .select("*")\
        .eq("company_id", company_id)\
        .order("month", desc=True)\
        .limit(months)\
        .execute()
```

---

## Need Help?

- 📧 **Email Support**: support@yourcompany.com
- 💬 **GitHub Issues**: Open an issue for bugs or questions
- 📖 **Streamlit Docs**: https://docs.streamlit.io
- 🗄️ **Supabase Docs**: https://supabase.com/docs

---

**Pro Tip**: Start with small customizations (colors, branding) before making major changes (new metrics, multi-tenancy). Test thoroughly after each change!
