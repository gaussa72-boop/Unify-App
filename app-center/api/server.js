require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 10000;
const JWT_SECRET = process.env.JWT_SECRET;
const DATABASE_URL = process.env.DATABASE_URL;
const SUPERADMIN_EMAIL = (process.env.SUPERADMIN_EMAIL || '').trim().toLowerCase();
const APP_ORIGIN = process.env.APP_ORIGIN || 'https://astralis-app-center.onrender.com';
const pool = new Pool({ connectionString: DATABASE_URL, ssl: process.env.NODE_ENV === 'production' ? { rejectUnauthorized: false } : false });

if (!JWT_SECRET || JWT_SECRET.length < 32) throw new Error('JWT_SECRET must be set to a random value of at least 32 characters.');
if (!DATABASE_URL) throw new Error('DATABASE_URL is required.');

app.set('trust proxy', 1);
app.use(helmet());
app.use(cors({ origin: [APP_ORIGIN], methods: ['GET','POST','PUT','DELETE'], allowedHeaders: ['Content-Type','Authorization'] }));
app.use(express.json({ limit: '32kb' }));
app.use('/api/', rateLimit({ windowMs: 15 * 60 * 1000, limit: 180, standardHeaders: 'draft-7', legacyHeaders: false }));

const wallets = {
  BTC: { network: 'Bitcoin Mainnet', address: 'bc1q4q7lujkr8mcv9e7suet524uxjfwlaxm7aelq5y' },
  BNB: { network: 'BNB Smart Chain', address: '0xa1CBD80EE6E1050312f346B2341faC46Be5e5a7d' }
};

async function init() {
  const sql = fs.readFileSync(path.join(__dirname, 'schema.sql'), 'utf8');
  await pool.query(sql);
}
function tokenFor(user) {
  return jwt.sign({ sub: String(user.id), role: user.role }, JWT_SECRET, { expiresIn: '7d', issuer: 'astralis-app-center' });
}
function safeUser(row) {
  return { id: row.id, email: row.email, displayName: row.display_name, role: row.role, premiumStatus: row.premium_status, premiumPaidAt: row.premium_paid_at, createdAt: row.created_at };
}
async function auth(req, res, next) {
  try {
    const raw = (req.headers.authorization || '').replace(/^Bearer\s+/i, '');
    const payload = jwt.verify(raw, JWT_SECRET, { issuer: 'astralis-app-center' });
    const result = await pool.query('SELECT * FROM users WHERE id=$1', [payload.sub]);
    if (!result.rowCount) return res.status(401).json({ error: 'Konto nicht gefunden.' });
    req.user = result.rows[0];
    next();
  } catch { res.status(401).json({ error: 'Bitte erneut anmelden.' }); }
}
function admin(req, res, next) {
  if (req.user.role !== 'superadmin') return res.status(403).json({ error: 'Nur für Superadministratoren.' });
  next();
}
function validUrl(value) {
  try { const u = new URL(value); return ['http:','https:'].includes(u.protocol); } catch { return false; }
}

app.get('/health', async (_req,res) => {
  try { await pool.query('SELECT 1'); res.json({ ok: true, service: 'astralis-app-center-api' }); }
  catch { res.status(503).json({ ok: false }); }
});

