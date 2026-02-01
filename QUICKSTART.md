# ⚡ Quick Start - Get Running in 10 Minutes

The absolute fastest path from download to working dashboard.

---

## Prerequisites

- ✅ Python 3.11+ installed ([Download](https://www.python.org/downloads/))
- ✅ A free Supabase account ([Sign up](https://supabase.com))
- ✅ A free Anthropic account ([Sign up](https://console.anthropic.com/))

**Have those ready? Let's go!** ⏱️

---

## Step 1: Install (2 minutes)

```bash
# Unzip the download
cd saas-dashboard-template

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

✅ **Installed!**

---

## Step 2: Supabase Setup (3 minutes)

### 2a. Create Project

1. Go to [app.supabase.com](https://app.supabase.com)
2. Click **"New Project"**
3. Fill in:
   - **Name**: my-saas-dashboard
   - **Database Password**: (generate strong password, save it!)
   - **Region**: (closest to you)
4. Click **"Create new project"**
5. ⏱️ Wait 2-3 minutes while it sets up

### 2b. Run Database Schema

1. In Supabase, click **"SQL Editor"** (left sidebar)
2. Click **"New query"**
3. Open `schema.sql` from the template
4. **Copy all the SQL** and paste into the editor
5. Click **"Run"**
6. ✅ You should see: "Success. No rows returned"

### 2c. Get Your Credentials

1. Click **"Settings"** → **"API"**
2. Copy these two values:
   - **Project URL** (looks like `https://abc123.supabase.co`)
   - **anon/public** key (the long string under "Project API keys")

✅ **Supabase ready!**

---

## Step 3: Get Claude API Key (1 minute)

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign up/login
3. Click **"API Keys"**
4. Click **"Create Key"**
5. Give it a name: "SaaS Dashboard"
6. Copy the key (starts with `sk-ant-api03-...`)

You get **$5 free credits** - plenty to test!

✅ **API key ready!**

---

## Step 4: Configure (1 minute)

```bash
# Copy the example file
cp .env.example .env

# Edit with your values
nano .env  # or use any text editor
```

Paste your credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

Save and close.

✅ **Configured!**

---

## Step 5: Generate Demo Data (30 seconds)

```bash
python seed_data.py
```

You should see:

```
🌱 Starting database seeding...
✅ Connected to Supabase
📊 Generating sample data...
  ✓ 12 monthly revenue records
  ✓ 36 plan breakdown records
  ✓ 36 cohort retention records
✨ Database seeded successfully!
```

✅ **Data loaded!**

---

## Step 6: Launch! (10 seconds)

```bash
streamlit run app.py
```

You should see:

```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

**Open that URL in your browser!** 🎉

✅ **Running!**

---

## Step 7: Create Your Account

1. Click the **"Sign Up"** tab
2. Enter your email and password (min. 6 characters)
3. Click **"Create Account"**
4. Check your email for the verification link
5. Click the link to verify
6. Return to the dashboard and **login**

**You're in!** 🚀

---

## What You'll See

- **4 key metrics** at the top
- **MRR trend chart** (12 months)
- **Customer growth chart**
- **Navigation sidebar** with 4 sections
- **AI insights button** - try asking "What's my growth rate?"

All with **12 months of realistic sample data**!

---

## Common Issues

### "Module not found" error
→ Make sure you activated the virtual environment:
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### "Supabase credentials not found"
→ Check that `.env` file exists and has your URL and key

### "No data available"
→ Run `python seed_data.py` again

### Charts not showing
→ Try refreshing the page (Cmd+R or Ctrl+R)

### Can't login after signup
→ Check your email for the verification link first

---

## Next Steps

### 1. Explore the Dashboard
- Click through all 4 navigation sections
- Try the AI insights (ask a question!)
- Check out the cohort retention heatmap

### 2. Customize Your Branding
- Edit `assets/style.css` to change colors
- Update `app.py` to change the title and icon
- See `CUSTOMIZATION.md` for full guide

### 3. Connect Real Data
- Replace the seed data with your actual metrics
- Hook up to Stripe, your database, etc.
- See `README.md` for integration guides

### 4. Deploy to Production
- Use Streamlit Cloud (free tier)
- Or deploy to Heroku, DigitalOcean, etc.
- See `DEPLOYMENT.md` for instructions

---

## Help & Support

**Need help?**
- 📧 Email: support@yourcompany.com
- 💬 GitHub: Open an issue
- 📖 Docs: See `README.md` and `CUSTOMIZATION.md`

---

**That's it! You're running a production-quality SaaS dashboard in under 10 minutes.** ⚡

Now make it yours! 🎨
