import React, { useMemo, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend, CartesianGrid } from "recharts";

// --- Utility math ---
const deg2rad = (d: number) => (Math.PI / 180) * d;
const rad2deg = (r: number) => (180 / Math.PI) * r;
const clamp = (x: number, a: number, b: number) => Math.min(Math.max(x, a), b);
const wrap360 = (deg: number) => ((deg % 360) + 360) % 360;
const wrap180 = (deg: number) => {
  const w = wrap360(deg);
  return w > 180 ? w - 360 : w;
};

// --- Physical-ish constants & assumptions ---
const SYNODIC_DAYS = 29.530588853; // mean synodic month
const FULL_DAY_ILLUM_MAX = 120_000; // lux, bright sun over a reflective surface under clear sky (Earthlike 1.2 atm)
const FULL_EARTHLIGHT_MAX = 50; // lux at zenith for full Earth under clear sky (near side only)

// New Moon reference (close): 2000-01-06 18:14 UTC (J2000-era new moon)
const NEW_MOON_EPOCH_UTC = Date.UTC(2000, 0, 6, 18, 14, 0, 0);

function lunarAgeDays(dateUTCms: number): number {
  const days = (dateUTCms - NEW_MOON_EPOCH_UTC) / (1000 * 60 * 60 * 24);
  return ((days % SYNODIC_DAYS) + SYNODIC_DAYS) % SYNODIC_DAYS;
}

function subsolarLongitudeDeg(ageDays: number): number {
  const frac = ageDays / SYNODIC_DAYS;
  return wrap360(180 + 360 * frac);
}

function solarElevationDeg(latDeg: number, lonDeg: number, ageDays: number): number {
  const lat = deg2rad(latDeg);
  const subsolarLon = subsolarLongitudeDeg(ageDays);
  const H = deg2rad(wrap180(lonDeg - subsolarLon));
  const sinH = Math.cos(lat) * Math.cos(H);
  const h = Math.asin(clamp(sinH, -1, 1));
  return rad2deg(h);
}

function earthAltitudeDeg(latDeg: number, lonDeg: number): number {
  const lat = deg2rad(latDeg);
  const H = deg2rad(wrap180(lonDeg));
  const sinAlt = Math.cos(lat) * Math.cos(H);
  const alt = Math.asin(clamp(sinAlt, -1, 1));
  return rad2deg(alt);
}

function earthPhaseFraction(ageDays: number): number {
  const phaseAngle = 2 * Math.PI * (ageDays / SYNODIC_DAYS);
  return (1 + Math.cos(phaseAngle)) / 2;
}

function skyLuxFromSun(elevDeg: number): number {
  if (elevDeg >= 10) return FULL_DAY_ILLUM_MAX * Math.sin(deg2rad(elevDeg));
  if (elevDeg > 0) {
    const t = elevDeg / 10;
    const low = 3;
    const high = FULL_DAY_ILLUM_MAX * Math.sin(deg2rad(10));
    return low * (1 - t) + high * t;
  }
  if (elevDeg >= -6) return 0.5 + (2.5 * (elevDeg + 6)) / 6;
  if (elevDeg >= -12) return 0.05 + (0.45 * (elevDeg + 12)) / 6;
  if (elevDeg >= -18) return 0.001 + (0.049 * (elevDeg + 18)) / 6;
  return 0.0005;
}

function earthlightLux(latDeg: number, lonDeg: number, ageDays: number): number {
  const alt = earthAltitudeDeg(latDeg, lonDeg);
  if (alt <= 0) return 0;
  const phase = earthPhaseFraction(ageDays);
  const altScale = Math.sin(deg2rad(alt));
  return FULL_EARTHLIGHT_MAX * phase * altScale;
}