app.post('/api/auth/register', async (req,res) => {
  const email = String(req.body.email || '').trim().toLowerCase();
  const displayName = String(req.body.displayName || '').trim().slice(0,80);
  const password = String(req.body.password || '');
  if (!/^\S+@\S+\.\S+$/.test(email) || !displayName || password.length < 12) return res.status(400).json({ error: 'Bitte gültige E-Mail, Namen und ein Passwort mit mindestens 12 Zeichen eingeben.' });
  try {
    const hash = await bcrypt.hash(password, 12);
    const role = email === SUPERADMIN_EMAIL ? 'superadmin' : 'user';
    const result = await pool.query('INSERT INTO users(email,display_name,password_hash,role) VALUES($1,$2,$3,$4) RETURNING *', [email,displayName,hash,role]);
    res.status(201).json({ token: tokenFor(result.rows[0]), user: safeUser(result.rows[0]) });
  } catch (e) {
    if (e.code === '23505') return res.status(409).json({ error: 'Für diese E-Mail gibt es bereits ein Konto.' });
    res.status(500).json({ error: 'Registrierung fehlgeschlagen.' });
  }
});
app.post('/api/auth/login', async (req,res) => {
  const email = String(req.body.email || '').trim().toLowerCase();
  const result = await pool.query('SELECT * FROM users WHERE email=$1', [email]);
  if (!result.rowCount || !(await bcrypt.compare(String(req.body.password || ''), result.rows[0].password_hash))) return res.status(401).json({ error: 'E-Mail oder Passwort falsch.' });
  res.json({ token: tokenFor(result.rows[0]), user: safeUser(result.rows[0]) });
});
app.get('/api/auth/me', auth, (req,res) => res.json({ user: safeUser(req.user) }));

app.get('/api/projects', auth, async (req,res) => {
  const result = await pool.query('SELECT id,name,url,description,platform,repository_url,created_at,updated_at FROM projects WHERE user_id=$1 ORDER BY created_at DESC', [req.user.id]);
  res.json({ projects: result.rows });
});
app.post('/api/projects', auth, async (req,res) => {
  if (req.user.premium_status !== 'active' && req.user.role !== 'superadmin') return res.status(403).json({ error: 'Zum Verwalten eigener Projekte ist Premium erforderlich.' });
  const name = String(req.body.name || '').trim().slice(0,100);
  const url = String(req.body.url || '').trim();
  const description = String(req.body.description || '').trim().slice(0,1000);
  const platform = String(req.body.platform || 'website').slice(0,30);
  const repositoryUrl = String(req.body.repositoryUrl || '').trim();
  if (!name || !validUrl(url) || (repositoryUrl && !validUrl(repositoryUrl))) return res.status(400).json({ error: 'Name und gültige HTTP(S)-Website-URL sind erforderlich.' });
  const result = await pool.query('INSERT INTO projects(user_id,name,url,description,platform,repository_url) VALUES($1,$2,$3,$4,$5,$6) RETURNING *', [req.user.id,name,url,description,platform,repositoryUrl || null]);
  res.status(201).json({ project: result.rows[0] });
});
app.put('/api/projects/:id', auth, async (req,res) => {
  if (req.user.premium_status !== 'active' && req.user.role !== 'superadmin') return res.status(403).json({ error: 'Premium erforderlich.' });
  const name = String(req.body.name || '').trim().slice(0,100), url = String(req.body.url || '').trim();
  const description = String(req.body.description || '').trim().slice(0,1000), platform = String(req.body.platform || 'website').slice(0,30);
  const repositoryUrl = String(req.body.repositoryUrl || '').trim();
  if (!name || !validUrl(url) || (repositoryUrl && !validUrl(repositoryUrl))) return res.status(400).json({ error: 'Ungültige Projektdaten.' });
  const result = await pool.query('UPDATE projects SET name=$1,url=$2,description=$3,platform=$4,repository_url=$5,updated_at=NOW() WHERE id=$6 AND user_id=$7 RETURNING *', [name,url,description,platform,repositoryUrl || null,req.params.id,req.user.id]);
  if (!result.rowCount) return res.status(404).json({ error: 'Projekt nicht gefunden.' });
  res.json({ project: result.rows[0] });
});
app.delete('/api/projects/:id', auth, async (req,res) => {
  const result = await pool.query('DELETE FROM projects WHERE id=$1 AND user_id=$2', [req.params.id,req.user.id]);
  if (!result.rowCount) return res.status(404).json({ error: 'Projekt nicht gefunden.' });
  res.json({ ok: true });
});

