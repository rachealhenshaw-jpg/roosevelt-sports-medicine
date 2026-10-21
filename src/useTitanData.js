import { useState, useEffect } from "react";
import { supabase, supabaseConfigured } from "./supabaseClient";

export function useTitanData() {
  const [positions, setPositions] = useState({});
  const [injuries, setInjuries] = useState([]);
  const [gpsSessions, setGpsSessions] = useState([]);
  const [weights, setWeights] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!supabaseConfigured) {
      setLoading(false);
      return;
    }
    async function fetchAllData() {
      try {
        const [{ data: posData }, { data: gpsData }, { data: injData }, { data: weightData }] = await Promise.all([
          supabase.from("roster_positions").select("*"),
          supabase.from("gps_sessions").select("*").range(0, 5000),
          supabase.from("injuries").select("*"),
          supabase.from("weights").select("*")
        ]);
        if (posData && posData.length) {
          const map = {};
          posData.forEach((item) => { if (item.player_name) map[item.player_name] = item.position || ""; });
          setPositions(map);
        }
        if (gpsData && gpsData.length) {
          const mappedGps = gpsData.map((row) => {
            const name = row.player_name || row["Player Name"] || row.playerName || row.name || "Unknown Player";
            const date = row.session_date || row["Date"] || row.sessionDate || row.date || "";
            const dist = Number(row.total_distance || row["Total Distance"] || row.totalDistance || row.distance || 0);
            const speed = Number(row.top_speed || row["Top Speed"] || row.topSpeed || 0);
            const ld = Number(row.load || row["Load"] || 0);
            const accel = Number(row.peak_accel || row["Peak Accel"] || row.peakAccel || 0);
            return {
              ...row,
              name,
              playerName: name,
              "Player Name": name,
              player_name: name,
              sessionDate: date,
              "Date": date,
              session_date: date,
              totalDistance: dist,
              "Total Distance": dist,
              total_distance: dist,
              topSpeed: speed,
              "Top Speed": speed,
              top_speed: speed,
              load: ld,
              "Load": ld,
              peakAccel: accel,
              "Peak Accel": accel,
              peak_accel: accel
            };
          });
          setGpsSessions(mappedGps);
        }
        if (injData) setInjuries(injData);
        if (weightData) setWeights(weightData);
      } catch (err) {
        console.error("Error fetching Supabase data:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchAllData();
  }, []);

  return {
    positions,
    injuries,
    gpsSessions,
    weights,
    loading,
    isSupabaseConnected: supabaseConfigured,
  };
}