function describeLux(lux: number): string {
  if (lux >= 30_000) return "Bright daylight";
  if (lux >= 5_000) return "Daylight";
  if (lux >= 1_000) return "Overcast/low sun";
  if (lux >= 10) return "Twilight";
  if (lux >= 0.1) return "Deep twilight";
  if (lux >= 0.01) return "Very dark";
  return "Starlight";
}

// --- Perceptual scales ---
function toLogLux(lux: number): number {
  return lux > 0 ? Math.log10(lux) : -4; // safe floor
}

function toCIE_L(lux: number): number {
  // Normalize lux to Y/Yn (using 100k lux as white reference)
  const Yn = 100_000;
  const Y = Math.min(lux, Yn);
  return Y <= 0 ? 0 : 116 * Math.cbrt(Y / Yn) - 16;
}

// Build time series
function buildSeries(lat: number, lon: number, centerUTCms: number, scale: string, spanDays = 30, stepMinutes = 60) {
  const pts: any[] = [];
  const halfSpanMs = (spanDays / 2) * 24 * 3600 * 1000;
  const start = centerUTCms - halfSpanMs;
  const steps = Math.ceil((spanDays * 24 * 60) / stepMinutes);
  for (let i = 0; i <= steps; i++) {
    const t = start + i * stepMinutes * 60 * 1000;
    const age = lunarAgeDays(t);
    const sunEl = solarElevationDeg(lat, lon, age);
    const skyLux = skyLuxFromSun(sunEl);
    const earthLux = earthlightLux(lat, lon, age);
    const totalLux = skyLux + earthLux;

    let scaleFn = (x: number) => x;
    if (scale === "log") scaleFn = toLogLux;
    if (scale === "cie") scaleFn = toCIE_L;

    pts.push({
      t,
      time: new Date(t).toISOString().slice(0, 16).replace("T", " "),
      SunElevation: sunEl,
      SkyLux: Number(scaleFn(skyLux).toFixed(3)),
      EarthlightLux: Number(scaleFn(earthLux).toFixed(3)),
      TotalLux: Number(scaleFn(totalLux).toFixed(3)),
    });
  }
  return pts;
}

