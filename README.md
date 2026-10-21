# Titan Risk Analyzer — local app with Supabase backend

This version runs on your laptop (`npm run dev`) and stores your roster and
weekly GPS sessions in Supabase, so the data persists across restarts and is
available from any device that runs this app pointed at the same project.

## 1. Install Node.js (you don't have it yet)

1. Go to **https://nodejs.org** and download the **LTS** version for your
   operating system (the left/recommended button on the homepage).
2. Run the installer, clicking through the defaults.
3. Confirm it worked — open a terminal (Terminal on Mac, Command Prompt or
   PowerShell on Windows) and run:
   ```
   node -v
   npm -v
   ```
   Both should print a version number. If they don't, restart your terminal
   (and your computer, if it still doesn't work) — the installer needs a
   fresh terminal session to update your PATH.

## 2. Create your Supabase project

1. Go to **https://supabase.com**, sign up or log in, and click **New project**.
2. Give it a name (e.g. "titan-risk-analyzer"), set a database password
   (save it somewhere), pick a region close to you, and create the project.
   This takes a minute or two to provision.
3. Once it's ready, open the **SQL Editor** (left sidebar) → **New query**.
4. Open `schema.sql` from this folder, copy its entire contents, paste into
   the SQL editor, and click **Run**. This creates the three tables the app
   needs (`roster`, `gps_sessions`, `app_settings`).
5. Go to **Settings → API** (left sidebar). You'll need two values from
   this page in the next step:
   - **Project URL** (looks like `https://abcdefgh.supabase.co`)
   - **anon public** key (a long string under "Project API keys")

## 3. Configure the app with your Supabase credentials

1. In this project folder, copy `.env.example` to a new file named `.env`.
2. Open `.env` and paste in your Project URL and anon key from step 2.5:
   ```
   VITE_SUPABASE_URL=https://abcdefgh.supabase.co
   VITE_SUPABASE_ANON_KEY=eyJhbGciOi...
   ```
3. Save the file. (`.env` is for your machine only — don't share it or
   commit it to a public repo, since the anon key gives access to your data.)

## 4. Install dependencies and run it

In a terminal, `cd` into this project folder, then:

```
npm install
npm run dev
```

The terminal will print a local address, usually **http://localhost:5173**.
Open that in your browser — that's the app, running on your laptop.

Click **"Load sample data"** to confirm everything (including the Supabase
connection) is working before trying your real CSV.

## 5. Using it day to day

- Every time you reopen the project: `cd` into the folder and run
  `npm run dev` again. There's nothing else to redo — Node and your
  dependencies stay installed.
- Upload your real Titan CSV export each session, check the tiers, and
  click **"Save session to history"** — that writes to Supabase, so it'll
  still be there next time and starts building the real ACWR trend.
- Roster position assignments are saved to Supabase too and will be there
  automatically the next time you open the app, even on a different
  computer, as long as it's pointed at the same Supabase project (same
  `.env` values).

## 6. Deploying it (a real URL, not just localhost)

Once it's working locally:

```
npm run build
```

This produces a `dist` folder — a set of static files. Deploy that folder
the same way as the earlier standalone version: drag it onto
**app.netlify.com/drop**, or connect this project's folder to Netlify/Vercel
via their CLI or GitHub integration for automatic redeploys later.

**Important:** when deploying, you'll need to set the same
`VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` as environment variables in
your hosting provider's dashboard (Netlify: Site settings → Environment
variables) — the `.env` file itself never gets uploaded.

## Security note before sharing this more widely

`schema.sql` sets up Row Level Security policies that allow full read/write
access to anyone holding your Supabase **anon key** — which is visible in
your deployed app's client-side code (this is normal for anon keys, but it
means anyone who inspects your site's network requests could read or write
to these tables). That's fine for a private prototype only you and your
coaching staff use. Before sharing the URL more broadly (e.g. handing it to
Hudl for an open demo, or using it with real athlete data at scale), add
proper authentication and tighten the RLS policies so only logged-in users
can read/write.
