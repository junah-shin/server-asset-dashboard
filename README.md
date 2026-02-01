# 📊 SaaS Dashboard Template

> **Production-ready Streamlit template for SaaS metrics visualization**

A beautiful, fully-functional SaaS analytics dashboard that you can have running in under 10 minutes. Perfect for indie hackers, startup founders, and SaaS businesses who need professional metrics tracking without the complexity.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11+-blue)

---

## ✨ Features

### 🔐 **Complete Authentication**
- Supabase email/password authentication
- Secure session management
- User registration with email verification
- Password reset functionality (optional)

### 📈 **SaaS Metrics Tracking**
- **MRR (Monthly Recurring Revenue)** with growth trends
- **Customer Count** with growth rates
- **Churn Rate** analysis and visualization
- **Plan Tier Breakdown** (Starter/Pro/Enterprise)
- **Cohort Retention** heatmaps
- **New Customer** acquisition tracking

### 🤖 **AI-Powered Insights**
- Executive summary generation via Claude API
- Natural language metric queries
- Trend analysis and recommendations
- "Ask your dashboard" functionality

### 🎨 **Professional UI/UX**
- Beautiful dark theme
- Responsive design (works on mobile)
- Interactive Plotly charts
- Custom CSS styling
- Clean, modern interface

### 🛠️ **Developer-Friendly**
- Well-documented code
- Modular architecture
- Easy customization
- Production-ready structure
- Demo data generator included

---

## 🚀 Quick Start (10 Minutes)

### Prerequisites

