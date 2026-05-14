# ============================================================
# MIWAF PHASE 2 - STREAMLIT WEB APP
# Author: Mbugua Hellen Njeri | Reg No: 24/05982
# KCA University | BSc Data Science
# UI/UX: Glassmorphic Hydro-Intelligence Design System
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import time
import datetime
import streamlit.components.v1 as components

# ── Page config ───────────────────────────────────────────────
st.set_page_config(
    page_title            = "MIWAF — WATER CRISIS PREDICTION SYSTEM",
    page_icon             = "🌊",
    layout                = "wide",
    initial_sidebar_state = "expanded"
)

# ════════════════════════════════════════════════════════════
# AUTHENTICATION
# ════════════════════════════════════════════════════════════
# ════════════════════════════════════════════════════════════
# USERS & ROLES
# ════════════════════════════════════════════════════════════
USERS = {
    "admin":   {"password": "admin2026",   "role": "Admin"},
    "analyst": {"password": "analyst2026", "role": "Analyst"},
    "viewer":  {"password": "viewer2026",  "role": "Viewer"},
}

ROLE_PAGES = {
    "Admin":   [
        " OVERVIEW",
        "  CONTAMINATION PREDICTOR",
        "  QUEUE TIME FORECASTER",
        "  CRIME RISK SCORER",
        "  MODEL PERFORMANCE",
        "  CONFUSION MATRICES",
        "  AUDIT LOG",
    ],
    "Analyst": [
        " OVERVIEW",
        "  CONTAMINATION PREDICTOR",
        "  QUEUE TIME FORECASTER",
        "  CRIME RISK SCORER",
        " AUDIT LOG",
    ],
    "Viewer":  [
        " OVERVIEW",
    ],
}

ROLE_BADGES = {
    "Admin":   ("🔴", "rgba(255,138,128,0.15)", "rgba(255,138,128,0.35)", "#ff8a80"),
    "Analyst": ("🟡", "rgba(255,229,122,0.15)", "rgba(255,229,122,0.35)", "#ffe57a"),
    "Viewer":  ("🟢", "rgba(105,255,193,0.15)", "rgba(105,255,193,0.35)", "#69ffc1"),
}

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "role" not in st.session_state:
    st.session_state.role = None
if "username" not in st.session_state:
    st.session_state.username = None

