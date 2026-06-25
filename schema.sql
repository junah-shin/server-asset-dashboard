-- ============================================================================
-- Server Asset Management Dashboard - Database Schema
-- ============================================================================
--
-- Instructions:
-- 1. Go to your Supabase project dashboard
-- 2. Navigate to SQL Editor
-- 3. Copy and paste this entire file
-- 4. Click "Run" to create the table and insert sample data
--
-- ============================================================================

-- ----------------------------------------------------------------------------
-- SERVER INVENTORY TABLE
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS server_inventory (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    location VARCHAR(10) NOT NULL CHECK (location IN ('IDC', 'HQ')),
    env VARCHAR(10) NOT NULL CHECK (env IN ('PRD', 'STG', 'DEV')),
    hostname VARCHAR(255) NOT NULL,
    ip VARCHAR(45) NOT NULL,
    owner VARCHAR(100) NOT NULL,
    status VARCHAR(10) NOT NULL CHECK (status IN ('정상', '장애', '점검')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- ----------------------------------------------------------------------------
-- INDEXES
-- ----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_server_inventory_location ON server_inventory(location);
CREATE INDEX IF NOT EXISTS idx_server_inventory_env ON server_inventory(env);
CREATE INDEX IF NOT EXISTS idx_server_inventory_status ON server_inventory(status);
CREATE INDEX IF NOT EXISTS idx_server_inventory_hostname ON server_inventory(hostname);

-- ----------------------------------------------------------------------------
-- TRIGGER: AUTO-UPDATE updated_at
-- ----------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = TIMEZONE('utc', NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_server_inventory_updated_at
    BEFORE UPDATE ON server_inventory
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ----------------------------------------------------------------------------
-- ROW LEVEL SECURITY (Optional)
-- ----------------------------------------------------------------------------
ALTER TABLE server_inventory ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow authenticated read" ON server_inventory
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "Allow authenticated insert" ON server_inventory
    FOR INSERT TO authenticated WITH CHECK (true);

CREATE POLICY "Allow authenticated update" ON server_inventory
    FOR UPDATE TO authenticated USING (true);

CREATE POLICY "Allow authenticated delete" ON server_inventory
    FOR DELETE TO authenticated USING (true);

-- ----------------------------------------------------------------------------
-- SAMPLE DATA
-- ----------------------------------------------------------------------------
INSERT INTO server_inventory (location, env, hostname, ip, owner, status) VALUES
    -- IDC PRD
    ('IDC', 'PRD', 'web-prd-01', '10.10.1.11', '김민수', '정상'),
    ('IDC', 'PRD', 'web-prd-02', '10.10.1.12', '김민수', '정상'),
    ('IDC', 'PRD', 'api-prd-01', '10.10.1.21', '이영희', '정상'),
    ('IDC', 'PRD', 'api-prd-02', '10.10.1.22', '이영희', '장애'),
    ('IDC', 'PRD', 'db-prd-01', '10.10.1.31', '박정호', '정상'),
    ('IDC', 'PRD', 'db-prd-02', '10.10.1.32', '박정호', '정상'),
    ('IDC', 'PRD', 'cache-prd-01', '10.10.1.41', '최서연', '점검'),
    -- IDC STG
    ('IDC', 'STG', 'web-stg-01', '10.10.2.11', '김민수', '정상'),
    ('IDC', 'STG', 'api-stg-01', '10.10.2.21', '이영희', '정상'),
    ('IDC', 'STG', 'db-stg-01', '10.10.2.31', '박정호', '정상'),
    -- IDC DEV
    ('IDC', 'DEV', 'web-dev-01', '10.10.3.11', '한지우', '정상'),
    ('IDC', 'DEV', 'api-dev-01', '10.10.3.21', '한지우', '정상'),
    ('IDC', 'DEV', 'db-dev-01', '10.10.3.31', '정다은', '점검'),
    -- HQ PRD
    ('HQ', 'PRD', 'erp-prd-01', '192.168.1.11', '오승훈', '정상'),
    ('HQ', 'PRD', 'mail-prd-01', '192.168.1.21', '오승훈', '정상'),
    ('HQ', 'PRD', 'file-prd-01', '192.168.1.31', '윤하늘', '장애'),
    -- HQ STG
    ('HQ', 'STG', 'erp-stg-01', '192.168.2.11', '오승훈', '정상'),
    ('HQ', 'STG', 'mail-stg-01', '192.168.2.21', '윤하늘', '정상'),
    -- HQ DEV
    ('HQ', 'DEV', 'erp-dev-01', '192.168.3.11', '정다은', '정상'),
    ('HQ', 'DEV', 'test-dev-01', '192.168.3.21', '한지우', '정상');

-- ============================================================================
-- DONE!
-- ============================================================================
--
-- Next Steps:
-- 1. Set up .env with your Supabase credentials
-- 2. Launch dashboard: streamlit run app.py
--
-- ============================================================================