- Python 3.11 or higher
- A [Supabase](https://supabase.com) account (free tier works!)
- An [Anthropic API key](https://console.anthropic.com/) (for AI features)

### Step 1: Clone & Install

```bash
# Clone the repository
git clone https://github.com/yourusername/saas-dashboard-template.git
cd saas-dashboard-template

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for the project to finish setting up (2-3 minutes)
3. Go to **SQL Editor** in your Supabase dashboard
4. Copy the contents of `schema.sql` and paste it into the editor
5. Click **Run** to create all tables

### Step 3: Get Your Credentials

**Supabase:**
1. In your Supabase project, go to **Settings → API**
2. Copy your **Project URL**
3. Copy your **anon/public key**

**Anthropic:**
1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up or log in
3. Navigate to **API Keys**
4. Create a new API key

### Step 4: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, etc.
```

Add your credentials:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
ANTHROPIC_API_KEY=sk-ant-api03-...
```

### Step 5: Seed Sample Data

```bash
# Generate 12 months of realistic sample data
python seed_data.py
```

You should see:
```
🌱 Starting database seeding...
✅ Connected to Supabase
📊 Generating sample data...
✨ Database seeded successfully!
```

### Step 6: Launch Dashboard

```bash
streamlit run app.py
```

Visit `http://localhost:8501` in your browser. **You're live!** 🎉

### Step 7: Create Your First User

1. Click the **"Sign Up"** tab
2. Enter your email and password (minimum 6 characters)
3. Check your email for the verification link
4. Click the verification link
5. Return to the dashboard and log in

---

## 📖 Usage Guide

### Dashboard Navigation

The dashboard has four main sections:

#### 1. **Overview**
- High-level KPIs at a glance
- MRR and customer growth charts
- Quick performance summary

#### 2. **Revenue Analytics**
- Detailed MRR trend analysis
- Revenue breakdown by plan tier
- Plan distribution table

#### 3. **Customer Insights**
- Customer growth visualization
- Churn rate analysis
- Cohort retention heatmap

#### 4. **AI Insights**
- Executive summary generation
- Natural language queries
- Ask questions like:
  - "What's driving my revenue growth?"
  - "Should I be worried about churn?"
  - "Which plan tier is most profitable?"

---

## 🗂️ Project Structure

```
saas-dashboard-template/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── schema.sql                # Database schema (run in Supabase)
├── seed_data.py              # Sample data generator
├── README.md                 # This file
├── CUSTOMIZATION.md          # Customization guide
├── LICENSE                   # MIT License
│
├── utils/                    # Utility modules
│   ├── __init__.py
│   ├── auth.py              # Authentication logic
│   ├── database.py          # Database queries
│   ├── charts.py            # Plotly chart generation
│   └── ai_insights.py       # Claude AI integration
│
├── assets/                   # Static assets
│   └── style.css            # Custom CSS theme
│
└── docs/                     # Additional documentation
    └── DEPLOYMENT.md        # Deployment guide (optional)
```

---

## 🎨 Customization

### Change Brand Colors

Edit `assets/style.css`:

```css
/* Primary color (green) */
#00C853 → #YOUR_COLOR

/* Accent colors */
#2196F3 → #YOUR_BLUE
#FF9800 → #YOUR_ORANGE
```

### Modify Plan Tiers

Edit `seed_data.py`:

```python
PLAN_PRICES = {
    'basic': 19,      # Change names and prices
    'premium': 79,
    'ultimate': 199
}
```

Update database queries in `utils/database.py` to match.

### Add New Metrics

1. Update database schema in `schema.sql`
2. Add queries in `utils/database.py`
3. Create chart functions in `utils/charts.py`
4. Add new page in `app.py`

See `CUSTOMIZATION.md` for detailed instructions.

---

## 🚢 Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add secrets in the app settings:
   ```
   SUPABASE_URL = "your_url"
   SUPABASE_KEY = "your_key"
   ANTHROPIC_API_KEY = "your_key"
   ```
5. Deploy!

### Other Platforms

- **Heroku**: Use the included `Procfile`
- **DigitalOcean**: Deploy as a web service
- **AWS/GCP**: Run on EC2/Compute Engine
- **Docker**: Containerize with provided `Dockerfile`

---

## 🔒 Security Best Practices

### Essential Security Steps

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Enable Row Level Security (RLS)** in Supabase for multi-tenancy
3. **Rotate API keys** if accidentally exposed
4. **Use environment variables** for all secrets
5. **Enable email verification** in Supabase settings

### Production Checklist

- [ ] Set up SSL/HTTPS
- [ ] Enable Supabase RLS policies
- [ ] Use strong password requirements
- [ ] Implement rate limiting
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Review Supabase auth settings

---

## 📊 Metrics Tracked

| Metric | Description | Calculation |
|--------|-------------|-------------|
| **MRR** | Monthly Recurring Revenue | Sum of all active subscriptions |
| **Customer Count** | Total active customers | Count of non-churned users |
| **Churn Rate** | % of customers lost | (Churned / Total) × 100 |
| **Cohort Retention** | % retained by signup month | (Active / Initial) × 100 per cohort |
| **Plan Breakdown** | Revenue by tier | Sum per plan (Starter/Pro/Enterprise) |
| **New Customers** | Monthly acquisitions | Count of new signups |

---

## 💰 Cost Breakdown

### Free Tier Usage

- **Supabase**: 500MB database, 2GB transfer/month (Free forever)
- **Streamlit Cloud**: 1 private app (Free)
- **Anthropic Claude**: $5 free credits (then pay-as-you-go)

### Typical Monthly Costs (after free tier)

- **Supabase**: $0-25 (upgrade if you exceed 500MB)
- **Claude API**: $1-5 (for AI insights, very affordable)
- **Hosting**: $0 (Streamlit Cloud free tier)

**Total**: $1-30/month depending on usage

Compare to alternatives:
- ChartMogul: $100/month
- Baremetrics: $108/month
- ProfitWell: $0 (but limited features)

---

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|------------|---------|---------|
| **Streamlit** | Web framework | 1.31+ |
| **Supabase** | Database & Auth | PostgreSQL |
| **Anthropic Claude** | AI insights | API v1 |
| **Plotly** | Interactive charts | 5.18+ |
| **Pandas** | Data processing | 2.1+ |
| **Python** | Backend | 3.11+ |

---

## 🆘 Troubleshooting

### "No data available"
→ Run `python seed_data.py` to generate sample data

### "Supabase credentials not found"
→ Check that `.env` file exists and has valid `SUPABASE_URL` and `SUPABASE_KEY`

### "Login failed"
→ Check your email for the verification link from Supabase

### Charts not displaying
→ Ensure data exists in database and tables were created via `schema.sql`

### AI insights not working
→ Verify `ANTHROPIC_API_KEY` is set in `.env` and has credits

### Import errors
→ Activate virtual environment and run `pip install -r requirements.txt`

---

## 📚 Additional Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [Supabase Documentation](https://supabase.com/docs)
- [Anthropic Claude API Docs](https://docs.anthropic.com)
- [Plotly Python Documentation](https://plotly.com/python/)

---

## 🤝 Contributing

This is a template product, but if you have suggestions:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - See `LICENSE` file for details.

You have full rights to:
- ✅ Use commercially
- ✅ Modify and customize
- ✅ Distribute
- ✅ Private use

No attribution required (but appreciated!)

---

## 🙏 Support

**Questions? Issues?**

- 📧 Email: support@yourcompany.com
- 💬 GitHub Issues: [Create an issue](https://github.com/yourusername/saas-dashboard-template/issues)
- 📖 Documentation: See `CUSTOMIZATION.md` for advanced topics

---

## 🌟 What's Next?

Once you're comfortable with the template:

1. **Connect real data** - Replace sample data with your actual SaaS metrics
2. **Add more metrics** - LTV, CAC, runway, burn rate
3. **Customize styling** - Match your brand colors
4. **Deploy to production** - Use Streamlit Cloud or your preferred platform
5. **Add features** - Email reports, Slack notifications, exports

---

**Built for indie makers and startup founders who need beautiful analytics without the complexity.**

Got questions? Want to share your customization? Open an issue or PR!

⭐ If this saved you time, consider starring the repo!