export default function App() {
  const now = new Date();
  const [lat, setLat] = useState(0);
  const [lon, setLon] = useState(0);
  const [dtLocal, setDtLocal] = useState(() => new Date().toISOString().slice(0, 16));
  const [scale, setScale] = useState("linear");

  const dt = useMemo(() => new Date(dtLocal), [dtLocal]);
  const age = lunarAgeDays(dt.getTime());
  const sunEl = solarElevationDeg(lat, lon, age);
  const skyLux = skyLuxFromSun(sunEl);
  const eAlt = earthAltitudeDeg(lat, lon);
  const ePhase = earthPhaseFraction(age);
  const eLux = earthlightLux(lat, lon, age);
  const totalLux = skyLux + eLux;

  const nearSide = eAlt > 0;
  const series = useMemo(() => buildSeries(lat, lon, dt.getTime(), scale, 30, 60), [lat, lon, dt, scale]);

  let displayVal = totalLux;
  if (scale === "log") displayVal = toLogLux(totalLux);
  if (scale === "cie") displayVal = toCIE_L(totalLux);

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <header className="flex items-center justify-between">
          <h1 className="text-2xl md:text-3xl font-bold">Lunar Light & Earthlight Calculator</h1>
          <div className="text-sm opacity-70">Approximate model • Earthlike 1.2 atm</div>
        </header>

        <section className="grid md:grid-cols-3 gap-4">
          <div className="p-4 bg-white rounded-2xl shadow">
            <label className="block text-sm font-medium">Latitude (°)</label>
            <input type="range" min={-90} max={90} step={0.5} value={lat} onChange={(e)=>setLat(parseFloat(e.target.value))} className="w-full"/>
            <div className="text-sm">{lat.toFixed(1)}°</div>

            <label className="block text-sm font-medium mt-4">Longitude (°E)</label>
            <input type="range" min={-180} max={180} step={0.5} value={lon} onChange={(e)=>setLon(parseFloat(e.target.value))} className="w-full"/>
            <div className="text-sm">{lon.toFixed(1)}°</div>

            <label className="block text-sm font-medium mt-4">Date & Time (local)</label>
            <input type="datetime-local" value={dtLocal} onChange={(e)=>setDtLocal(e.target.value)} className="w-full border rounded px-2 py-1"/>
            <p className="text-xs mt-2 opacity-70">Interpreted in your local timezone, converted to UTC internally.</p>

            <label className="block text-sm font-medium mt-4">Scale</label>
            <select value={scale} onChange={(e)=>setScale(e.target.value)} className="w-full border rounded px-2 py-1">
              <option value="linear">Linear (lux)</option>
              <option value="log">Log Lux (log10)</option>
              <option value="cie">CIE L* (perceptual)</option>
            </select>
          </div>

          <div className="p-4 bg-white rounded-2xl shadow space-y-2">
            <h2 className="font-semibold">Instant Conditions</h2>
            <div className="grid grid-cols-2 gap-2 text-sm">
              <div className="p-2 bg-gray-100 rounded-lg">Solar elevation: <b>{sunEl.toFixed(2)}°</b></div>
              <div className="p-2 bg-gray-100 rounded-lg">Earth altitude: <b>{eAlt.toFixed(2)}°</b></div>
              <div className="p-2 bg-gray-100 rounded-lg">Earth phase: <b>{(ePhase*100).toFixed(0)}%</b></div>
              <div className="p-2 bg-gray-100 rounded-lg">Raw total lux: <b>{totalLux.toFixed(2)}</b></div>
              <div className="p-2 bg-gray-100 rounded-lg">Scaled value: <b>{displayVal.toFixed(2)}</b></div>
            </div>
            <div className="mt-2 text-sm">Perceived brightness: <b>{describeLux(totalLux)}</b></div>
            <div className="text-xs opacity-70">Near-side visibility: <b>{nearSide ? "Earth above horizon" : "Earth below horizon (far-side)"}</b></div>
          </div>

          <div className="p-4 bg-white rounded-2xl shadow text-sm">
            <h2 className="font-semibold mb-1">Model Notes</h2>
            <ul className="list-disc pl-5 space-y-1">
              <li>Subsolar longitude evolves linearly with lunar age; axial tilt and libration ignored.</li>
              <li>Sky lux uses twilight model for 1.2 atm atmosphere.</li>
              <li>Earthlight peaks ~50 lux at zenith full Earth, scaled by phase and altitude.</li>
              <li>Chart supports Linear, Log Lux, and CIE L* perceptual scales.</li>
            </ul>
          </div>
        </section>

        <section className="p-4 bg-white rounded-2xl shadow">
          <h2 className="font-semibold mb-2">30-day Light Curve (hourly)</h2>
          <div className="w-full h-72">
            <ResponsiveContainer>
              <LineChart data={series} margin={{ top: 10, right: 20, bottom: 10, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" tick={false} interval={Math.ceil(series.length/12)} />
                <YAxis yAxisId="left" orientation="left" domain={["auto", "auto"]} />
                <Tooltip formatter={(v: any, n: string) => [v, n]} />
                <Legend />
                <Line yAxisId="left" type="monotone" dataKey="TotalLux" dot={false} strokeWidth={2} name="Total" />
                <Line yAxisId="left" type="monotone" dataKey="SkyLux" dot={false} strokeWidth={1.5} name="Sky (Sun)" />
                <Line yAxisId="left" type="monotone" dataKey="EarthlightLux" dot={false} strokeWidth={1.5} name="Earthlight" />
              </LineChart>
            </ResponsiveContainer>
          </div>
          <div className="text-xs opacity-70 mt-2">Tip: switch scale to Linear, Log Lux, or CIE L* to see physical vs perceptual differences.</div>
        </section>
      </div>
    </div>
  );
}
