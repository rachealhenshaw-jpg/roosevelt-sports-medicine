import React, { useState, useEffect } from "react";
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL;
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY;
const supabase = createClient(supabaseUrl, supabaseAnonKey);

export default function App() {
  const [session, setSession] = useState(null);
  const [email, setEmail] = useState("rhensh@neisd.net");
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState("");
  const [fetchError, setFetchError] = useState("");
  const [athletes, setAthletes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [selectedTab, setSelectedTab] = useState("Roster");

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => setSession(session));
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => setSession(session));
    return () => subscription.unsubscribe();
  }, []);

  useEffect(() => {
    if (session) fetchAthleteData();
  }, [session]);

  async function fetchAthleteData() {
    setLoading(true);
    setFetchError("");
    const { data, error } = await supabase.from("athletes").select("*");
    if (error) {
      console.error("Supabase error:", error);
      setFetchError(error.message);
    } else if (data) {
      setAthletes(data);
    }
    setLoading(false);
  }

  return (
    <div style={{ minHeight: "100vh", width: "100vw", backgroundColor: "#0f172a", color: "#f8fafc", fontFamily: "system-ui, -apple-system, sans-serif", margin: 0, padding: 0, boxSizing: "border-box" }}>
      {!session ? (
        <div style={{ display: "flex", alignItems: "center", justifyContent: "center", minHeight: "100vh", padding: "20px" }}>
          <div style={{ maxWidth: "440px", width: "100%", backgroundColor: "#1e293b", borderRadius: "12px", padding: "32px", border: "1px solid #334155", boxShadow: "0 25px 50px -12px rgba(0, 0, 0, 0.5)" }}>
            <h2 style={{ fontSize: "24px", fontWeight: "700", color: "#34d399", margin: "0 0 8px 0" }}>Roosevelt Performance and Injury Risk</h2>
            <p style={{ color: "#94a3b8", fontSize: "14px", margin: "0 0 24px 0" }}>Sign in to access Supabase Athlete Analytics</p>

            {authError && (
              <div style={{ marginBottom: "16px", padding: "12px", backgroundColor: "#7f1d1d", border: "1px solid #ef4444", borderRadius: "6px", color: "#fca5a5", fontSize: "14px" }}>
                {authError}
              </div>
            )}

            <form onSubmit={async (e) => {
              e.preventDefault();
              setLoading(true);
              const { data, error } = await supabase.auth.signInWithPassword({ email, password });
              if (error) setAuthError(error.message);
              else setSession(data.session);
              setLoading(false);
            }} style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
              <div>
                <label style={{ display: "block", fontSize: "12px", fontWeight: "600", letterSpacing: "0.05em", color: "#cbd5e1", textTransform: "uppercase", marginBottom: "6px" }}>Email</label>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} style={{ width: "100%", backgroundColor: "#0f172a", border: "1px solid #475569", borderRadius: "6px", padding: "10px 12px", color: "#ffffff", fontSize: "14px", outline: "none", boxSizing: "border-box" }} required />
              </div>
              <div>
                <label style={{ display: "block", fontSize: "12px", fontWeight: "600", letterSpacing: "0.05em", color: "#cbd5e1", textTransform: "uppercase", marginBottom: "6px" }}>Password</label>
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} style={{ width: "100%", backgroundColor: "#0f172a", border: "1px solid #475569", borderRadius: "6px", padding: "10px 12px", color: "#ffffff", fontSize: "14px", outline: "none", boxSizing: "border-box" }} required />
              </div>
              <button type="submit" disabled={loading} style={{ width: "100%", backgroundColor: "#10b981", color: "#022c22", fontWeight: "700", padding: "12px", borderRadius: "6px", border: "none", cursor: "pointer", fontSize: "15px", marginTop: "8px" }}>
                {loading ? "Signing in..." : "Sign In"}
              </button>
            </form>
          </div>
        </div>
      ) : (
        <div style={{ padding: "32px", maxWidth: "1200px", margin: "0 auto" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "32px", borderBottom: "1px solid #334155", paddingBottom: "16px" }}>
            <h1 style={{ fontSize: "28px", fontWeight: "800", color: "#34d399", margin: 0 }}>Roosevelt Performance and Injury Risk</h1>
            <button onClick={() => supabase.auth.signOut()} style={{ backgroundColor: "#334155", color: "#ffffff", border: "none", padding: "8px 16px", borderRadius: "6px", cursor: "pointer", fontSize: "14px", fontWeight: "600" }}>
              Sign Out (Dr. Henshaw)
            </button>
          </div>

          <div style={{ display: "flex", gap: "16px", marginBottom: "24px" }}>
            <button onClick={() => setSelectedTab("Roster")} style={{ padding: "8px 16px", fontWeight: "600", fontSize: "15px", backgroundColor: "transparent", border: "none", borderBottom: selectedTab === "Roster" ? "3px solid #34d399" : "none", color: selectedTab === "Roster" ? "#34d399" : "#94a3b8", cursor: "pointer" }}>
              Roster ({athletes.length})
            </button>
          </div>

          {fetchError && (
            <div style={{ marginBottom: "20px", padding: "16px", backgroundColor: "#7f1d1d", border: "1px solid #ef4444", borderRadius: "8px", color: "#fca5a5", fontSize: "14px" }}>
              <strong>Supabase Error:</strong> {fetchError}
            </div>
          )}

          {loading ? (
            <p style={{ color: "#94a3b8" }}>Loading Supabase Data...</p>
          ) : athletes.length === 0 && !fetchError ? (
            <div style={{ padding: "24px", backgroundColor: "#1e293b", border: "1px solid #334155", borderRadius: "8px", color: "#94a3b8" }}>
              No athlete records found in table 'athletes'.
            </div>
          ) : (
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "20px" }}>
              {athletes.map((a, i) => (
                <div key={a.id || i} style={{ backgroundColor: "#1e293b", border: "1px solid #334155", padding: "20px", borderRadius: "10px" }}>
                  <h3 style={{ margin: "0 0 8px 0", color: "#34d399", fontSize: "18px", fontWeight: "700" }}>{a.name || a.athlete_name || `Athlete #${i + 1}`}</h3>
                  <p style={{ margin: "4px 0", color: "#cbd5e1", fontSize: "14px" }}>Position: {a.position || "N/A"}</p>
                  <p style={{ margin: "4px 0", color: "#cbd5e1", fontSize: "14px" }}>Status: {a.status || "Active"}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}