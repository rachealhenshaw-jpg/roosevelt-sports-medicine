-- Titan Risk Analyzer -- Supabase schema
-- Run this once in your Supabase project's SQL Editor (Dashboard -> SQL Editor -> New query -> paste -> Run)

-- Roster: one row per player, holds their assigned position.
-- Manually-set positions here always take priority over whatever a CSV says.
create table if not exists roster (
  player_name text primary key,
  position text,
  updated_at timestamptz default now()
);

-- One row per player per uploaded session. This is what powers both the
-- current session's risk tiers and, once several sessions exist for the
-- same player, the ACWR (acute:chronic workload ratio) trend.
create table if not exists gps_sessions (
  id bigint generated always as identity primary key,
  player_name text not null,
  session_date text,
  distance numeric,
  top_speed numeric,
  load numeric,
  peak_accel numeric,
  band4_yds numeric,
  band5_yds numeric,
  decel_total numeric,
  has_decel boolean,
  position text,
  created_at timestamptz default now()
);

create index if not exists gps_sessions_player_idx on gps_sessions (player_name, session_date);

-- Single-row settings table (just the team name for now).
create table if not exists app_settings (
  id int primary key default 1,
  team_name text default 'Your Team'
);
insert into app_settings (id, team_name) values (1, 'Your Team')
  on conflict (id) do nothing;

-- Row Level Security: required by Supabase before any table is readable/
-- writable via the public anon key. This schema opens each table to anyone
-- holding your anon key (fine for a private prototype only you and your
-- staff use). Before sharing this app's URL more broadly, tighten these
-- policies -- e.g. require authentication -- since the anon key is visible
-- in the deployed app's client-side code.
alter table roster enable row level security;
alter table gps_sessions enable row level security;
alter table app_settings enable row level security;

create policy "anon full access - roster" on roster
  for all using (true) with check (true);
create policy "anon full access - gps_sessions" on gps_sessions
  for all using (true) with check (true);
create policy "anon full access - app_settings" on app_settings
  for all using (true) with check (true);
