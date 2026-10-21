import React, { useState, useEffect } from 'react';
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = 'https://mdboekicnrcptptwdacy.supabase.co';
const SUPABASE_ANON_KEY = 'YOUR_SUPABASE_ANON_KEY'; // Replace with your actual anon key if separate
const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const ADMIN_EMAIL = 'rhensh@neisd.net';

// Mock generator for Admin Demo data
const generateDemoData = () => {
  const athletes = ['Athlete A', 'Athlete B', 'Athlete C', 'Athlete D', 'Athlete E'];
  const types = ['Game', 'Practice'];
  const mockData = [];
  
  for (let week = 1; week <= 4; week++) {
    for (let day = 1; day <= 5; day++) {
      athletes.forEach(athlete => {
        const sessionType = types[Math.floor(Math.random() * types.length)];
        mockData.push({
          id: `${athlete}-w${week}-d${day}`,
          athlete_name: athlete,
          date: `2026-10-${(week * 7 + day).toString().padStart(2, '0')}`,
          week: `Week ${week}`,
          session_type: sessionType,
          total_distance: Math.floor(Math.random() * 4000) + 2000,
          hsd: Math.floor(Math.random() * 800) + 200,
          player_load: Math.floor(Math.random() * 300) + 150,
          priority_score: (Math.random() * 5 + 1).toFixed(1)
        });
      });
    }
  }
  return mockData;
};

export default function App() {
  const [session, setSession] = useState(null);
  const [email, setEmail] = useState('rhensh@neisd.net');
  const [password, setPassword] = useState('');
  const [authError, setAuthError] = useState('');
  
  const [gpsData, setGpsData] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // Dashboard Filters & Controls
  const [selectedTab, setSelectedTab] = useState('Dashboard');
  const [sessionFilter, setSessionFilter] = useState('All'); // All, Game, Practice
  const [selectedWeek, setSelectedWeek] = useState('All');
  const [compareMode, setCompareMode] = useState('day'); // 'day', 'week', 'game'
  
  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      if (session) fetchSupabaseData();
    });

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      if (session) fetchSupabaseData();
    });

    return () => subscription.unsubscribe();
  }, []);

  const fetchSupabaseData = async () => {
    setLoading(true);
    const { data, error } = await supabase.from('gps_sessions').select('*');
    if (!error && data && data.length > 0) {
      setGpsData(data);
    } else {
      // Fallback load if empty or initial setup
      setGpsData([]);
    }
    setLoading(false);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setAuthError('');
    const { error } = await supabase.auth.signInWithPassword({ email, password });
    if (error) setAuthError(error.message);
  };

  const handleSignOut = () => {
    supabase.auth.signOut();
  };

  const handleLoadDemoData = async () => {
    const demoRows = generateDemoData();
    setGpsData(demoRows);
    // Optional: Persist demo data directly to Supabase
    await supabase.from('gps_sessions').upsert(demoRows);
  };

  // Filter data based on Session Type and Week selection
  const filteredData = gpsData.filter(item => {
    const matchesType = sessionFilter === 'All' || item.session_type === sessionFilter;
    const matchesWeek = selectedWeek === 'All' || item.week === selectedWeek;
    return matchesType && matchesWeek;
  });

  // Group filtered records by Athlete for Card display
  const athleteMap = filteredData.reduce((acc, row) => {
    const name = row.athlete_name || row.athlete || 'Unknown Athlete';
    if (!acc[name]) acc[name] = [];
    acc[name].push(row);
    return acc;
  }, {});

  // Render Login Page if not authenticated
  if (!session) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', backgroundColor: '#0d1117', color: '#c9d1d9', fontFamily: 'sans-serif' }}>
        <div style={{ backgroundColor: '#161b22' }}22', padding: '32px', borderRadius: '8px', border: '1px solid #30363d', width: '100%', maxWidth: '400px' }}>
          <h2 style={{ color: '#238636', textAlign: 'center', marginBottom: '8px' }}>Titan Performance Suite</h2>
          <p style={{ color: '#8b949e', textAlign: 'center', fontSize: '14px', marginBottom: '24px' }}>Sign in to access secure athlete analytics</p>
          
          {authError && <div style={{ backgroundColor: '#3d1316', color: '#f85149', padding: '10px', borderRadius: '6px', fontSize: '13px', marginBottom: '16px' }}>{authError}</div>}
          
          <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold', marginBottom: '4px' }}>Email</label>
              <input type="email" value={email} onChange={e => setEmail(e.target.value)} required style={{ width: '100%', padding: '10px', borderRadius: '6px', backgroundColor: '#0d1117', border: '1px solid #30363d', color: '#fff', boxSizing: 'border-box' }} />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 'bold', marginBottom: '4px' }}>Password</label>
              <input type="password" value={password} onChange={e => setPassword(e.target.value)} required style={{ width: '100%', padding: '10px', borderRadius: '6px', backgroundColor: '#0d1117', border: '1px solid #30363d', color: '#fff', boxSizing: 'border-box' }} />
            </div>
            <button type="submit" style={{ backgroundColor: '#238636', color: '#fff', padding: '10px', borderRadius: '6px', border: 'none', fontWeight: 'bold', cursor: 'pointer', marginTop: '8px' }}>
              Sign In
            </button>
          </form>
        </div>
      </div>
    );
  }

  const isAdmin = session.user?.email === ADMIN_EMAIL;

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0d1117', color: '#c9d1d9', fontFamily: 'sans-serif' }}>
      {/* Top Header */}
      <header style={{ backgroundColor: '#161b22' }}22', padding: '16px 24px', borderBottom: '1px solid #30363d', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h1 style={{ fontSize: '20px', margin: 0, color: '#238636' }}>Titan Performance, Recruiting & Prehab Suite</h1>
          <span style={{ fontSize: '12px', color: '#8b949e' }}>Workload Analytics & Injury Prevention • Supabase Authenticated</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {isAdmin && (
            <button onClick={handleLoadDemoData} style={{ backgroundColor: '#238636', color: '#fff', border: 'none', padding: '8px 14px', borderRadius: '6px', fontWeight: 'bold', cursor: 'pointer', fontSize: '12px' }}>
              ⚡ Load Admin Demo Data
            </button>
          )}
          <button onClick={handleSignOut} style={{ backgroundColor: '#21262d', color: '#c9d1d9', border: '1px solid #30363d', padding: '8px 14px', borderRadius: '6px', cursor: 'pointer', fontSize: '12px' }}>
            Sign Out
          </button>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav style={{ backgroundColor: '#161b22' }}