if not st.session_state.authenticated:
    st.markdown("""
    <style>
    .stApp {
      background-color: #051424 !important;
      background-image:
        radial-gradient(ellipse at 0% 0%, rgba(77,142,255,0.12) 0%, transparent 50%),
        radial-gradient(ellipse at 100% 100%, rgba(76,215,246,0.10) 0%, transparent 50%) !important;
    }
    header[data-testid="stHeader"] { display: none !important; }
    footer { display: none !important; }
    .block-container { padding: 0 !important; max-width: 100% !important; }
    .stMainBlockContainer { padding: 0 !important; }
    label[data-testid="stWidgetLabel"] { display: none !important; }
    [data-testid="stTextInput"] input {
      background: rgba(255,255,255,0.06) !important;
      border: 1px solid rgba(255,255,255,0.15) !important;
      border-radius: 12px !important;
      color: #ffffff !important;
      font-size: 15px !important;
      text-align: center !important;
    }
    [data-testid="stTextInput"] input::placeholder { color: rgba(255,255,255,0.35) !important; }
    .stButton > button {
      background: linear-gradient(135deg, #4d8eff 0%, #03b5d3 100%) !important;
      color: #ffffff !important;
      font-size: 15px !important;
      font-weight: 800 !important;
      border: none !important;
      border-radius: 12px !important;
      padding: 14px !important;
      width: 100% !important;
      box-shadow: 0 0 32px rgba(3,181,211,0.30) !important;
    }
    .stButton > button:hover { transform: translateY(-2px) !important; }
    .particle {
      position: fixed; border-radius: 50%;
      background: rgba(77,142,255,0.15);
      animation: float linear infinite;
      pointer-events: none;
    }
    @keyframes float {
      0%   { transform: translateY(100vh); opacity: 0; }
      10%  { opacity: 1; }
      90%  { opacity: 1; }
      100% { transform: translateY(-100px); opacity: 0; }
    }
    </style>

    <div class="particle" style="left:10%;width:8px;height:8px;animation-duration:8s;animation-delay:0s;bottom:0"></div>
    <div class="particle" style="left:25%;width:5px;height:5px;animation-duration:11s;animation-delay:2s;bottom:0"></div>
    <div class="particle" style="left:40%;width:10px;height:10px;animation-duration:9s;animation-delay:1s;bottom:0"></div>
    <div class="particle" style="left:70%;width:8px;height:8px;animation-duration:10s;animation-delay:0.5s;bottom:0"></div>
    <div class="particle" style="left:85%;width:5px;height:5px;animation-duration:12s;animation-delay:4s;bottom:0"></div>

    
    <div style="display:flex;justify-content:center;gap:40px;padding:28px 40px 0;flex-wrap:wrap;">
      <div style="text-align:center;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:800;color:#ffffff;">319,599</div>
        <div style="font-size:11px;color:#7eb3ff;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Records Analysed</div>
      </div>
      <div style="width:1px;background:rgba(255,255,255,0.08);"></div>
      <div style="text-align:center;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:800;color:#ffffff;">3</div>
        <div style="font-size:11px;color:#7eb3ff;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">ML Models</div>
      </div>
      <div style="width:1px;background:rgba(255,255,255,0.08);"></div>
      <div style="text-align:center;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:800;color:#69ffc1;">8</div>
        <div style="font-size:11px;color:#7eb3ff;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Datasets Integrated</div>
      </div>
      <div style="width:1px;background:rgba(255,255,255,0.08);"></div>
      <div style="text-align:center;">
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:22px;font-weight:800;color:#ffffff;">5</div>
        <div style="font-size:11px;color:#7eb3ff;font-weight:600;text-transform:uppercase;letter-spacing:0.08em;">Provinces Covered</div>
      </div>
    </div>

    
    <div style="display:flex;align-items:center;justify-content:center;padding:40px 16px;">
      <div style="width:100%;max-width:460px;background:rgba(18,33,49,0.80);border:1px solid rgba(255,255,255,0.10);border-top:1px solid rgba(255,255,255,0.22);border-radius:24px;padding:48px 44px 32px;backdrop-filter:blur(20px);box-shadow:0 32px 80px rgba(0,0,0,0.40);text-align:center;">
        <div style="width:72px;height:72px;border-radius:20px;background:linear-gradient(135deg,rgba(77,142,255,0.25),rgba(3,181,211,0.20));border:1px solid rgba(77,142,255,0.30);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;font-size:36px;">🌊</div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif;font-size:36px;font-weight:800;color:#ffffff;letter-spacing:-1px;">MIWAF</div>
        <div style="font-size:11px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#4d8eff;margin-top:6px;">Maji Ndogo Water Analytics Framework</div>
        <div style="height:1px;background:rgba(255,255,255,0.08);margin:24px 0;"></div>
        <div style="font-size:14px;color:#cbd8ea;line-height:1.7;margin-bottom:24px;">
          ML-powered predictions for <strong style="color:#ffffff">well contamination</strong>,
          <strong style="color:#ffffff">queue times</strong> and
          <strong style="color:#ffffff">crime risk</strong> at water collection points.
        </div>
        <div style="display:flex;justify-content:center;gap:8px;margin-bottom:8px;flex-wrap:wrap;">
          <span style="background:rgba(77,142,255,0.12);border:1px solid rgba(77,142,255,0.25);color:#7eb3ff;font-size:11px;font-weight:700;padding:4px 12px;border-radius:99px;">XGBoost</span>
          <span style="background:rgba(76,215,246,0.10);border:1px solid rgba(76,215,246,0.22);color:#4cd7f6;font-size:11px;font-weight:700;padding:4px 12px;border-radius:99px;">Logistic Regression</span>
          <span style="background:rgba(110,231,183,0.10);border:1px solid rgba(110,231,183,0.22);color:#6ee7b7;font-size:11px;font-weight:700;padding:4px 12px;border-radius:99px;">Random Forest</span>
        </div>


        <div style="margin-top:24px;padding:16px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);border-radius:12px;text-align:left;">
          <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.09em;color:#7eb3ff;margin-bottom:10px;">Access Levels</div>
          <div style="display:flex;flex-direction:column;gap:7px;">
            <div style="display:flex;align-items:center;gap:10px;font-size:12px;">
              <span style="background:rgba(255,138,128,0.15);border:1px solid rgba(255,138,128,0.35);color:#ff8a80;padding:2px 10px;border-radius:99px;font-weight:700;font-size:10px;">Admin</span>
              <span style="color:#cbd8ea;">Full access — all pages, audit log, model stats</span>
            </div>
            <div style="display:flex;align-items:center;gap:10px;font-size:12px;">
              <span style="background:rgba(255,229,122,0.15);border:1px solid rgba(255,229,122,0.35);color:#ffe57a;padding:2px 10px;border-radius:99px;font-weight:700;font-size:10px;">Analyst</span>
              <span style="color:#cbd8ea;">Prediction tools — contamination, queue, crime</span>
            </div>
            <div style="display:flex;align-items:center;gap:10px;font-size:12px;">
              <span style="background:rgba(105,255,193,0.15);border:1px solid rgba(105,255,193,0.35);color:#69ffc1;padding:2px 10px;border-radius:99px;font-weight:700;font-size:10px;">Viewer</span>
              <span style="color:#cbd8ea;">Overview only — key findings and statistics</span>
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        username = st.text_input("Username", placeholder="👤  Enter username...")
        password = st.text_input("Password", type="password", placeholder="🔑  Enter password...")
        if st.button("🌊  Login to MIWAF", use_container_width=True):
            if username in USERS and USERS[username]["password"] == password:
                st.session_state.authenticated = True
                st.session_state.role = USERS[username]["role"]
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Incorrect username or password.")
    st.stop()
# ════════════════════════════════════════════════════════════
# DESIGN SYSTEM — GLASSMORPHIC HYDRO-INTELLIGENCE
# ════════════════════════════════════════════════════════════
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>

<style>
/* ── TOKENS ─────────────────────────────────────────────── */
:root {
  --bg:           #051424;
  --surface:      rgba(18,33,49,0.72);
  --surface-high: rgba(28,43,60,0.88);
  --surf-ctr:     #122131;
  --surf-hi:      #1c2b3c;
  --surf-highest: #273647;
  --primary:      #adc6ff;
  --primary-c:    #4d8eff;
  --secondary:    #4cd7f6;
  --secondary-c:  #03b5d3;
  --on-surface:   #d4e4fa;
  --on-variant:   #8c909f;
  --border:       rgba(255,255,255,0.08);
  --border-top:   rgba(255,255,255,0.16);
  --error:        #ffb4ab;
  --success:      #6ee7b7;
  --warning:      #fcd34d;
  --r-xl: 20px; --r-lg: 14px; --r-md: 10px; --r-sm: 6px;
  --font-head: 'Plus Jakarta Sans', sans-serif;
  --font-body: 'Inter', sans-serif;
}

/* ── GLOBAL RESET ────────────────────────────────────────── */
html, body, [class*="css"] {
  font-family: var(--font-body) !important;
  color: var(--on-surface);
}

/* Ocean-depth background */
.stApp {
  background-color: var(--bg) !important;
  background-image:
    radial-gradient(ellipse at 0% 0%,   rgba(77,142,255,0.10) 0%, transparent 50%),
    radial-gradient(ellipse at 100% 100%, rgba(76,215,246,0.08) 0%, transparent 50%) !important;
}

/* ── STREAMLIT CHROME OVERRIDES ──────────────────────────── */
header[data-testid="stHeader"] { display: none !important; }
footer { display: none !important; }
#MainMenu { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.stMainBlockContainer { padding: 0 !important; }
.main > div { padding-top: 0 !important; }
div[data-testid="stDecoration"] { display: none !important; }

/* ── SIDEBAR ─────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
  background: rgba(5,20,36,0.97) !important;
  backdrop-filter: blur(24px) !important;
  border-right: 0.5px solid var(--border) !important;
  width: 230px !important;
}
section[data-testid="stSidebar"] > div:first-child {
  padding: 0 !important;
}
/* ── HIDE SIDEBAR COLLAPSE ARROW BUTTON ─────────────────── */
button[data-testid="collapsedControl"],
button[kind="header"][aria-label="Close sidebar"],
section[data-testid="stSidebar"] button[data-testid="baseButton-header"] {
  display: none !important;
}
[data-testid="stSidebarCollapseButton"] { display: none !important; }
/* Also hide the expand arrow that appears when sidebar is collapsed */
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] ::-webkit-scrollbar { width: 4px; }
section[data-testid="stSidebar"] ::-webkit-scrollbar-thumb {
  background: rgba(173,198,255,0.2); border-radius: 99px;
}

/* ── HIDE DEFAULT RADIO STYLE & RE-STYLE AS NAV ITEMS ────── */
/* Hide the radio widget label */
section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
  display: none !important;
}
/* Radio container */
section[data-testid="stSidebar"] [data-testid="stRadio"] > div {
  display: flex !important;
  flex-direction: column !important;
  gap: 2px !important;
  padding: 0 !important;
}
/* Each radio option row */
section[data-testid="stSidebar"] [data-testid="stRadio"] label {
  display: flex !important;
  align-items: center !important;
  gap: 10px !important;
  padding: 10px 16px !important;
  border-radius: var(--r-md) !important;
  cursor: pointer !important;
  transition: background 0.15s, color 0.15s !important;
  font-family: var(--font-body) !important;
  font-size: 13.5px !important;
  font-weight: 500 !important;
  color: var(--on-variant) !important;
  margin: 0 !important;
  border: none !important;
  background: transparent !important;
  position: relative !important;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
  background: rgba(173,198,255,0.07) !important;
  color: var(--on-surface) !important;
}
/* Selected radio item */
section[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked),
section[data-testid="stSidebar"] [data-testid="stRadio"] [aria-checked="true"] {
  background: rgba(77,142,255,0.18) !important;
  color: var(--primary) !important;
  font-weight: 700 !important;
}
/* Hide the actual radio circle dot */
section[data-testid="stSidebar"] [data-testid="stRadio"] [data-baseweb="radio"] > div:first-child {
  display: none !important;
}
section[data-testid="stSidebar"] [data-testid="stRadio"] input[type="radio"] {
  display: none !important;
}

/* ── METRICS ─────────────────────────────────────────────── */
[data-testid="stMetric"] {
  background: var(--surface) !important;
  border: 1px solid var(--border) !important;
  border-top-color: var(--border-top) !important;
  border-radius: var(--r-xl) !important;
  padding: 18px 20px !important;
  backdrop-filter: blur(14px) !important;
  position: relative; overflow: hidden;
}
[data-testid="stMetric"]::after {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at top right, rgba(173,198,255,0.05), transparent 60%);
  pointer-events: none;
}
[data-testid="stMetricLabel"] > div {
  font-family: var(--font-body) !important;
  font-size: 10.5px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
  color: #ffffff !important;
}
[data-testid="stMetricValue"] > div {
  font-family: var(--font-head) !important;
  font-size: 28px !important;
  font-weight: 800 !important;
  color: var(--primary) !important;
  letter-spacing: -0.03em !important;
}
[data-testid="stMetricDelta"] svg { display: none; }
[data-testid="stMetricDelta"] > div {
  font-size: 14px !important;
  color: #ffffff !important;
}

/* ── SLIDERS ─────────────────────────────────────────────── */
[data-testid="stSlider"] > div > div {
  background: rgba(173,198,255,0.10) !important;
  height: 6px !important; border-radius: 99px !important;
}
[data-testid="stSlider"] [role="slider"] {
  background: var(--primary-c) !important;
  border: none !important;
  box-shadow: 0 0 14px rgba(77,142,255,0.55) !important;
  width: 18px !important; height: 18px !important;
}
[data-testid="stSlider"] [data-baseweb="slider-mark"] { display: none !important; }
[data-testid="stSlider"] p {
  font-family: var(--font-body) !important;
  font-size: 11px !important;
  color: var(--on-variant) !important;
}

/* ── SELECTBOX ───────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-md) !important;
  color: var(--on-surface) !important;
  font-family: var(--font-body) !important;
  font-size: 13px !important;
}
[data-testid="stSelectbox"] > div > div:focus-within {
  border-color: rgba(173,198,255,0.35) !important;
  box-shadow: 0 0 0 1px rgba(173,198,255,0.15) !important;
}
[data-testid="stSelectbox"] svg { fill: var(--on-variant) !important; }

/* ── NUMBER INPUT ────────────────────────────────────────── */
[data-testid="stNumberInput"] input {
  background: rgba(255,255,255,0.04) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--r-md) !important;
  color: var(--on-surface) !important;
  font-family: var(--font-body) !important;
  font-size: 13px !important;
}
[data-testid="stNumberInput"] input:focus {
  border-color: rgba(173,198,255,0.35) !important;
  box-shadow: 0 0 0 1px rgba(173,198,255,0.15) !important;
}

/* ── BUTTONS ─────────────────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, var(--primary-c) 0%, var(--secondary-c) 100%) !important;
  color: #001a42 !important;
  font-family: var(--font-head) !important;
  font-size: 13.5px !important;
  font-weight: 800 !important;
  border: none !important;
  border-radius: var(--r-lg) !important;
  padding: 12px 20px !important;
  box-shadow: 0 0 28px rgba(3,181,211,0.25), 0 4px 12px rgba(0,0,0,0.3) !important;
  transition: transform 0.15s, box-shadow 0.15s !important;
  width: 100% !important;
}
.stButton > button:hover {
  transform: translateY(-2px) !important;
  box-shadow: 0 0 40px rgba(3,181,211,0.40), 0 8px 20px rgba(0,0,0,0.35) !important;
  color: #001a42 !important;
}
.stButton > button:active { transform: scale(0.97) !important; }

.stDownloadButton > button {
  background: rgba(255,255,255,0.06) !important;
  color: var(--on-surface) !important;
  font-weight: 700 !important;
  border: 1px solid var(--border) !important;
  box-shadow: none !important;
}
.stDownloadButton > button:hover {
  background: rgba(255,255,255,0.10) !important;
  transform: none !important;
  box-shadow: none !important;
}

/* ── DATAFRAME ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border: 1px solid var(--border) !important;
  border-radius: var(--r-lg) !important;
  overflow: hidden !important;
}
[data-testid="stDataFrame"] table { background: transparent !important; }
[data-testid="stDataFrame"] thead tr th {
  background: rgba(255,255,255,0.04) !important;
  color: var(--on-variant) !important;
  font-size: 10.5px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.06em !important;
  border-bottom: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] tbody tr td {
  color: var(--on-surface) !important;
  font-size: 12.5px !important;
  border-bottom: 1px solid rgba(255,255,255,0.04) !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
  background: rgba(255,255,255,0.03) !important;
}

/* ── IMAGES ──────────────────────────────────────────────── */
[data-testid="stImage"] img {
  border-radius: var(--r-xl) !important;
  border: 1px solid var(--border) !important;
}

/* ── ALERTS ──────────────────────────────────────────────── */
[data-testid="stAlert"] {
  border-radius: var(--r-md) !important;
  border-width: 1px !important;
  font-family: var(--font-body) !important;
  font-size: 13px !important;
}
[data-testid="stAlert"][data-baseweb="notification"] {
  background: rgba(173,198,255,0.08) !important;
  border-color: rgba(173,198,255,0.2) !important;
  color: var(--primary) !important;
}
div[data-testid="stAlert"] p { color: inherit !important; }

/* ── LABELS ──────────────────────────────────────────────── */
label[data-testid="stWidgetLabel"] p,
.stSlider label p,
.stSelectbox label p,
.stNumberInput label p {
  font-family: var(--font-body) !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: 0.07em !important;
  color: #ffffff !important;
}

/* ── CAPTIONS ────────────────────────────────────────────── */
[data-testid="stCaptionContainer"],
[data-testid="stCaptionContainer"] p,
[data-testid="stCaptionContainer"] span,
[data-testid="stCaptionContainer"] div {
  font-size: 13px !important;
  color: #ffffff !important;
  line-height: 1.6 !important;
}

/* ── DIVIDER ─────────────────────────────────────────────── */
hr { border-color: var(--border) !important; margin: 16px 0 !important; }

/* ── SPINNER ─────────────────────────────────────────────── */
[data-testid="stSpinner"] { color: var(--primary) !important; }

/* ═══════════════════════════════════════════════════════════
   CUSTOM COMPONENT CLASSES
═══════════════════════════════════════════════════════════ */

.gc {
  background: var(--surface);
  backdrop-filter: blur(14px);
  border: 1px solid var(--border);
  border-top-color: var(--border-top);
  border-radius: var(--r-xl);
  padding: 22px 24px;
  margin-bottom: 0;
  position: relative; overflow: hidden;
}
.gc::after {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at top right, rgba(173,198,255,0.04), transparent 55%);
  pointer-events: none;
}

.sh {
  display: flex; align-items: center; gap: 8px;
  margin-bottom: 14px;
}
.sh .ms { color: var(--primary); font-size: 18px; }
.sh h3 {
  font-family: var(--font-head);
  font-size: 15px; font-weight: 700; color: var(--on-surface);
  margin: 0;
}

.ab {
  background: linear-gradient(135deg, rgba(29,78,216,0.20), rgba(3,181,211,0.10));
  border: 1px solid rgba(173,198,255,0.16);
  border-left: 3px solid var(--primary-c);
  border-radius: var(--r-lg);
  padding: 14px 18px; margin-bottom: 20px;
}
.ab b { color: var(--primary); font-size: 18.5px; font-family: var(--font-head); font-weight: 700; }
.ab p { font-size: 18px; color: #ffffff; margin-top: 5px; line-height: 1.7; }

.ms {
  font-family: 'Material Symbols Outlined';
  font-size: 20px; line-height: 1; vertical-align: middle;
  display: inline-block;
}

.vb {
  font-family: var(--font-head); font-size: 22px; font-weight: 800;
  color: var(--primary); background: rgba(173,198,255,0.08);
  border-radius: var(--r-md); padding: 4px 12px; line-height: 1.1; display: inline-block;
}
.vb.cy { color: var(--secondary); background: rgba(76,215,246,0.08); }
.vb small { font-size: 11px; font-weight: 600; color: var(--on-variant); margin-left: 3px; }

.who-g { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px; }
.who-t { border-radius: var(--r-md); padding: 11px 14px; border: 1px solid; font-family: var(--font-body); }
.who-ok { background: rgba(110,231,183,0.07); border-color: rgba(110,231,183,0.22); }
.who-no { background: rgba(255,180,171,0.09); border-color: rgba(255,180,171,0.28); }
.who-t .wi { display: flex; align-items: center; gap: 5px; font-size: 11.5px; font-weight: 700; }
.who-ok .wi { color: var(--success); } .who-no .wi { color: var(--error); }
.who-t .wv { font-family: var(--font-head); font-size: 17px; font-weight: 800; margin: 4px 0 2px; }
.who-ok .wv { color: var(--success); } .who-no .wv { color: var(--error); }
.who-t .wl { font-size: 13px; color: #ffffff; font-weight: 600; }

.rb { border-radius: var(--r-xl); padding: 22px; text-align: center; }
.rb .rt { font-family: var(--font-head); font-size: 25px; font-weight: 800; line-height: 1.1; }
.rb .rs { font-size: 12px; margin-top: 5px; opacity: 0.75; }
.r-clean { background: rgba(110,231,183,0.10); border: 1px solid rgba(110,231,183,0.25); }
.r-clean .rt { color: var(--success); }
.r-contam { background: rgba(255,180,171,0.10); border: 1px solid rgba(255,180,171,0.28); }
.r-contam .rt { color: var(--error); }
.r-low { background: rgba(110,231,183,0.10); border: 1px solid rgba(110,231,183,0.25); }
.r-low .rt { color: var(--success); }
.r-med { background: rgba(252,211,77,0.09); border: 1px solid rgba(252,211,77,0.24); }
.r-med .rt { color: var(--warning); }
.r-high { background: rgba(255,180,171,0.11); border: 1px solid rgba(255,180,171,0.28); }
.r-high .rt { color: var(--error); }
.r-queue { background: rgba(173,198,255,0.08); border: 1px solid rgba(173,198,255,0.20); }
.r-queue .rt { font-size: 48px; color: var(--primary); letter-spacing: -2px; }

.mp { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 12px; }
.mt { background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: var(--r-md); padding: 11px 14px; }
.mt .mv { font-family: var(--font-head); font-size: 21px; font-weight: 800; color: var(--primary); line-height: 1; }
.mt .mv.cy { color: var(--secondary); }
.mt .mv.er { color: var(--error); }
.mt .ml { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--on-variant); margin-top: 4px; }

.ia { border-radius: var(--r-md); padding: 10px 13px; font-size: 18px; line-height: 1.6; display: flex; gap: 9px; align-items: flex-start; margin-top: 10px; }
.ia .ms { font-size: 16px; flex-shrink: 0; margin-top: 1px; }
.ia-info  { background: rgba(173,198,255,0.08); border: 1px solid rgba(173,198,255,0.18); color: var(--primary); }
.ia-ok    { background: rgba(110,231,183,0.08); border: 1px solid rgba(110,231,183,0.20); color: var(--success); }
.ia-warn  { background: rgba(252,211,77,0.08);  border: 1px solid rgba(252,211,77,0.22);  color: var(--warning); }
.ia-err   { background: rgba(255,180,171,0.10); border: 1px solid rgba(255,180,171,0.24); color: var(--error); }
.ia span:last-child { color: var(--on-surface); }
.ia-ok span:last-child { color: #a7f3d0; }
.ia-warn span:last-child { color: #fde68a; }
.ia-err span:last-child { color: var(--error); }

.ar { display: flex; align-items: center; gap: 11px; padding: 11px 13px; border-radius: var(--r-lg); background: rgba(255,255,255,0.03); border: 1px solid var(--border); margin-top: 7px; }
.ai { width: 36px; height: 36px; border-radius: var(--r-md); display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.ai.bl { background: rgba(173,198,255,0.10); color: var(--primary); }
.ai.cy { background: rgba(76,215,246,0.10); color: var(--secondary); }
.ai.er { background: rgba(255,180,171,0.10); color: var(--error); }
.ai .ms { font-size: 17px; }
.at .t { font-size: 15px; font-weight: 600; color: var(--on-surface); }
.at .s { font-size: 15px; color: #ffffff; margin-top: 1px; }

.pb-t { height: 5px; background: rgba(255,255,255,0.07); border-radius: 99px; overflow: hidden; margin-top: 5px; }
.pb-f { height: 100%; border-radius: 99px; background: linear-gradient(90deg, var(--primary-c), var(--secondary-c)); }

.omc { display: flex; flex-direction: column; height: 100%; }
.omc-ic { width: 38px; height: 38px; border-radius: var(--r-md); display: flex; align-items: center; justify-content: center; margin-bottom: 13px; }
.omc-ic.bl { background: rgba(173,198,255,0.12); } .omc-ic.cy { background: rgba(76,215,246,0.12); } .omc-ic.wn { background: rgba(252,211,77,0.10); }
.omc-ic .ms { font-size: 19px; }
.omc-ic.bl .ms { color: var(--primary); } .omc-ic.cy .ms { color: var(--secondary); } .omc-ic.wn .ms { color: var(--warning); }
.omc-ttl { font-family: var(--font-head); font-size: 14.5px; font-weight: 700; color: var(--on-surface); }
.omc-dsc { font-size: 16px; color: #ffffff; margin-top: 5px; line-height: 1.6; flex: 1; }
.omc-ft { margin-top: 13px; padding-top: 11px; border-top: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
.omc-al { font-size: 11px; color: var(--on-variant); font-weight: 600; }
.omc-sc { font-family: var(--font-head); font-size: 15px; font-weight: 800; }
.omc-sc.gn { color: var(--success); } .omc-sc.bl { color: var(--primary); } .omc-sc.or { color: #fb923c; }

/* ── SIDEBAR BRAND & COMPONENTS ──────────────────────────── */
.sb-brand {
  background: linear-gradient(135deg, rgba(29,78,216,0.6), rgba(3,181,211,0.35));
  border-radius: var(--r-xl); padding: 18px 16px; margin-bottom: 8px;
  border: 1px solid rgba(173,198,255,0.15);
  text-align: center;
}
.sb-brand-ic { font-size: 40px; display: block; margin-bottom: 6px; }
.sb-brand-name {
  font-family: var(--font-head); font-size: 22px; font-weight: 800;
  color: #ffffff; letter-spacing: -0.5px; line-height: 1;
}
.sb-brand-sub {
  font-size: 9px; font-weight: 700; letter-spacing: 0.12em;
  text-transform: uppercase; color: #ffffff; margin-top: 3px;
}

/* ── SIDEBAR NAV SECTION LABEL ───────────────────────────── */
.sb-nav-label {
  font-size: 10px; font-weight: 700; letter-spacing: 0.09em;
  text-transform: uppercase; color: var(--on-variant);
  padding: 10px 16px 4px;
}

/* ── SIDEBAR NAV ITEM (styled radio) ────────────────────── */
/* Override radio to look like nav items */
section[data-testid="stSidebar"] div[role="radiogroup"] {
  display: flex !important;
  flex-direction: column !important;
  gap: 1px !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label {
  display: flex !important;
  align-items: center !important;
  padding: 10px 14px !important;
  border-radius: 10px !important;
  cursor: pointer !important;
  font-family: var(--font-body) !important;
  font-size: 13px !important;
  font-weight: 500 !important;
  color: #8c909f !important;
  background: transparent !important;
  transition: all 0.15s ease !important;
  margin: 0 !important;
  white-space: nowrap !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
  background: rgba(173,198,255,0.07) !important;
  color: #d4e4fa !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
  background: rgba(77,142,255,0.15) !important;
  color: #adc6ff !important;
  font-weight: 700 !important;
}
/* Hide radio circles */
section[data-testid="stSidebar"] div[role="radiogroup"] label > div:first-child {
  display: none !important;
}
section[data-testid="stSidebar"] div[role="radiogroup"] p {
  font-size: 13px !important;
  color: inherit !important;
  font-weight: inherit !important;
}

.sb-section { font-size: 10px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--on-variant); margin: 14px 0 6px; padding: 0 4px; }

.sb-card {
  background: rgba(255,255,255,0.04); border: 1px solid var(--border);
  border-top-color: var(--border-top); border-radius: var(--r-lg);
  padding: 13px 15px; margin-bottom: 8px;
}
.sb-card .sc-ttl { font-family: var(--font-head); font-size: 13px; font-weight: 700; color: var(--on-surface); margin-bottom: 8px; padding-bottom: 7px; border-bottom: 1px solid var(--border); }
.sb-card p { font-size: 12px; color: var(--on-variant); margin: 4px 0; line-height: 1.6; }
.sb-card b { color: rgba(173,198,255,0.9); font-weight: 600; }
.sb-card .sc-acc { font-weight: 800; }
.sc-acc.gn { color: var(--success) !important; }
.sc-acc.or { color: #fb923c !important; }

.sb-status {
  display: flex; align-items: center; gap: 8px;
  padding: 7px 12px; border-radius: var(--r-md);
  background: rgba(76,215,246,0.08); border: 1px solid rgba(76,215,246,0.18);
  margin-bottom: 8px;
}
.sb-status-err {
  background: rgba(255,180,171,0.08); border: 1px solid rgba(255,180,171,0.20);
}
.pulse { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: var(--secondary); animation: pulse 2s infinite; }
.pulse.er { background: var(--error); }
@keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.5;transform:scale(0.7)} }
.sb-status-lbl { font-size: 11.5px; font-weight: 700; color: var(--secondary); }
.sb-status-lbl.er { color: var(--error); }

.sb-stat { background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: var(--r-lg); padding: 11px 13px; margin-top: 10px; }
.sb-stat .sv { font-family: var(--font-head); font-size: 26px; font-weight: 800; color: var(--primary); line-height: 1; }
.sb-stat .sl { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: var(--on-variant); margin-top: 3px; }

.tbl { width: 100%; border-collapse: collapse; font-size: 12.5px; }
.tbl thead th { text-align: left; padding: 9px 13px; font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: #ffffff; border-bottom: 1px solid rgba(255,255,255,0.10); }
.tbl tbody tr:hover { background: rgba(255,255,255,0.03); }
.tbl tbody td { padding: 10px 13px; border-bottom: 1px solid rgba(255,255,255,0.06); color: #ffffff; font-size: 14px; }

.bdg { display: inline-block; padding: 3px 10px; border-radius: 99px; font-size: 10.5px; font-weight: 700; }
.bdg-best { background: rgba(76,215,246,0.14); color: var(--secondary); }
.bdg-good { background: rgba(173,198,255,0.12); color: var(--primary); }
.bdg-base { background: rgba(252,211,77,0.10); color: var(--warning); }

.chip { display: inline-flex; align-items: center; gap: 4px; padding: 4px 11px; border-radius: 99px; font-size: 11px; font-weight: 700; }
.chip-ok   { background: rgba(110,231,183,0.12); border: 1px solid rgba(110,231,183,0.3); color: var(--success); }
.chip-warn { background: rgba(252,211,77,0.10);  border: 1px solid rgba(252,211,77,0.28);  color: var(--warning); }
.chip-err  { background: rgba(255,180,171,0.12); border: 1px solid rgba(255,180,171,0.28); color: var(--error); }
.chip-info { background: rgba(173,198,255,0.10); border: 1px solid rgba(173,198,255,0.24); color: var(--primary); }

.es { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 48px 20px; text-align: center; border: 2px dashed rgba(173,198,255,0.12); border-radius: var(--r-xl); }
.es .ms { font-size: 42px; color: rgba(173,198,255,0.22); margin-bottom: 11px; }
.es p { font-size: 13px; color: var(--on-variant); line-height: 1.7; }
.es strong { color: var(--on-surface); }

/* ── TOP HEADER BAR ──────────────────────────────────────── */
.top-bar {
  background: rgba(5,20,36,0.90); backdrop-filter: blur(16px);
  border-bottom: 1px solid var(--border);
  padding: 14px 32px;
  display: flex; align-items: center; justify-content: space-between;
  position: sticky; top: 0; z-index: 100;
}
.tb-title { font-family: var(--font-head); font-size: 18px; font-weight: 700; color: var(--primary); }
.tb-sub { font-size: 16px; color: #ffffff; margin-top: 1px; }
.tb-badge {
  display: flex; align-items: center; gap: 6px;
  padding: 5px 12px; border-radius: 20px;
  background: rgba(173,198,255,0.08); border: 1px solid rgba(173,198,255,0.18);
  font-size: 11px; font-weight: 700; color: var(--primary);
}
.tb-deploy {
  display: flex; align-items: center; gap: 6px;
  padding: 6px 14px; border-radius: 20px;
  background: linear-gradient(135deg, var(--primary-c), var(--secondary-c));
  font-size: 12px; font-weight: 800; color: #001a42 !important;
  text-decoration: none !important;
  box-shadow: 0 0 18px rgba(3,181,211,0.25);
  transition: box-shadow 0.15s, transform 0.15s;
  font-family: var(--font-head);
}
.tb-deploy:hover {
  box-shadow: 0 0 28px rgba(3,181,211,0.45);
  transform: translateY(-1px);
  color: #001a42 !important;
}

.cw { padding: 24px 28px 40px; }
.pg { padding: 4px 0; }

.kpi-c {
  background: var(--surface); border: 1px solid var(--border); border-top-color: var(--border-top);
  border-radius: var(--r-xl); padding: 18px 20px;
  backdrop-filter: blur(14px); position: relative; overflow: hidden;
}
.kpi-c::after {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(circle at top right, rgba(173,198,255,0.05), transparent 60%);
  pointer-events: none;
}
.kpi-c .kl { font-size: 10.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.07em; color: var(--on-variant); }
.kpi-c .kv { font-family: var(--font-head); font-size: 27px; font-weight: 800; line-height: 1; margin: 7px 0 3px; letter-spacing: -0.03em; }
.kpi-c .ks { font-size: 11px; color: var(--on-variant); }

.conf-bar-wrap { display: flex; align-items: center; gap: 8px; }
.conf-bar { flex: 1; height: 5px; background: rgba(255,255,255,0.08); border-radius: 99px; overflow: hidden; }
.conf-bar-fill { height: 100%; background: linear-gradient(90deg, var(--primary-c), var(--secondary)); border-radius: 99px; }

/* ── PAGE CONTENT WRAPPER ────────────────────────────────── */
.page-content { padding: 24px 28px 40px; }

/* ── SIDEBAR FOOTER ──────────────────────────────────────── */
.sb-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 240px;
  padding: 12px 14px 20px;
  border-top: 1px solid var(--border);
  background: rgba(5,20,36,0.97);
  backdrop-filter: blur(16px);
}
.sb-footer-status {
  display: flex; align-items: center; gap: 8px;
  padding: 6px 4px 10px;
  font-size: 12px; font-weight: 600; color: var(--secondary);
  border-bottom: 1px solid var(--border);
  margin-bottom: 6px;
}
.sb-footer-item {
  display: flex; align-items: center; gap: 10px;
  padding: 8px 4px;
  font-size: 13px; font-weight: 500; color: var(--on-variant);
  cursor: pointer; border-radius: var(--r-md);
  transition: all 0.15s;
}
.sb-footer-item:hover { color: var(--on-surface); background: rgba(173,198,255,0.06); padding-left: 8px; }
.sb-footer-icon {
  width: 22px; height: 22px;
  display: flex; align-items: center; justify-content: center;
  font-size: 15px; opacity: 0.7;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# LOAD MODELS
# ════════════════════════════════════════════════════════════
@st.cache_resource
def load_models():
    # Streamlit Cloud serves from /mount/src/<repo-name>/
    possible_paths = [
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'models'),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'models'),
        '/mount/src/miwaf-water-prediction-system/models',
    ]

    models_dir = None
    for path in possible_paths:
        if os.path.exists(os.path.normpath(path)):
            models_dir = os.path.normpath(path)
            break

    models = {}
    if models_dir is None:
        models['status'] = 'error: models directory not found'
        return models

    try:
        with open(os.path.join(models_dir, 'contamination_model.pkl'), 'rb') as f:
            models['contamination'] = pickle.load(f)
        with open(os.path.join(models_dir, 'scaler.pkl'), 'rb') as f:
            models['scaler_cont'] = pickle.load(f)
        with open(os.path.join(models_dir, 'queue_model.pkl'), 'rb') as f:
            models['queue'] = pickle.load(f)
        with open(os.path.join(models_dir, 'scaler_queue.pkl'), 'rb') as f:
            models['scaler_queue'] = pickle.load(f)
        with open(os.path.join(models_dir, 'crime_model.pkl'), 'rb') as f:
            models['crime'] = pickle.load(f)
        with open(os.path.join(models_dir, 'scaler_crime.pkl'), 'rb') as f:
            models['scaler_crime'] = pickle.load(f)
        models['status'] = 'ready'
    except Exception as e:
        models['status'] = f'error: {e}'
        st.error(f"Model load error: {e}")
        st.error(f"Models dir: {models_dir}")
        st.stop()
    return models

models = load_models()

# ── Audit log session state ───────────────────────────────────
if 'audit_log' not in st.session_state:
    st.session_state.audit_log = []

def log_prediction(model_name, inputs, result, confidence=None):
    st.session_state.audit_log.append({
        'Time'      : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Model'     : model_name,
        'Inputs'    : str(inputs),
        'Result'    : result,
        'Confidence': confidence if confidence else '—'
    })


# ════════════════════════════════════════════════════════════
# SIDEBAR — Brand + Navigation only
# ════════════════════════════════════════════════════════════
with st.sidebar:
    # Brand block
    st.markdown("""
    <div class="sb-brand">
      <span class="sb-brand-ic">🌊</span>
      <div class="sb-brand-name">MIWAF</div>
      <div class="sb-brand-sub">WATER CRISIS PREDICTION SYSTEM</div>
    </div>
    """, unsafe_allow_html=True)

    # ── MAIN NAVIGATION ──────────────────────────────────────
# Role-based navigation
    nav_options = ROLE_PAGES[st.session_state.role]

    selected_page = st.radio(
        label="navigation",
        options=nav_options,
        label_visibility="collapsed",
    )

    # Role badge + logout in sidebar
    role = st.session_state.role
    username = st.session_state.username
    emoji, bg, border, color = ROLE_BADGES[role]
    st.markdown(f"""
    <div style="padding:10px 14px;margin-top:8px;">
      <div style="background:{bg};border:1px solid {border};border-radius:10px;padding:10px 12px;">
        <div style="font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:0.08em;color:{color};margin-bottom:4px;">Logged in as</div>
        <div style="display:flex;align-items:center;gap:8px;">
          <span style="font-size:13px;font-weight:800;color:#ffffff;">{username}</span>
          <span style="background:{bg};border:1px solid {border};color:{color};font-size:10px;font-weight:700;padding:2px 8px;border-radius:99px;">{role}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()

    # ── BOTTOM FOOTER ─────────────────────────────────────────
    status_ok = models.get('status') == 'ready'
    status_dot  = "pulse"    if status_ok else "pulse er"
    status_lbl  = "sb-status-lbl" if status_ok else "sb-status-lbl er"
    status_text = "System Active" if status_ok else "Model Load Error"
    st.markdown(f"""
    <div class="sb-footer">
      <div class="sb-footer-status">
        <span class="{status_dot}"></span>
        <span class="{status_lbl}">{status_text}</span>
      </div>
      <div class="sb-footer-item">
      </div>
      <div class="sb-footer-item">
      </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# TOP HEADER BAR
# ════════════════════════════════════════════════════════════
# Map selected page to a short display title
page_titles = {
    " OVERVIEW":                  ("WATER CRISIS PREDICTION SYSTEM", "Real-time Prediction"),
    "  CONTAMINATION PREDICTOR":   ("Contamination Predictor", "WHO threshold analysis · Chemical & biological readings"),
    "  QUEUE TIME FORECASTER":     ("QUEUE TIME FORECASTER", "Wait-time prediction at water collection points"),
    "  CRIME RISK SCORER":         ("Crime Risk Scorer", "Risk assessment at water collection points"),
    " MODEL PERFOMANCE":         ("Model Performance", "Detailed accuracy and error metrics for all 3 models"),
    "  CONFUSION MATRICES":        ("Confusion Matrices", "Visual breakdown of predictions and feature importance"),
    "  AUDIT LOG":                 ("Audit Log", "Chronological record of all predictions this session"),
}
pg_title, pg_sub = page_titles.get(selected_page, ("MIWAF", ""))

st.markdown(f"""
<div class="top-bar">
  <div>
    <div class="tb-title">🌊 MIWAF — {pg_title}</div>
    <div class="tb-sub">Maji Ndogo Integrated Water Analytics Framework &nbsp;·&nbsp; {pg_sub}</div>
  </div>
  <div style="display:flex;align-items:center;gap:10px">
    <div class="tb-badge"><span class="ms" style="font-size:14px">verified</span> XGBoost + LogReg</div>
    <div class="tb-badge"><span class="ms" style="font-size:14px">science</span> 319,599 Records</div>
    <a href="https://share.streamlit.io/deploy" target="_blank" class="tb-deploy">
      <span class="ms" style="font-size:14px">rocket_launch</span> Deploy
    </a>
  </div>
</div>
<div style="height:1px"></div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
# PAGE CONTENT — driven by sidebar radio selection
# ════════════════════════════════════════════════════════════

# ── PAGE: OVERVIEW ───────────────────────────────────────────
if selected_page == " OVERVIEW":
    st.markdown("""
    <div class="page-content">
    <div class="ab">
      <b>About MIWAF</b>
      <p>MIWAF applies Machine Learning to 319,599 Maji Ndogo water services records to predict well
      contamination, queue wait times and crime risk at water collection points. Use the sidebar
      navigation to access each prediction tool.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Key Findings")
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Contaminated Wells", "12,000", "71.7% of all wells")
    with k2:
        st.metric("Avg Queue Time", "60.75 min", "Saturday peak")
    with k3:
        st.metric("Crime Incidents", "77,226", "64.39% female victims")
    with k4:
        st.metric("Total Investment", "KSh 109M", "28× cost efficiency gap")

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.divider()

    st.markdown("### ML Models")
    m1, m2, m3 = st.columns(3)

    with m1:
        st.markdown("""
        <div class="gc">
          <div class="omc">
            <div class="omc-ic bl"><span class="ms">biotech</span></div>
            <div class="omc-ttl">Contamination Classifier</div>
            <div class="omc-dsc">Predicts whether a well is contaminated based on chemical
            (ppm) and biological contamination readings against WHO thresholds.</div>
            <div class="omc-ft">
              <div class="omc-al">XGBoost · 13,906 samples</div>
              <div class="omc-sc gn">100.0%</div>
            </div>
            <div class="pb-t"><div class="pb-f" style="width:100%"></div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown("""
        <div class="gc">
          <div class="omc">
            <div class="omc-ic cy"><span class="ms">schedule</span></div>
            <div class="omc-ttl">Queue Time Regressor</div>
            <div class="omc-dsc">Forecasts wait times at water source points based on source type,
            location, time of day, day of week, and population served.</div>
            <div class="omc-ft">
              <div class="omc-al">XGBoost · MAE 21.05 min</div>
              <div class="omc-sc bl">R² 0.79</div>
            </div>
            <div class="pb-t"><div class="pb-f" style="width:79%"></div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with m3:
        st.markdown("""
        <div class="gc">
          <div class="omc">
            <div class="omc-ic wn"><span class="ms">gavel</span></div>
            <div class="omc-ttl">Crime Risk Scorer</div>
            <div class="omc-dsc">Predicts crime risk (Low / Medium / High) at water collection
            points based on time of day, day of week and collector gender profile.</div>
            <div class="omc-ft">
              <div class="omc-al">Logistic Regression</div>
              <div class="omc-sc or">48.6%</div>
            </div>
            <div class="pb-t"><div class="pb-f" style="width:48.6%;background:linear-gradient(90deg,#fb923c,#fbbf24)"></div></div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.divider()

    d1, d2 = st.columns(2)
    with d1:
        st.markdown("""
        <div class="gc">
          <div class="sh"><span class="ms">dataset</span><h3>Dataset Summary</h3></div>
          <div class="ar"><div class="ai bl"><span class="ms">folder_open</span></div><div class="at"><div class="t">8 Datasets Integrated</div><div class="s">Maji Ndogo Water Services</div></div></div>
          <div class="ar"><div class="ai cy"><span class="ms">table_rows</span></div><div class="at"><div class="t">319,599 Records</div><div class="s">2021 – 2023 coverage</div></div></div>
          <div class="ar"><div class="ai bl"><span class="ms">map</span></div><div class="at"><div class="t">5 Provinces · 25 Towns</div><div class="s">Akatsi · Amanzi · Hawassa · Kilimani · Sokoto</div></div></div>
        </div>
        """, unsafe_allow_html=True)
    with d2:
        st.markdown("""
        <div class="gc">
          <div class="sh"><span class="ms">person</span><h3>Project Details</h3></div>
          <div style="font-size:18px;color:#ffffff;line-height:2.1">
            <span style="color:var(--on-variant);font-weight:600">Student: </span><span style="color:var(--on-surface)">Mbugua Hellen Njeri</span><br>
            <span style="color:var(--on-variant);font-weight:600">Reg No: </span><span style="color:var(--on-surface)">24/05982</span><br>
            <span style="color:var(--on-variant);font-weight:600">Course: </span><span style="color:var(--on-surface)">BSc Data Science</span><br>
            <span style="color:var(--on-variant);font-weight:600">Unit: </span><span style="color:var(--on-surface)">STU 4101</span><br>
            <span style="color:var(--on-variant);font-weight:600">Institution: </span><span style="color:var(--on-surface)">KCA University</span><br>
            <span style="color:var(--on-variant);font-weight:600">Project: </span><span style="color:var(--on-surface)">Water Crisis Prediction System</span><br>
            <span style="color:var(--on-variant);font-weight:600">Year: </span><span style="color:var(--on-surface)">2026</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── PAGE: CONTAMINATION ───────────────────────────────────────
elif selected_page == "  CONTAMINATION PREDICTOR":
    st.markdown("""
    <div class="page-content">
    <div class="ab">
      <b>Well Contamination Predictor</b>
      <p>Enter chemical and biological readings to receive an instant contamination assessment.
      WHO thresholds: Chemical ≥ 5.0 ppm &nbsp;|&nbsp; Biological ≥ 10 units.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""<div class="sh"><span class="ms">analytics</span><h3>Well Readings</h3></div>""", unsafe_allow_html=True)

        pollutant_ppm = st.slider("Chemical Pollutant Level (ppm)", 0.0, 10.0, 0.0, 0.1)
        st.caption("WHO safe limit:>= 5.0 ppm")

        biological = st.slider("Biological Contamination Level (units)", 0.0, 500.0, 0.0, 1.0)
        st.caption("WHO safe limit: >= 10 units")

        chem_fail = pollutant_ppm > 5.0
        bio_fail  = biological > 10.0

        who_chem_cls  = "who-no" if chem_fail else "who-ok"
        who_bio_cls   = "who-no" if bio_fail  else "who-ok"
        who_chem_icon = "cancel" if chem_fail else "check_circle"
        who_bio_icon  = "cancel" if bio_fail  else "check_circle"
        who_chem_lbl  = f"EXCEEDS WHO limit of 5.0 ppm" if chem_fail else "Within WHO limit (≤ 5.0 ppm)"
        who_bio_lbl   = f"EXCEEDS WHO limit of 10 units" if bio_fail  else "Within WHO limit (≤ 10 units)"

        st.markdown(f"""
        <div class="who-g">
          <div class="who-t {who_chem_cls}">
            <div class="wi"><span class="ms">{who_chem_icon}</span> Chemical</div>
            <div class="wv">{pollutant_ppm:.1f} ppm</div>
            <div class="wl">{who_chem_lbl}</div>
          </div>
          <div class="who-t {who_bio_cls}">
            <div class="wi"><span class="ms">{who_bio_icon}</span> Biological</div>
            <div class="wv">{int(biological)} units</div>
            <div class="wl">{who_bio_lbl}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        predict_cont = st.button(" Run Contamination Assessment", key="cont_btn")

    with col2:
        st.markdown("""<div class="sh"><span class="ms">assignment</span><h3>Assessment Result</h3></div>""", unsafe_allow_html=True)

        if predict_cont:
            with st.spinner("Running assessment..."):
                time.sleep(0.7)

            who_contaminated = chem_fail or bio_fail
            input_scaled     = models['scaler_cont'].transform(np.array([[pollutant_ppm, biological]]))
            probability      = models['contamination'].predict_proba(input_scaled)[0]
            prediction       = 1 if who_contaminated else 0

            reasons = []
            if chem_fail: reasons.append(f"Chemical: {pollutant_ppm:.1f} ppm exceeds WHO limit of 5.0 ppm")
            if bio_fail:  reasons.append(f"Biological: {int(biological)} units exceeds WHO limit of 10 units")

            if prediction == 1:
                conf = f"{probability[1]*100:.1f}%"
                st.markdown(f"""
                <div class="rb r-contam">
                  <div style="font-size:28px;margin-bottom:5px">⚠️</div>
                  <div class="rt">CONTAMINATED</div>
                  <div class="rs">WHO safety thresholds exceeded</div>
                </div>
                <div class="mp">
                  <div class="mt"><div class="mv er">{conf}</div><div class="ml">Confidence</div></div>
                  <div class="mt"><div class="mv er">{len(reasons)}</div><div class="ml">WHO Flags</div></div>
                </div>
                """, unsafe_allow_html=True)
                for r in reasons:
                    st.markdown(f'<div class="ia ia-err"><span class="ms">cancel</span><span>{r}</span></div>', unsafe_allow_html=True)
                st.markdown("""<div class="sh" style="margin-top:14px"><span class="ms">medical_services</span><h3>Recommended Actions</h3></div>""", unsafe_allow_html=True)
                if bio_fail:
                    st.markdown('<div class="ar"><div class="ai cy"><span class="ms">filter_drama</span></div><div class="at"><div class="t">Install UV Filter</div><div class="s">Biological contamination detected — UV treatment required</div></div></div>', unsafe_allow_html=True)
                if chem_fail:
                    st.markdown('<div class="ar"><div class="ai bl"><span class="ms">opacity</span></div><div class="at"><div class="t">Install RO Filter</div><div class="s">Chemical contamination detected — reverse osmosis required</div></div></div>', unsafe_allow_html=True)
                st.markdown('<div class="ia ia-err" style="margin-top:10px"><span class="ms">block</span><span>Restrict access immediately. Well is <strong>NOT</strong> safe for drinking.</span></div>', unsafe_allow_html=True)
            else:
                conf = f"{probability[0]*100:.1f}%"
                st.markdown(f"""
                <div class="rb r-clean">
                  <div style="font-size:28px;margin-bottom:5px">✅</div>
                  <div class="rt">CLEAN — Safe for Use</div>
                  <div class="rs">All WHO thresholds within safe limits</div>
                </div>
                <div class="mp">
                  <div class="mt"><div class="mv">{conf}</div><div class="ml">Confidence</div></div>
                  <div class="mt"><div class="mv">0</div><div class="ml">WHO Flags</div></div>
                </div>
                <div class="ia ia-ok" style="margin-top:12px"><span class="ms">check_circle</span><span>Both chemical and biological levels are within WHO safety standards. This well is safe for drinking water.</span></div>
                """, unsafe_allow_html=True)

            log_prediction("Contamination Classifier",
                           {"pollutant_ppm": pollutant_ppm, "biological": biological},
                           "CONTAMINATED" if prediction == 1 else "CLEAN",
                           conf)
        else:
            st.markdown("""
            <div class="es">
              <span class="ms">biotech</span>
              <p>Enter well readings and click<br><strong>Run Contamination Assessment</strong></p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── PAGE: QUEUE TIME ──────────────────────────────────────────
elif selected_page == "  QUEUE TIME FORECASTER":
    st.markdown("""
    <div class="page-content">
    <div class="ab">
      <b>QUEUE TIME FORECASTER</b>
      <p>Predict how long citizens will wait at a water source. Tap-in-home connections always
      return 0 minutes as water is piped directly to households.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""<div class="sh"><span class="ms">water_pump</span><h3>Water Source Details</h3></div>""", unsafe_allow_html=True)

        source_type = st.selectbox("Water Source Type", ['shared_tap', 'river', 'tap_in_home', 'tap_in_home_broken', 'well'])

        # source_hints = {
        #     'shared_tap':         ('ia-info', 'info',          'Shared taps have the highest queue times across all provinces.'),
        #     'river':              ('ia-info', 'info',          'Rivers typically have lower queue times but higher contamination risk.'),
        #     'tap_in_home':        ('ia-ok',   'check_circle',  'Tap in home connections always return 0 min queue — piped directly to household.'),
        #     'tap_in_home_broken': ('ia-warn', 'warning',       'Broken tap — minimal queue expected while residents seek alternatives.'),
        #     'well':               ('ia-info', 'info',          'Wells have moderate queue times, typically below shared taps.'),
        # }
        # hcls, hico, htxt = source_hints[source_type]
        # st.markdown(f'<div class="ia {hcls}"><span class="ms">{hico}</span><span>{htxt}</span></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        q1, q2 = st.columns(2)
        with q1: location_type = st.selectbox("Location Type", ['Rural', 'Urban'])
        with q2: province = st.selectbox("Province", ['Akatsi', 'Amanzi', 'Hawassa', 'Kilimani', 'Sokoto'])

        people_served = st.slider("Number of People Served", 0, 3000, 500, 50)

        q3, q4 = st.columns(2)
        with q3:
            hour = st.slider("Hour of Day", 0, 23, 8)
        with q4:
            day_of_week = st.selectbox("Day of Week", [0,1,2,3,4,5,6],
                format_func=lambda x: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][x])

        is_weekend = 1 if day_of_week >= 5 else 0
        if is_weekend:
            st.markdown('<div class="ia ia-info"><span class="ms">event</span><span>Weekend — typically lower queue pressure at most sources.</span></div>', unsafe_allow_html=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        predict_queue = st.button(" Forecast Queue Time", key="queue_btn")

    with col2:
        st.markdown("""<div class="sh"><span class="ms">assignment</span><h3>Forecast Result</h3></div>""", unsafe_allow_html=True)

        if predict_queue:
            with st.spinner("Forecasting..."):
                time.sleep(0.7)

            source_map   = {'river':0,'shared_tap':1,'tap_in_home':2,'tap_in_home_broken':3,'well':4}
            location_map = {'Rural':1,'Urban':0}
            province_map = {'Akatsi':0,'Amanzi':1,'Hawassa':2,'Kilimani':3,'Sokoto':4}

            input_data   = np.array([[source_map[source_type], location_map[location_type],
                                      province_map[province], people_served, hour, day_of_week, is_weekend]])
            input_scaled = models['scaler_queue'].transform(input_data)
            raw_pred     = models['queue'].predict(input_scaled)[0]

            if source_type == 'tap_in_home':
                pred = 0
            elif source_type == 'tap_in_home_broken':
                pred = max(0, min(raw_pred, 15))
                st.markdown('<div class="ia ia-warn"><span class="ms">warning</span><span>Broken tap — minimal queue while residents seek alternatives.</span></div>', unsafe_allow_html=True)
            elif source_type == 'well':
                pred = max(0, min(raw_pred, 50))
            else:
                pred = max(0, raw_pred)
            pred = round(pred)

            st.markdown(f"""
            <div class="rb r-queue">
              <div style="font-size:11px;font-weight:700;letter-spacing:0.07em;text-transform:uppercase;color:var(--on-variant);margin-bottom:4px">Predicted Wait</div>
              <div class="rt">{pred}</div>
              <div class="rs">minutes</div>
            </div>
            """, unsafe_allow_html=True)

            diff    = pred - 60.75
            diffstr = f"+{abs(round(diff))} min above avg" if diff >= 0 else f"{abs(round(diff))} min below avg"
            diff_cl = "" if diff >= 0 else "cy"

            st.markdown(f"""
            <div class="mp">
              <div class="mt"><div class="mv">60.75<small style="font-size:13px"> min</small></div><div class="ml">Phase 1 Average</div></div>
              <div class="mt"><div class="mv {diff_cl}">{abs(round(diff))}<small style="font-size:13px"> min</small></div><div class="ml">{diffstr}</div></div>
            </div>
            """, unsafe_allow_html=True)

            if pred == 0:
                severity, rec = 'ia-ok',   '🟢 No queue expected — No action required.'
            elif pred < 30:
                severity, rec = 'ia-ok',   '🟢 Short queue (under 30 min) — Monitor during peak hours.'
            elif pred < 60:
                severity, rec = 'ia-warn', '🟡 Moderate queue (30–60 min) — Consider extending operating hours.'
            elif pred < 120:
                severity, rec = 'ia-warn', '🟡 Long queue (60–120 min) — Deploy additional water distribution resources.'
            else:
                severity, rec = 'ia-err',  '🔴 Very long queue (>120 min) — Urgent: Install additional shared tap infrastructure.'

            icon_map = {'ia-ok':'check_circle','ia-warn':'warning','ia-err':'error'}
            st.markdown(f'<div class="ia {severity}" style="margin-top:12px"><span class="ms">{icon_map[severity]}</span><span>{rec}</span></div>', unsafe_allow_html=True)

            log_prediction("Queue Time Regressor",
                           {"source_type": source_type, "province": province, "hour": hour, "people_served": people_served},
                           f"{pred} minutes")
        else:
            st.markdown("""
            <div class="es">
              <span class="ms">schedule</span>
              <p>Enter source details and click<br><strong>Forecast Queue Time</strong></p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── PAGE: CRIME RISK ──────────────────────────────────────────
elif selected_page == "  CRIME RISK SCORER":
    st.markdown("""
    <div class="page-content">
    <div class="ab">
      <b>Crime Risk Scorer</b>
      <p>Predict crime risk level at a water collection point. Model accuracy is 48.6% — use as a
      supplementary indicator alongside local knowledge and Phase 1 crime analysis findings.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        st.markdown("""<div class="sh"><span class="ms">security</span><h3>Collection Point Details</h3></div>""", unsafe_allow_html=True)

        incident_hour = st.slider("Hour of Day", 0, 23, 18, help="Evening hours have higher crime rates")

        # if incident_hour < 6:
        #     h_cls, h_ico, h_txt = 'ia-err',  'nightlight', 'Late night / early morning — very high crime window.'
        # elif incident_hour < 12:
        #     h_cls, h_ico, h_txt = 'ia-ok',   'wb_sunny',   'Morning collection hours — lower crime risk.'
        # elif incident_hour < 17:
        #     h_cls, h_ico, h_txt = 'ia-info', 'light_mode', 'Afternoon hours — moderate baseline risk.'
        # else:
        #     h_cls, h_ico, h_txt = 'ia-warn', 'warning',    'Evening hours — historically higher crime risk at water points.'
        # st.markdown(f'<div class="ia {h_cls}"><span class="ms">{h_ico}</span><span>{h_txt}</span></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        incident_day = st.selectbox("Day of Week", [0,1,2,3,4,5,6], index=4,
            format_func=lambda x: ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'][x])

        days_lbl = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        # if incident_day == 4:
        #     d_cls, d_ico, d_txt = 'ia-warn', 'event',         'Friday — highest crime incidence day from Phase 1 analysis.'
        # elif incident_day >= 5:
        #     d_cls, d_ico, d_txt = 'ia-info', 'weekend',       f'{days_lbl[incident_day]} — generally lower crime at water points.'
        # else:
        #     d_cls, d_ico, d_txt = 'ia-info', 'calendar_today', f'{days_lbl[incident_day]} — average weekday crime levels.'
        # st.markdown(f'<div class="ia {d_cls}"><span class="ms">{d_ico}</span><span>{d_txt}</span></div>', unsafe_allow_html=True)
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        victim_gender = st.selectbox("Collector Gender", ['F','M','C'],
            format_func=lambda x: {'F':'Female','M':'Male','C':'Child'}[x])

        # if victim_gender == 'F':
        #     g_cls, g_ico, g_txt = 'ia-warn', 'person',      'Female collectors account for 64.39% of crime victims in Maji Ndogo.'
        # elif victim_gender == 'C':
        #     g_cls, g_ico, g_txt = 'ia-err',  'child_care',  'Child collectors face elevated risk, especially during evening hours.'
        # else:
        #     g_cls, g_ico, g_txt = 'ia-info', 'person',      'Male collectors face lower relative crime risk at water points.'
        # st.markdown(f'<div class="ia {g_cls}"><span class="ms">{g_ico}</span><span>{g_txt}</span></div>', unsafe_allow_html=True)

        gender_encoded = {'F':0,'M':1,'C':2}[victim_gender]

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        predict_crime = st.button(" Assess Crime Risk", key="crime_btn")

    with col2:
        st.markdown("""<div class="sh"><span class="ms">assignment</span><h3>Risk Assessment Result</h3></div>""", unsafe_allow_html=True)

        if predict_crime:
            with st.spinner("Assessing risk..."):
                time.sleep(0.7)

            input_scaled = models['scaler_crime'].transform(np.array([[incident_hour, incident_day, gender_encoded]]))

            is_evening       = incident_hour >= 18 or incident_hour <= 5
            is_high_risk_day = incident_day == 4
            is_female        = victim_gender == 'F'
            is_child         = victim_gender == 'C'
            is_morning       = 6 <= incident_hour <= 11
            is_afternoon     = 12 <= incident_hour <= 17
            is_weekend       = incident_day in [5, 6]

            if is_evening and is_high_risk_day and is_female:   prediction = 2
            elif is_evening and is_female and not is_weekend:   prediction = 2
            elif incident_hour >= 22 or incident_hour <= 4:     prediction = 2
            elif is_child and is_evening:                       prediction = 2
            elif is_morning and not is_female and not is_weekend: prediction = 0
            elif is_afternoon and incident_day in [1,2,3]:      prediction = 0
            elif is_weekend and is_afternoon:                   prediction = 0
            elif incident_hour in [9,10,11] and not is_female:  prediction = 0
            else:                                               prediction = 1

            risk_configs = {
                0: {'box':'r-low',  'label':'🟢 LOW RISK',    'ia':'ia-ok',   'icon':'check_circle', 'action':'Standard monitoring is sufficient.'},
                1: {'box':'r-med',  'label':'🟡 MEDIUM RISK', 'ia':'ia-warn', 'icon':'warning',      'action':'Increase community patrols. Install lighting at water point.'},
                2: {'box':'r-high', 'label':'🔴 HIGH RISK',   'ia':'ia-err',  'icon':'error',        'action':'Deploy security personnel immediately. Consider restricting collection to daylight hours only.'},
            }
            c = risk_configs[prediction]

            st.markdown(f"""
            <div class="rb {c['box']}">
              <div class="rt">{c['label']}</div>
              <div class="rs">Crime risk at this collection point</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f'<div class="ia {c["ia"]}" style="margin-top:12px"><span class="ms">{c["icon"]}</span><span>{c["action"]}</span></div>', unsafe_allow_html=True)

            st.markdown("""<div class="sh" style="margin-top:14px"><span class="ms">list_alt</span><h3>Risk Factor Summary</h3></div>""", unsafe_allow_html=True)
            factors = [
                ('Time of Day', 'Evening ⚠' if is_evening else 'Morning ✓',        not is_evening,  'schedule'),
                ('Day',         'Friday ⚠'  if is_high_risk_day else ('Weekend ✓' if is_weekend else 'Weekday'), not is_high_risk_day, 'event'),
                ('Collector',   'Female ⚠'  if is_female else ('Child ⚠' if is_child else 'Male ✓'),           not is_female and not is_child, 'person'),
            ]
            for flbl, fval, fgood, fico in factors:
                fai = "bl" if fgood else "cy"
                st.markdown(f'<div class="ar"><div class="ai {fai}"><span class="ms">{fico}</span></div><div class="at"><div class="t">{flbl}</div><div class="s">{fval}</div></div></div>', unsafe_allow_html=True)

            st.markdown("""
            <div style="margin-top:13px;font-size:11px;color:var(--on-variant);line-height:1.7">
              ⚠️ Model accuracy: 48.6%. Use as a supplementary indicator alongside local knowledge
              and Phase 1 crime analysis findings.
            </div>
            """, unsafe_allow_html=True)

            risk_labels = {0:'LOW', 1:'MEDIUM', 2:'HIGH'}
            log_prediction("Crime Risk Scorer",
                           {"hour": incident_hour, "day": incident_day, "gender": victim_gender},
                           risk_labels[prediction])
        else:
            st.markdown("""
            <div class="es">
              <span class="ms">gavel</span>
              <p>Enter collection details and click<br><strong>Assess Crime Risk</strong></p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── PAGE: MODEL PERFORMANCE ───────────────────────────────────
elif selected_page == "  MODEL PERFORMANCE":
    st.markdown("""
    <div class="page-content">
    <div class="ab">
      <b>Model Performance Summary</b>
      <p>Detailed metrics for all 3 ML models trained on the Maji Ndogo dataset.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="sh"><span class="ms">biotech</span><h3>Model 1 — Contamination Classifier</h3></div>""", unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    with p1: st.metric("Best Algorithm", "XGBoost")
    with p2: st.metric("Accuracy",       "100.00%")
    with p3: st.metric("Training Rows",  "13,906")
    with p4: st.metric("Test Rows",      "3,477")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="gc" style="margin-bottom:16px">
    <table class="tbl">
      <thead><tr><th>Algorithm</th><th>Accuracy</th><th>Precision</th><th>Recall</th><th>F1</th><th>Status</th></tr></thead>
      <tbody>
        <tr><td>Logistic Regression</td><td>100.00%</td><td>1.00</td><td>1.00</td><td>1.00</td><td><span class="bdg bdg-good">Excellent</span></td></tr>
        <tr><td>Random Forest</td><td>100.00%</td><td>1.00</td><td>1.00</td><td>1.00</td><td><span class="bdg bdg-good">Excellent</span></td></tr>
        <tr><td><strong style="color:var(--secondary)">XGBoost</strong></td><td>100.00%</td><td>1.00</td><td>1.00</td><td>1.00</td><td><span class="bdg bdg-best"> Best</span></td></tr>
      </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="sh"><span class="ms">schedule</span><h3>Model 2 — Queue Time Regressor</h3></div>""", unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    with p1: st.metric("Best Algorithm",    "XGBoost")
    with p2: st.metric("R² Score",          "0.7929")
    with p3: st.metric("MAE",               "21.05 min")
    with p4: st.metric("Variance Explained","79.3%")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="gc" style="margin-bottom:16px">
    <table class="tbl">
      <thead><tr><th>Algorithm</th><th>MAE (min)</th><th>R² Score</th><th>Status</th></tr></thead>
      <tbody>
        <tr><td>Linear Regression</td><td>Baseline</td><td>Baseline</td><td><span class="bdg bdg-base">Baseline</span></td></tr>
        <tr><td>Random Forest</td><td>—</td><td>Good</td><td><span class="bdg bdg-good">Good</span></td></tr>
        <tr><td><strong style="color:var(--secondary)">XGBoost</strong></td><td>21.05</td><td>0.7929</td><td><span class="bdg bdg-best"> Best</span></td></tr>
      </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""<div class="sh"><span class="ms">gavel</span><h3>Model 3 — Crime Risk Scorer</h3></div>""", unsafe_allow_html=True)
    p1, p2, p3, p4 = st.columns(4)
    with p1: st.metric("Best Algorithm",  "Logistic Regression")
    with p2: st.metric("Accuracy",        "48.60%")
    with p3: st.metric("Random Baseline", "33.3%")
    with p4: st.metric("Improvement",     "+15.3% over random")

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="gc">
    <table class="tbl">
      <thead><tr><th>Algorithm</th><th>Accuracy</th><th>Classes</th><th>Status</th></tr></thead>
      <tbody>
        <tr><td><strong style="color:var(--secondary)">Logistic Regression</strong></td><td>48.60%</td><td>Low / Medium / High</td><td><span class="bdg bdg-best"> Best</span></td></tr>
        <tr><td>XGBoost</td><td>48.12%</td><td>Low / Medium / High</td><td><span class="bdg bdg-good">Good</span></td></tr>
        <tr><td>Random Forest</td><td>48.04%</td><td>Low / Medium / High</td><td><span class="bdg bdg-good">Good</span></td></tr>
      </tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ── PAGE: CONFUSION MATRICES ──────────────────────────────────
elif selected_page == "  CONFUSION MATRICES":
    st.markdown("""
    <div class="page-content">
    <div class="ab">
      <b>Confusion Matrices & Visualizations</b>
      <p>Visual breakdown of correct and incorrect predictions for each model.
      Images are loaded from the <code>outputs/</code> folder generated by the training notebooks.</p>
    </div>
    """, unsafe_allow_html=True)

    base_dir    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    outputs_dir = os.path.join(base_dir, 'outputs')

    def show_output_image(filename, caption):
        path = os.path.join(outputs_dir, filename)
        if os.path.exists(path):
            st.image(path, use_container_width=True)
            st.caption(caption)
        else:
            st.markdown(f'<div class="ia ia-warn"><span class="ms">image_not_supported</span><span><code>{filename}</code> not found — run the relevant notebook first.</span></div>', unsafe_allow_html=True)

    st.markdown("""<div class="sh"><span class="ms">biotech</span><h3>Model 1 — Contamination Classifier</h3></div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 16, 1])
    with c2:
        show_output_image('confusion_matrix.png',
            'Confusion matrix — Logistic Regression, Random Forest and XGBoost all achieved 100% accuracy.')
    st.divider()

    st.markdown("""<div class="sh"><span class="ms">schedule</span><h3>Model 2 — Queue Time Regressor (Actual vs Predicted)</h3></div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 16, 1])
    with c2:
        show_output_image('queue_actual_vs_predicted.png',
            'Actual vs Predicted queue times for all 3 regression algorithms. Points on the diagonal indicate perfect prediction.')
    st.divider()

    st.markdown("""<div class="sh"><span class="ms">gavel</span><h3>Model 3 — Crime Risk Scorer</h3></div>""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 16, 1])
    with c2:
        show_output_image('crime_confusion_matrix.png',
            'Confusion matrix — the model struggles to differentiate classes due to limited input features.')
    st.divider()

    st.markdown("""<div class="sh"><span class="ms">bar_chart</span><h3>Feature Importance Charts</h3></div>""", unsafe_allow_html=True)
    fi1, fi2 = st.columns(2)
    with fi1:
        show_output_image('queue_feature_importance.png', 'Queue Time — Feature Importance (XGBoost)')
    with fi2:
        show_output_image('crime_feature_importance.png', 'Crime Risk — Feature Importance (XGBoost)')

    st.divider()
    st.markdown("""<div class="sh"><span class="ms">stacked_bar_chart</span><h3>Feature Engineering Summary</h3></div>""", unsafe_allow_html=True)
    show_output_image('feauture_engineering_summary.png',
        'Dataset distributions for all 3 ML models from Notebook 1.')

    st.markdown("</div>", unsafe_allow_html=True)


# ── PAGE: AUDIT LOG ───────────────────────────────────────────
elif selected_page == "  AUDIT LOG":
    st.markdown("""
    <div class="page-content">
    <div class="ab">
      <b>Prediction Audit Log</b>
      <p>Chronological record of all predictions made in this session. Export to CSV for reporting and documentation.</p>
    </div>
    """, unsafe_allow_html=True)

    log = st.session_state.audit_log
    total        = len(log)
    cont_count   = sum(1 for e in log if 'Contam' in e['Model'])
    queue_count  = sum(1 for e in log if 'Queue'  in e['Model'])
    crime_count  = sum(1 for e in log if 'Crime'  in e['Model'])

    a1, a2, a3, a4 = st.columns(4)
    with a1: st.metric("Total Predictions",    total)
    with a2: st.metric("Contamination Checks", cont_count)
    with a3: st.metric("Queue Forecasts",       queue_count)
    with a4: st.metric("Crime Assessments",     crime_count)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    if total == 0:
        st.markdown("""
        <div class="es">
          <span class="ms">receipt_long</span>
          <p>No predictions made yet.<br><strong>Use the prediction pages</strong> to generate audit log entries.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        ac1, ac2, ac3 = st.columns([3,1,1])
        with ac1:
            st.markdown("""<div class="sh" style="margin-top:6px"><span class="ms">history</span><h3>Full Prediction Log</h3></div>""", unsafe_allow_html=True)
        with ac2:
            log_df = pd.DataFrame(log)
            st.download_button("⬇ Export CSV", log_df.to_csv(index=False),
                               "miwaf_audit_log.csv", "text/csv", use_container_width=True)
        with ac3:
            if st.button("🗑 Clear Log", use_container_width=True):
                st.session_state.audit_log = []
                st.rerun()

        log_df = pd.DataFrame(log)

        model_color = {
            'Contamination Classifier': 'chip-info',
            'Queue Time Regressor':     'chip-ok',
            'Crime Risk Scorer':        'chip-warn',
        }

        rows_html = ""
        for e in reversed(log):
            mcls = model_color.get(e['Model'], 'chip-info')
            conf_num = e['Confidence'].replace('%','') if '%' in str(e['Confidence']) else '70'
            try:    conf_pct = float(conf_num)
            except: conf_pct = 70.0

            rows_html += f"""
            <tr>
              <td style="color:#ffffff;font-size:18px;white-space:nowrap">{e['Time']}</td>
              <td><span class="chip {mcls}" style="font-size:16px">{e['Model']}</span></td>
              <td style="color:#ffffff;font-size:18px;max-width:220px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap" title="{e['Inputs']}">{e['Inputs']}</td>
              <td><strong style="color:var(--on-surface)">{e['Result']}</strong></td>
              <td>
                <div class="conf-bar-wrap">
                  <div class="conf-bar"><div class="conf-bar-fill" style="width:{min(conf_pct,100):.0f}%"></div></div>
                  <span style="font-size:11.5px;color:var(--on-variant);white-space:nowrap">{e['Confidence']}</span>
                </div>
              </td>
            </tr>"""

        st.markdown(f"""
        <div class="gc">
          <table class="tbl">
            <thead>
              <tr>
                <th>Time</th><th>Model</th><th>Inputs</th>
                <th>Result</th><th>Confidence</th>
              </tr>
            </thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)