app.get('/api/premium/wallets', (_req,res) => res.json({ amountEur: 80, paymentType: 'Einmalzahlung · Lifetime Premium', wallets }));
app.post('/api/premium/submit', auth, async (req,res) => {
  const asset = String(req.body.asset || '').toUpperCase();
  const wallet = wallets[asset];
  const txid = String(req.body.txid || '').trim();
  if (!wallet || txid.length < 20 || txid.length > 160 || !/^[a-zA-Z0-9]+$/.test(txid)) return res.status(400).json({ error: 'Bitte BTC oder BNB und eine gültige Transaktions-ID angeben.' });
  try {
    const result = await pool.query('INSERT INTO payments(user_id,asset,network,txid) VALUES($1,$2,$3,$4) RETURNING id,amount_eur,asset,network,txid,status,submitted_at', [req.user.id,asset,wallet.network,txid]);
    await pool.query("UPDATE users SET premium_status='pending' WHERE id=$1 AND premium_status <> 'active'", [req.user.id]);
    res.status(201).json({ payment: result.rows[0], message: 'Zahlungsnachweis eingereicht. Premium wird erst nach manueller Prüfung freigeschaltet.' });
  } catch (e) {
    if (e.code === '23505') return res.status(409).json({ error: 'Diese Transaktions-ID wurde bereits eingereicht.' });
    res.status(500).json({ error: 'Zahlungsnachweis konnte nicht gespeichert werden.' });
  }
});
app.get('/api/premium/mine', auth, async (req,res) => {
  const result = await pool.query('SELECT id,amount_eur,asset,network,txid,status,submitted_at,reviewed_at FROM payments WHERE user_id=$1 ORDER BY submitted_at DESC', [req.user.id]);
  res.json({ payments: result.rows, premiumStatus: req.user.premium_status });
});

app.get('/api/admin/users', auth, admin, async (_req,res) => {
  const result = await pool.query('SELECT id,email,display_name,role,premium_status,premium_paid_at,created_at FROM users ORDER BY created_at DESC');
  res.json({ users: result.rows });
});
app.get('/api/admin/payments', auth, admin, async (_req,res) => {
  const result = await pool.query('SELECT p.*,u.email,u.display_name FROM payments p JOIN users u ON u.id=p.user_id ORDER BY p.submitted_at DESC');
  res.json({ payments: result.rows });
});
app.post('/api/admin/payments/:id/review', auth, admin, async (req,res) => {
  const status = String(req.body.status || '');
  if (!['approved','rejected'].includes(status)) return res.status(400).json({ error: 'Status muss approved oder rejected sein.' });
  const client = await pool.connect();
  try {
    await client.query('BEGIN');
    const p = await client.query('SELECT * FROM payments WHERE id=$1 FOR UPDATE', [req.params.id]);
    if (!p.rowCount) { await client.query('ROLLBACK'); return res.status(404).json({ error: 'Zahlung nicht gefunden.' }); }
    await client.query('UPDATE payments SET status=$1,reviewed_at=NOW(),reviewed_by=$2 WHERE id=$3', [status,req.user.id,req.params.id]);
    if (status === 'approved') await client.query("UPDATE users SET premium_status='active',premium_paid_at=NOW() WHERE id=$1", [p.rows[0].user_id]);
    else {
      const other = await client.query("SELECT 1 FROM payments WHERE user_id=$1 AND status='approved' AND id<>$2 LIMIT 1", [p.rows[0].user_id,req.params.id]);
      if (!other.rowCount) await client.query("UPDATE users SET premium_status='rejected' WHERE id=$1", [p.rows[0].user_id]);
    }
    await client.query('COMMIT');
    res.json({ ok: true, status });
  } catch { await client.query('ROLLBACK'); res.status(500).json({ error: 'Prüfung fehlgeschlagen.' }); }
  finally { client.release(); }
});

app.use((err,_req,res,_next) => { console.error(err); res.status(500).json({ error: 'Interner Serverfehler.' }); });
init().then(() => app.listen(PORT, () => console.log('ASTRALIS App Center API listening on ' + PORT))).catch(e => { console.error('Database initialization failed', e); process.exit(1); });
