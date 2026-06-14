"""
NAVIGO — Smart Autonomous Campus Delivery Ecosystem
Streamlit prototype · All data simulated/hardcoded

Run:  streamlit run app.py
Deps: pip install streamlit plotly
"""

import streamlit as st
import plotly.graph_objects as go
import datetime, random
import pandas as pd

# ── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NAVIGO — The future of Last-mile logistics",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── PALETTE ──────────────────────────────────────────────────────────────────
NAVY    = "#0a2540"
BLUE    = "#4589f5"
TEAL    = "#06b6d4"
PURPLE  = "#8b5cf6"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER  = "#ef4444"
BG      = "#eef2ff"

# ── GLOBAL CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
/* Body */
[data-testid="stAppViewContainer"] {{ background: {BG}; }}
[data-testid="block-container"]    {{ padding-top:1.4rem; padding-bottom:2.5rem; }}

/* Sidebar */
[data-testid="stSidebar"] {{ background: linear-gradient(180deg,#071a30 0%,{NAVY} 100%) !important; }}
[data-testid="stSidebar"] * {{ color:#e2e8f0 !important; }}
[data-testid="stSidebar"] .stButton > button {{
    width:100%; background:transparent; border:none; text-align:left;
    padding:10px 16px; border-radius:10px; color:#e2e8f0 !important;
    font-size:14px; transition:all .2s; margin-bottom:2px;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background:rgba(69,137,245,0.25) !important;
    color:white !important;
}}

/* Cards */
.card {{
    background:white; border-radius:18px; padding:22px 20px;
    box-shadow:0 4px 20px rgba(10,37,64,.09); margin-bottom:16px;
}}
.metric-card {{
    background:white; border-radius:16px; padding:22px 18px;
    box-shadow:0 4px 18px rgba(10,37,64,.08); text-align:center;
    transition:transform .2s,box-shadow .2s;
}}
.metric-card:hover {{ transform:translateY(-4px); box-shadow:0 10px 30px rgba(10,37,64,.15); }}

.hero-card {{
    background:linear-gradient(135deg,#071a30 0%,#0f3460 50%,#1a5276 100%);
    border-radius:24px; padding:36px 32px; color:white; margin-bottom:28px;
    box-shadow:0 8px 32px rgba(10,37,64,.25); position:relative; overflow:hidden;
}}
.hero-card::before {{
    content:''; position:absolute; top:-60px; right:-60px;
    width:220px; height:220px; border-radius:50%;
    background:rgba(69,137,245,0.15);
}}
.hero-card::after {{
    content:''; position:absolute; bottom:-40px; left:30%;
    width:140px; height:140px; border-radius:50%;
    background:rgba(6,182,212,0.10);
}}

.notif-card {{
    border-left:4px solid {BLUE}; background:white;
    border-radius:0 14px 14px 0; padding:14px 18px;
    margin-bottom:10px; box-shadow:0 2px 10px rgba(0,0,0,.05);
    transition:transform .2s,box-shadow .2s;
}}
.notif-card:hover {{ transform:translateX(4px); box-shadow:0 6px 20px rgba(10,37,64,.12); }}

.step-card {{
    background:white; border-radius:16px; padding:24px 18px; text-align:center;
    box-shadow:0 4px 16px rgba(10,37,64,.08);
    transition:transform .2s,box-shadow .2s; height:100%;
}}
.step-card:hover {{ transform:translateY(-5px); box-shadow:0 12px 32px rgba(10,37,64,.15); }}

/* Badges */
.badge-success {{ background:{SUCCESS}22; color:{SUCCESS}; border-radius:20px; padding:4px 12px; font-size:12px; font-weight:700; }}
.badge-info    {{ background:{BLUE}22;    color:{BLUE};    border-radius:20px; padding:4px 12px; font-size:12px; font-weight:700; }}
.badge-warning {{ background:{WARNING}22; color:{WARNING}; border-radius:20px; padding:4px 12px; font-size:12px; font-weight:700; }}
.badge-danger  {{ background:{DANGER}22;  color:{DANGER};  border-radius:20px; padding:4px 12px; font-size:12px; font-weight:700; }}
.badge-purple  {{ background:{PURPLE}22;  color:{PURPLE};  border-radius:20px; padding:4px 12px; font-size:12px; font-weight:700; }}

/* Buttons */
.stButton > button {{
    background:linear-gradient(135deg,{BLUE},{TEAL}); color:white; border:none;
    border-radius:12px; font-weight:700; padding:.5rem 1.5rem;
    transition:all .2s; letter-spacing:.3px;
}}
.stButton > button:hover {{
    background:linear-gradient(135deg,#2d6fd4,#0891b2) !important;
    color:white !important; border:none !important;
    transform:translateY(-1px); box-shadow:0 6px 16px rgba(69,137,245,.4) !important;
}}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea,
.stSelectbox > div > div {{
    border-radius:12px !important;
    border:2px solid #e2e8f6 !important;
    background:#fafbff !important;
}}
.stTextInput > div > div > input:focus,
.stTextArea  > div > div > textarea:focus {{
    border-color:{BLUE} !important;
    box-shadow:0 0 0 3px rgba(69,137,245,.15) !important;
}}

/* Progress */
.stProgress > div > div > div > div {{ background:linear-gradient(90deg,{BLUE},{TEAL}) !important; }}

/* Tabs */
.stTabs [data-baseweb="tab"]           {{ font-weight:700; font-size:14px; }}
.stTabs [data-baseweb="tab-highlight"] {{ background:linear-gradient(90deg,{BLUE},{TEAL}) !important; }}

/* Animations */
@keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:.35; }} }}
.pulse {{ animation:pulse 1.6s infinite; }}
@keyframes float {{ 0%,100% {{ transform:translateY(0); }} 50% {{ transform:translateY(-6px); }} }}
.float {{ animation:float 3s ease-in-out infinite; }}

/* Metric text visibility fix */
[data-testid="stMetricValue"]       {{ color:{NAVY} !important; font-weight:800 !important; }}
[data-testid="stMetricLabel"]       {{ color:#64748b !important; font-weight:600 !important; }}
[data-testid="stMetricDeltaIcon--up"]   {{ color:{SUCCESS} !important; }}
[data-testid="stMetricDeltaIcon--down"] {{ color:{DANGER}  !important; }}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE ─────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "Home",
        "active_delivery": None,   # holds the latest submitted delivery dict
        "requests": [
            {"id":"NAV-1029","name":"Ananya S.","category":"Food",     "pickup":"Hostel A",      "dropoff":"Library",       "priority":"Normal",   "status":"Delivered","ts":"10:32 AM"},
            {"id":"NAV-1028","name":"Rohan M.", "category":"Parcel",   "pickup":"Cafeteria",     "dropoff":"Hostel B",      "priority":"Urgent",   "status":"En Route", "ts":"10:45 AM"},
            {"id":"NAV-1027","name":"Priya K.", "category":"Medicines","pickup":"Medical Centre","dropoff":"Academic Block","priority":"Emergency","status":"Delivered","ts":"09:58 AM"},
            {"id":"NAV-1026","name":"Vijay R.", "category":"Documents","pickup":"Academic Block","dropoff":"Library",       "priority":"Normal",   "status":"Delivered","ts":"09:20 AM"},
        ],
        "notifications": [
            {"type":"success","title":"Delivery Completed","body":"Package NAV-1029 delivered to Library.",           "time":"2 min ago"},
            {"type":"info",   "title":"TURBO En Route",    "body":"TURBO heading from Cafeteria to Hostel B.",        "time":"8 min ago"},
            {"type":"info",   "title":"Request Confirmed", "body":"Delivery NAV-1028 assigned to TURBO.",             "time":"10 min ago"},
            {"type":"warning","title":"Path Rerouted",     "body":"TURBO rerouting — obstacle near Cafeteria.",       "time":"1 hr ago"},
            {"type":"warning","title":"Battery Alert",     "body":"TURBO #4 battery at 15%. Returning after delivery.","time":"2 hrs ago"},
            {"type":"error",  "title":"GPS Degraded",      "body":"Signal weak. Backup navigation active.",           "time":"3 hrs ago"},
        ],
        "chat_messages": [
            {"role":"assistant","text":"Hello! I'm the NAVIGO support bot. How can I help you today?"},
        ],
        "feedback_list": [],
        "maintenance_reports": [
            {"id":"MNT-001","issue":"Battery Problem","desc":"TURBO #4 battery depletes faster than expected.","status":"In Progress","reported":"Jun 12"},
            {"id":"MNT-002","issue":"Sensor Issue",   "desc":"Proximity sensor false alerts on TURBO #2.",   "status":"Resolved",   "reported":"Jun 10"},
        ],
        "tracking_step": 2,
        "tracking_eta":  512,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
PAGES = [
    ("🏠","Home"), ("📦","Request Delivery"), ("📍","Live Tracking"),
    ("🔔","Notifications"), ("💬","Helpdesk"), ("⭐","Feedback"),
    ("🔧","Maintenance"), ("📊","Community Dashboard"),
]

with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:24px 0 20px;'>
        <div class="float" style='font-size:40px;'>🚚</div>
        <div style='font-size:26px;font-weight:900;color:white;letter-spacing:3px;margin:8px 0 4px;'>NAVIGO</div>
        <div style='font-size:11px;color:#64748b;margin-bottom:14px;letter-spacing:1px;'>SMART CAMPUS DELIVERY</div>
        <div style='background:rgba(34,197,94,.15);border:1px solid rgba(34,197,94,.3);
                    border-radius:20px;padding:6px 14px;display:inline-block;font-size:12px;color:{SUCCESS};'>
            <span class='pulse' style='display:inline-block;width:7px;height:7px;
            background:{SUCCESS};border-radius:50%;margin-right:5px;'></span>
            TURBO Online
        </div>
    </div>
    <div style='border-top:1px solid rgba(255,255,255,0.08);margin:0 8px 12px;'></div>
    """, unsafe_allow_html=True)

    for icon, name in PAGES:
        is_active = st.session_state.page == name
        if is_active:
            st.markdown(f"""
            <div style='background:linear-gradient(135deg,rgba(69,137,245,.3),rgba(6,182,212,.2));
                        border-left:3px solid {BLUE};border-radius:0 10px 10px 0;
                        padding:10px 16px;margin-bottom:3px;font-size:14px;
                        font-weight:700;color:white;'>
                {icon}  {name}
            </div>
            """, unsafe_allow_html=True)
        else:
            if st.button(f"{icon}  {name}", key=f"nav_{name}"):
                st.session_state.page = name
                st.rerun()

    st.markdown("""
    <div style='border-top:1px solid rgba(255,255,255,0.08);margin:14px 8px 10px;'></div>
    <div style='font-size:11px;color:rgba(255,255,255,0.25);text-align:center;padding:6px 0;'>
        NAVIGO v1.0 · Campus Logistics
    </div>
    """, unsafe_allow_html=True)

# ── HELPERS ───────────────────────────────────────────────────────────────────
STATUS_BADGE   = {"Delivered":"badge-success","En Route":"badge-info","Pending":"badge-warning","Assigned":"badge-info","Cancelled":"badge-danger"}
PRIORITY_BADGE = {"Normal":"badge-success","Urgent":"badge-warning","Emergency":"badge-danger"}
NOTIF_COLORS   = {"success":SUCCESS,"info":BLUE,"warning":WARNING,"error":DANGER}
NOTIF_ICONS    = {"success":"✅","info":"ℹ️","warning":"⚠️","error":"🚨"}
LOCATIONS      = ["Hostel A","Hostel B","Library","Cafeteria","Academic Block","Medical Centre"]

def metric_card(label, value, delta="", color=BLUE):
    delta_html = f"<div style='font-size:12px;color:#64748b;margin-top:3px;'>{delta}</div>" if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div style='font-size:32px;font-weight:900;color:{color};line-height:1.1;'>{value}</div>
        <div style='font-size:13px;color:#64748b;font-weight:600;margin-top:6px;'>{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

def notif_card(n):
    color = NOTIF_COLORS.get(n["type"], BLUE)
    icon  = NOTIF_ICONS.get(n["type"], "ℹ️")
    st.markdown(f"""
    <div class="notif-card" style="border-left-color:{color};">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
            <strong style="font-size:14px;color:#1e293b;">{icon} {n['title']}</strong>
            <span style="font-size:12px;color:#94a3b8;">{n['time']}</span>
        </div>
        <div style="font-size:13px;color:#475569;">{n['body']}</div>
    </div>
    """, unsafe_allow_html=True)

def request_card(req):
    b_s = STATUS_BADGE.get(req["status"],"badge-info")
    b_p = PRIORITY_BADGE.get(req["priority"],"badge-success")
    st.markdown(f"""
    <div class="notif-card" style="border-left-color:{BLUE};">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
            <div>
                <strong style="font-size:15px;color:{NAVY};">{req['id']}</strong>
                <span style="color:#64748b;font-size:13px;margin-left:10px;">{req['name']} · {req['category']}</span>
            </div>
            <div style="display:flex;gap:8px;">
                <span class="{b_p}">{req['priority']}</span>
                <span class="{b_s}">{req['status']}</span>
            </div>
        </div>
        <div style="font-size:13px;color:#475569;margin-top:6px;">
            📌 {req['pickup']} &nbsp;→&nbsp; 🏁 {req['dropoff']} &nbsp;·&nbsp; 🕐 {req['ts']}
        </div>
    </div>
    """, unsafe_allow_html=True)

def new_id():
    return f"NAV-{random.randint(1030,9999)}"

# ── PAGE: HOME ────────────────────────────────────────────────────────────────
def page_home():
    # Hero
    st.markdown(f"""
    <div class="hero-card">
        <div style='font-size:11px;letter-spacing:4px;color:{TEAL};font-weight:800;margin-bottom:10px;'>
            NAVIGO · AUTONOMOUS DELIVERY
        </div>
        <h1 style='color:white;margin:0 0 12px;font-size:2.8rem;font-weight:900;line-height:1.15;'>
            Meet <span style='color:{TEAL};'>TURBO</span> 🚚
        </h1>
        <p style='color:rgba(255,255,255,0.75);font-size:16px;margin-bottom:24px;max-width:580px;line-height:1.65;'>
            Your Autonomous Campus Delivery Companion — faster, smarter, and fully trackable.
            Zero waiting. Zero hassle. Pure efficiency.
        </p>
        <div style='display:flex;gap:12px;flex-wrap:wrap;'>
            <div style='background:rgba(34,197,94,.2);border:1px solid rgba(34,197,94,.4);
                        border-radius:24px;padding:8px 18px;font-size:13px;color:{SUCCESS};font-weight:600;'>
                ● TURBO Online
            </div>
            <div style='background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,.2);
                        border-radius:24px;padding:8px 18px;font-size:13px;color:white;'>
                ⚡ Avg Delivery: 8 min
            </div>
            <div style='background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,.2);
                        border-radius:24px;padding:8px 18px;font-size:13px;color:white;'>
                🏆 284 Deliveries Completed
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Active Deliveries","3","↑ 1 from yesterday")
    with c2: metric_card("Total Completed","284","All time",color=SUCCESS)
    with c3: metric_card("Avg Delivery Time","8 min","↓ 1 min this week",color=WARNING)
    with c4: metric_card("TURBO Units","4","3 active · 1 charging",color=PURPLE)

    st.markdown("<br>", unsafe_allow_html=True)

    # Core features strip
    st.markdown(f"<h3 style='color:{NAVY};margin-bottom:16px;'>🚀 Core Features</h3>", unsafe_allow_html=True)
    fc1,fc2,fc3,fc4 = st.columns(4)
    feats = [
        ("📍","Geo Tracking",       BLUE,  "Real-time live map of TURBO's exact position on campus."),
        ("🔒","End-to-End Security",TEAL,  "Lockable compartment + live camera. Your item, protected."),
        ("🔔","Smart Notifications",WARNING,"Instant alerts for every delivery milestone automatically."),
        ("🛠","Fleet Maintenance",  PURPLE,"Health dashboard, battery status and issue reporting."),
    ]
    for col,(icon,title,color,desc) in zip([fc1,fc2,fc3,fc4],feats):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:left;padding:20px;border-top:4px solid {color};">
                <div style='font-size:28px;margin-bottom:10px;'>{icon}</div>
                <div style='font-weight:800;font-size:15px;color:{NAVY};margin-bottom:6px;'>{title}</div>
                <div style='font-size:12px;color:#64748b;line-height:1.55;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # How NAVIGO Works — horizontal cards
    st.markdown(f"<h3 style='color:{NAVY};margin-bottom:18px;'>📦 How NAVIGO Works</h3>", unsafe_allow_html=True)
    steps = [
        ("1","🖊️","Place Request",  BLUE,  "Submit via the app in seconds — pick item, location and priority level."),
        ("2","🤖","TURBO Assigned", TEAL,  "The nearest available TURBO unit is dispatched to your pickup point."),
        ("3","📍","Live Tracking",  PURPLE,"Follow TURBO's journey on the live campus map in real-time."),
        ("4","📦","Delivered",      SUCCESS,"Package reaches your door. Rate your experience and help us improve!"),
    ]
    s1,s2,s3,s4 = st.columns(4)
    for col,(num,icon,title,color,desc) in zip([s1,s2,s3,s4],steps):
        with col:
            st.markdown(f"""
            <div class="step-card">
                <div style='width:44px;height:44px;background:linear-gradient(135deg,{color},{color}99);
                            border-radius:50%;display:flex;align-items:center;justify-content:center;
                            font-size:20px;margin:0 auto 14px;box-shadow:0 4px 12px {color}44;'>
                    {icon}
                </div>
                <div style='background:{color}18;color:{color};border-radius:20px;
                            padding:3px 12px;font-size:11px;font-weight:800;
                            display:inline-block;margin-bottom:10px;'>STEP {num}</div>
                <div style='font-weight:800;font-size:15px;color:{NAVY};margin-bottom:8px;'>{title}</div>
                <div style='font-size:13px;color:#64748b;line-height:1.6;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # Designed for
    st.markdown(f"<h3 style='color:{NAVY};margin-bottom:14px;'>🌍 Designed For</h3>", unsafe_allow_html=True)
    venues = [("🏫","Universities"),("🏘️","Gated Communities"),("🏢","Corporate Parks"),("🌳","Smart Public Spaces")]
    v1,v2,v3,v4 = st.columns(4)
    for col,(icon,label) in zip([v1,v2,v3,v4],venues):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="padding:18px;">
                <div style='font-size:28px;margin-bottom:8px;'>{icon}</div>
                <div style='font-size:13px;font-weight:700;color:{NAVY};'>{label}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📦  Request a Delivery Now →", key="home_cta"):
        st.session_state.page = "Request Delivery"
        st.rerun()

# ── PAGE: REQUEST DELIVERY ────────────────────────────────────────────────────
def page_request():
    st.markdown(f"<h2 style='color:{NAVY};font-weight:900;'>📦 Request Delivery</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;font-size:15px;margin-bottom:20px;'>Fill in the details below and TURBO will be dispatched to you instantly.</p>", unsafe_allow_html=True)

    with st.form("delivery_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name     = st.text_input("👤 Your Name",        placeholder="e.g. Arjun Sharma")
            contact  = st.text_input("📱 Contact Number",   placeholder="e.g. 9876543210")
        with c2:
            category = st.selectbox("📦 Item Category",["Food","Medicines","Parcel","Documents"])
            priority = st.selectbox("🚦 Priority Level",["Normal","Urgent","Emergency"])
        c3, c4 = st.columns(2)
        with c3:
            pickup  = st.selectbox("📌 Pickup Location",   LOCATIONS)
        with c4:
            dropoff = st.selectbox("🏁 Delivery Location", LOCATIONS)
        notes = st.text_area("📝 Special Instructions (optional)",
                             placeholder="e.g. Fragile item, leave at door…", height=80)
        submitted = st.form_submit_button("🤖 Assign TURBO & Track Live", use_container_width=True)

    if submitted:
        if not name.strip() or not contact.strip():
            st.error("⚠️ Please enter your name and contact number.")
        elif pickup == dropoff:
            st.warning("⚠️ Pickup and delivery location cannot be the same.")
        else:
            nid = new_id()
            now_ts = datetime.datetime.now().strftime("%I:%M %p")
            delivery = {
                "id": nid, "name": name.strip(), "category": category,
                "pickup": pickup, "dropoff": dropoff,
                "priority": priority, "status": "En Route", "ts": now_ts,
            }
            st.session_state.requests.insert(0, delivery)
            st.session_state.active_delivery = delivery
            st.session_state.notifications.insert(0, {
                "type":"info","title":f"TURBO Assigned — {nid}",
                "body":f"TURBO heading from {pickup} to {dropoff}.",
                "time":"Just now",
            })
            # Reset tracking to step 2 (En Route) for the new delivery
            st.session_state.tracking_step = 2
            st.session_state.tracking_eta  = 480
            st.success(f"✅ TURBO assigned! Redirecting to Live Tracking…")
            st.session_state.page = "Live Tracking"
            st.rerun()

    # Recent requests (only 4 seed ones)
    st.markdown(f"<h3 style='color:{NAVY};margin-top:20px;'>📋 Recent Delivery Requests</h3>", unsafe_allow_html=True)
    for req in st.session_state.requests[:4]:
        request_card(req)

# ── PAGE: LIVE TRACKING ───────────────────────────────────────────────────────
TRACK_STEPS = ["Request Received","TURBO Assigned","En Route","Near Destination","Delivered"]
 
BUILDINGS = {
    "🏠 Hostel A":       (0.10, 0.88),
    "🍽 Cafeteria":      (0.35, 0.68),
    "🏫 Academic Block": (0.58, 0.46),
    "📚 Library":        (0.82, 0.16),
    "🏥 Medical Centre": (0.18, 0.46),
    "🏠 Hostel B":       (0.78, 0.80),
    "⚡ Base Station":   (0.50, 0.92),
}
WP_X = [0.10,0.18,0.35,0.50,0.58,0.70,0.82]
WP_Y = [0.88,0.78,0.68,0.58,0.46,0.30,0.16]
 
def turbo_pos(step):
    total = len(TRACK_STEPS) - 1
    frac  = min(step / total, 1.0)
    seg   = min(int(frac * (len(WP_X)-1)), len(WP_X)-2)
    t     = (frac * (len(WP_X)-1)) - seg
    x = WP_X[seg] + t*(WP_X[seg+1]-WP_X[seg])
    y = WP_Y[seg] + t*(WP_Y[seg+1]-WP_Y[seg])
    return x, y
 
def page_tracking():
    st.markdown(f"<h2 style='color:{NAVY};font-weight:900;'>📍 Live Tracking</h2>", unsafe_allow_html=True)
 
    active  = st.session_state.tracking_step
    eta_sec = st.session_state.tracking_eta
    mins, secs = divmod(eta_sec, 60)
 
    # ── ETA + Progress ────────────────────────────────
    col_eta, col_prog = st.columns([1, 2])
 
    with col_eta:
        step_label = TRACK_STEPS[active] if active < len(TRACK_STEPS) else "Delivered"
        st.markdown(f"""
        <div class="metric-card" style="padding:28px 20px;border-top:4px solid {TEAL};">
            <div style="font-size:10px;color:#94a3b8;font-weight:800;letter-spacing:2px;margin-bottom:12px;">
                ESTIMATED ARRIVAL
            </div>
            <div style="font-size:52px;font-weight:900;color:{NAVY};letter-spacing:4px;line-height:1;font-family:monospace;">
                {mins:02d}:{secs:02d}
            </div>
            <div style="margin-top:16px;padding:8px 14px;background:{TEAL}18;border-radius:12px;">
                <span class="pulse" style="display:inline-block;width:8px;height:8px;
                background:{SUCCESS};border-radius:50%;margin-right:6px;"></span>
                <span style="font-size:13px;color:{NAVY};font-weight:700;">{step_label}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
    with col_prog:
        st.markdown(f"""
        <div class="card">
            <div style="font-weight:800;font-size:16px;color:{NAVY};margin-bottom:16px;">
                📦 Delivery Progress
            </div>
        """, unsafe_allow_html=True)
        for i, step in enumerate(TRACK_STEPS):
            if i < active:
                icon, color, fw, bg = "✅", SUCCESS, "600", f"{SUCCESS}12"
            elif i == active:
                icon, color, fw, bg = "🔵", BLUE, "800", f"{BLUE}18"
            else:
                icon, color, fw, bg = "⚪", "#94a3b8", "400", "transparent"
            current = "<span style='margin-left:auto;font-size:11px;color:#64748b;font-weight:600;'>CURRENT</span>" if i==active else ""
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;
                        padding:10px 14px;background:{bg};border-radius:10px;">
                <span style="font-size:18px;">{icon}</span>
                <span style="color:{color};font-weight:{fw};font-size:14px;">{step}</span>
                {current}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
 
    st.markdown("<br>", unsafe_allow_html=True)
 
    # ── Google-Maps-style campus map ─────────────────
    st.markdown(f"<h3 style='color:{NAVY};'>🗺️ Campus Map — Live TURBO Location</h3>", unsafe_allow_html=True)
 
    tx, ty = turbo_pos(active)
    st.write("Turbo:", tx, ty)
 
    # Road grid lines for visual depth
    road_shapes = []
    for v in [0.25, 0.50, 0.75]:
        road_shapes.append(dict(type="line",x0=v,y0=0,x1=v,y1=1,
            line=dict(color="#9ca3af",width=28)))
        road_shapes.append(dict(type="line",x0=0,y0=v,x1=1,y1=v,
            line=dict(color="#9ca3af",width=28)))
 
    # Campus boundary
    road_shapes.append(dict(type="rect",x0=0,y0=0,x1=1,y1=1,
        line=dict(color="#c8d4e0",width=2),fillcolor="rgba(0,0,0,0)"))
 
    # Green areas
    green_shapes = [
        dict(type="rect",x0=0.60,y0=0.55,x1=0.78,y1=0.72,
             line=dict(color="#86efac",width=0),fillcolor="rgba(220,252,231,0.53)"),
        dict(type="rect",x0=0.02,y0=0.02,x1=0.14,y1=0.30,
             line=dict(color="#86efac",width=0),fillcolor="rgba(220,252,231,0.53)"),
    ]
 
    fig = go.Figure()
 
    # Background fill
    fig.add_shape(type="rect",x0=-0.02,y0=-0.02,x1=1.02,y1=1.02,
                  fillcolor="#f0f4e8",line=dict(color="#d4ddc8",width=1))
 
    # Roads
    for s in road_shapes:
        fig.add_shape(**s)
    for s in green_shapes:
        fig.add_shape(**s)
 
    # Route dashed line
    fig.add_trace(go.Scatter(
        x=WP_X, y=WP_Y, mode="lines",
        line=dict(
            color="#ff0000",
            width=18,
            dash="solid"
        ),
        name="Route", hoverinfo="skip",
    ))
 
    # Completed route (solid, highlighted)
    seg   = min(int((min(active/(len(TRACK_STEPS)-1),1.0))*(len(WP_X)-1)), len(WP_X)-2)
    t_frc = (min(active/(len(TRACK_STEPS)-1),1.0)*(len(WP_X)-1)) - seg
    cx    = WP_X[seg] + t_frc*(WP_X[seg+1]-WP_X[seg])
    cy    = WP_Y[seg] + t_frc*(WP_Y[seg+1]-WP_Y[seg])
    fig.add_trace(go.Scatter(
        x=WP_X[:seg+1]+[cx], y=WP_Y[:seg+1]+[cy],
        mode="lines",
        line=dict(color="#22c55e",width=12),
        name="Done", hoverinfo="skip",
    ))

    fig.add_trace(
        go.Scatter(
            x=WP_X,
            y=WP_Y,
            mode="lines",
            line=dict(
                color="#22c55e",
                width=6
            ),
            showlegend=False,
            hoverinfo="skip"
    )
)

    # Building markers

    building_icons = {
        "Hostel A":"🏠",
        "Hostel B":"🏠",
        "Cafeteria":"🍽",
        "Academic Block":"🏫",
        "Library":"📚",
        "Medical Centre":"🏥",
        "Base Station":"⚡",
    }

    for bname,(bx,by) in BUILDINGS.items():

        fig.add_trace(
            go.Scatter(
                x=[bx],
                y=[by],
                mode="markers+text",
                marker=dict(
                    size=45,
                    color="white",
                    line=dict(color="#2563eb", width=3)
                ),
                text=[building_icons.get(bname,"📍")],
                textposition="middle center",
                textfont=dict(size=28),
                showlegend=False,
                hovertemplate=f"<b>{bname}</b><extra></extra>"
            )
        )

        fig.add_annotation(
            x=bx,
            y=by-0.05,
            text=bname,
            showarrow=False,
            font=dict(size=12,color="#0f172a"
            )
        )
    # TURBO marker

    fig.add_trace(
        go.Scatter(
            x=[tx],
            y=[ty],
            mode="markers+text",
            marker=dict(
                size=30,
                color="#ef4444",
                line=dict(color="white",width=3)
            ),
            text=["🚚"],
            textposition="middle center",
            textfont=dict(size=20),
            showlegend=False,
            hovertemplate="<b>TURBO</b><extra></extra>"
        )
    )
 
    fig.update_layout(
        height=450,
        margin=dict(l=0,r=0,t=10,b=10),
        plot_bgcolor="#f0f4e8",
        paper_bgcolor="white",
        showlegend=False,
        xaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-0.04,1.04]),
        yaxis=dict(showgrid=False,zeroline=False,showticklabels=False,range=[-0.04,1.04]),
        hoverlabel=dict(bgcolor="white",font_size=13,font_color=NAVY),
    )
    
    st.write("Traces:", len(fig.data))
    st.plotly_chart(fig, use_container_width=True)
 
    # Controls
    b1, b2, _ = st.columns([1,1,4])
    with b1:
        if st.button("⏩ Advance Step"):
            st.session_state.tracking_step = (active+1) % len(TRACK_STEPS)
            st.session_state.tracking_eta  = max(0, eta_sec-120)
            st.rerun()
    with b2:
        if st.button("🔄 Reset"):
            st.session_state.tracking_step = 0
            st.session_state.tracking_eta  = 600
            st.rerun()
 
    # ── Active Delivery Details ──────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
 
    # Prefer user's own submitted delivery; fallback to any En Route
    active_req = st.session_state.get("active_delivery") or \
                 next((r for r in st.session_state.requests if r["status"]=="En Route"), None)

    if active_req:
       st.success(
        f"🚚 TURBO is currently travelling from {active_req['pickup']} to {active_req['dropoff']}"
       ) 

    if active_req:
        st.markdown(f"""
        <div class="card" style="border-top:4px solid {BLUE};">
            <div style="font-weight:800;font-size:17px;color:{NAVY};margin-bottom:18px;">
                📦 Active Delivery Details
            </div>
            <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:16px;">
                <div style="background:{BLUE}12;border-radius:12px;padding:14px;">
                    <div style="font-size:11px;color:#64748b;font-weight:700;letter-spacing:.5px;margin-bottom:4px;">DELIVERY ID</div>
                    <div style="font-size:16px;font-weight:900;color:{BLUE};">{active_req['id']}</div>
                </div>
                <div style="background:{TEAL}12;border-radius:12px;padding:14px;">
                    <div style="font-size:11px;color:#64748b;font-weight:700;letter-spacing:.5px;margin-bottom:4px;">CUSTOMER</div>
                    <div style="font-size:16px;font-weight:900;color:{NAVY};">{active_req['name']}</div>
                </div>
                <div style="background:{WARNING}12;border-radius:12px;padding:14px;">
                    <div style="font-size:11px;color:#64748b;font-weight:700;letter-spacing:.5px;margin-bottom:4px;">ITEM</div>
                    <div style="font-size:16px;font-weight:900;color:{NAVY};">{active_req['category']}</div>
                </div>
                <div style="background:{PURPLE}12;border-radius:12px;padding:14px;">
                    <div style="font-size:11px;color:#64748b;font-weight:700;letter-spacing:.5px;margin-bottom:4px;">PRIORITY</div>
                    <div style="font-size:16px;font-weight:900;color:{PURPLE};">{active_req['priority']}</div>
                </div>
            </div>
            <div style="margin-top:16px;padding:12px 16px;background:#f8faff;border-radius:12px;
                        font-size:14px;color:{NAVY};font-weight:600;">
                📌 {active_req['pickup']} &nbsp;→&nbsp; 🏁 {active_req['dropoff']}
                &nbsp;&nbsp;|&nbsp;&nbsp; 🕐 {active_req['ts']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No active delivery at the moment. Place a request to begin.")

# ── PAGE: NOTIFICATIONS ───────────────────────────────────────────────────────
def page_notifications():
    st.markdown(f"<h2 style='color:{NAVY};font-weight:900;'>🔔 Notifications</h2>", unsafe_allow_html=True)
    t_all,t_ok,t_warn,t_err = st.tabs(["All","✅ Success","⚠️ Warnings","🚨 Alerts"])
    def render(items):
        if items:
            for n in items: notif_card(n)
        else:
            st.info("No notifications here.")
    with t_all:  render(st.session_state.notifications)
    with t_ok:   render([n for n in st.session_state.notifications if n["type"]=="success"])
    with t_warn: render([n for n in st.session_state.notifications if n["type"]=="warning"])
    with t_err:  render([n for n in st.session_state.notifications if n["type"]=="error"])
    st.divider()
    if st.button("🗑️ Clear All Notifications"):
        st.session_state.notifications = []
        st.rerun()

# ── PAGE: HELPDESK ────────────────────────────────────────────────────────────
BOT = {
    "where":  "TURBO is near the Academic Block and will reach you in ~3 minutes.",
    "cancel": "Cancellations are only possible within 2 minutes of placing a request.",
    "time":   "Average campus delivery time is 8–12 minutes. Peak hours may add 3–5 min.",
    "track":  "Open 📍 Live Tracking in the sidebar to follow TURBO in real-time.",
    "help":   "I can help with tracking, cancellations, delivery times, and general queries.",
    "default":"Your concern has been escalated. A human agent will respond shortly.",
}
FAQS = [
    ("Where is my delivery?","TURBO is en route — open Live Tracking for the real-time map."),
    ("How do I cancel?","Contact support within 2 minutes of placing the request."),
    ("How long does delivery take?","8–12 minutes on average. Peak hours may add a few minutes."),
    ("What can TURBO carry?","Up to 5 kg — food, medicines, documents, parcels."),
    ("What are TURBO's hours?","7:00 AM – 10:00 PM daily, including weekends."),
    ("Is my item safe?","Yes! Lockable compartment and live camera monitoring."),
]

def bot_reply(text):
    t = text.lower()
    if any(w in t for w in ["where","location","find"]): return BOT["where"]
    if "cancel" in t: return BOT["cancel"]
    if any(w in t for w in ["time","long","minute"]):    return BOT["time"]
    if "track" in t:  return BOT["track"]
    if "help"  in t:  return BOT["help"]
    return BOT["default"]

def page_helpdesk():
    st.markdown(f"<h2 style='color:{NAVY};font-weight:900;'>💬 Helpdesk & Support</h2>", unsafe_allow_html=True)
    t_chat, t_faq = st.tabs(["💬 Live Chat","❓ FAQs"])
    with t_chat:
        st.markdown("<p style='color:#64748b;'>Chat with the NAVIGO support assistant.</p>", unsafe_allow_html=True)
        for msg in st.session_state.chat_messages:
            with st.chat_message(msg["role"], avatar="🤖" if msg["role"]=="assistant" else "👤"):
                st.markdown(msg["text"])
        user_input = st.chat_input("Type your message…")
        if user_input:
            st.session_state.chat_messages.append({"role":"user","text":user_input})
            st.session_state.chat_messages.append({"role":"assistant","text":bot_reply(user_input)})
            st.rerun()
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_messages = [{"role":"assistant","text":"Hello! I'm the NAVIGO support bot. How can I help you today?"}]
            st.rerun()
    with t_faq:
        st.markdown(f"<h3 style='color:{NAVY};'>Frequently Asked Questions</h3>", unsafe_allow_html=True)
        for q,a in FAQS:
            with st.expander(q):
                st.markdown(f"<p style='color:#475569;font-size:14px;'>{a}</p>", unsafe_allow_html=True)

# ── PAGE: FEEDBACK ────────────────────────────────────────────────────────────
SAMPLE_REVIEWS = [
    ("★★★★★","Fast delivery and accurate tracking. Absolutely loved it!","Rohan M.",SUCCESS),
    ("★★★★★","TURBO arrived exactly on time. Packaging was perfect.","Priya K.",BLUE),
    ("★★★★☆","Smooth experience and super easy to use. Will use again!","Ananya S.",TEAL),
]

def page_feedback():
    st.markdown(f"<h2 style='color:{NAVY};font-weight:900;'>⭐ Feedback</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748b;font-size:15px;'>Help us improve NAVIGO and TURBO by sharing your experience.</p>", unsafe_allow_html=True)
    st.divider()

    with st.form("feedback_form", clear_on_submit=True):
        delivery_id = st.text_input("📦 Delivery ID (optional)", placeholder="e.g. NAV-1029")
        rating = st.select_slider("⭐ Overall Rating", options=[1,2,3,4,5], value=5,
                                  format_func=lambda x: "⭐"*x)
        categories = st.multiselect("👍 What went well?",
            ["Speed","Punctuality","Packaging","TURBO behaviour","App experience","Customer service"])
        comment   = st.text_area("💬 Your Comments", placeholder="Tell us about your experience…", height=100)
        recommend = st.radio("Would you recommend NAVIGO?",["Yes, definitely!","Maybe","No"], horizontal=True)
        submitted = st.form_submit_button("📨 Submit Feedback", use_container_width=True)

    if submitted:
        entry = {
            "id": delivery_id.strip() or "—",
            "rating": rating, "categories": categories,
            "comment": comment.strip(), "recommend": recommend,
            "ts": datetime.datetime.now().strftime("%b %d, %I:%M %p"),
        }
        st.session_state.feedback_list.insert(0, entry)
        st.success("Thank you for your feedback! 🙏 We'll keep improving TURBO for you.")
        st.balloons()

    # Sample reviews
    st.markdown(f"<h3 style='color:{NAVY};margin-top:20px;'>🌟 What People Are Saying</h3>", unsafe_allow_html=True)
    for stars,text,author,color in SAMPLE_REVIEWS:
        st.markdown(f"""
        <div class="notif-card" style="border-left-color:{color};">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <span style="font-size:16px;color:{WARNING};">{stars}</span>
                <span style="font-size:13px;color:{NAVY};font-weight:700;">{author}</span>
            </div>
            <div style="font-size:14px;color:#334155;">{text}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.session_state.feedback_list:
        st.markdown(f"<h3 style='color:{NAVY};'>📋 Your Submitted Feedback</h3>", unsafe_allow_html=True)
        for fb in st.session_state.feedback_list:
            stars = "⭐"*fb["rating"]
            cats  = ", ".join(fb["categories"]) if fb["categories"] else "—"
            st.markdown(f"""
            <div class="notif-card" style="border-left-color:{BLUE};">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;flex-wrap:wrap;gap:6px;">
                    <strong style="color:{NAVY};">{fb['id']}</strong>
                    <span style="font-size:16px;">{stars}</span>
                    <span style="font-size:12px;color:#94a3b8;">{fb['ts']}</span>
                </div>
                <div style="font-size:13px;color:#64748b;margin-bottom:5px;">👍 {cats}</div>
                <div style="font-size:14px;color:#334155;">{fb['comment'] or '<em style="color:#94a3b8;">No comment provided</em>'}</div>
                <div style="font-size:12px;color:#94a3b8;margin-top:5px;">Recommend: {fb['recommend']}</div>
            </div>
            """, unsafe_allow_html=True)

# ── PAGE: MAINTENANCE ─────────────────────────────────────────────────────────
TURBO_UNITS = [
    {"id":"TURBO #1","battery":87,"status":"Active",  "location":"Hostel A",    "deliveries":12},
    {"id":"TURBO #2","battery":62,"status":"Active",  "location":"Library",     "deliveries":9},
    {"id":"TURBO #3","battery":95,"status":"Active",  "location":"Cafeteria",   "deliveries":15},
    {"id":"TURBO #4","battery":15,"status":"Charging","location":"Base Station","deliveries":6},
]

def bat_color(p):
    return SUCCESS if p>50 else (WARNING if p>20 else DANGER)

def page_maintenance():
    st.markdown(f"<h2 style='color:{NAVY};font-weight:900;'>🔧 Maintenance</h2>", unsafe_allow_html=True)
    t_fleet, t_report = st.tabs(["🤖 TURBO Fleet","📝 Report Issue"])

    with t_fleet:
        st.markdown(f"<h3 style='color:{NAVY};'>Fleet Overview</h3>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i,unit in enumerate(TURBO_UNITS):
            bat=unit["battery"]; bc=bat_color(bat)
            s_cls="badge-success" if unit["status"]=="Active" else "badge-warning"
            with cols[i%2]:
                st.markdown(f"""
                <div class="card" style="border-top:4px solid {bc};">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
                        <strong style="font-size:16px;color:{NAVY};">🤖 {unit['id']}</strong>
                        <span class="{s_cls}">{unit['status']}</span>
                    </div>
                    <div style="display:flex;gap:20px;font-size:13px;color:#64748b;margin-bottom:12px;">
                        <span>📌 {unit['location']}</span>
                        <span>📦 {unit['deliveries']} deliveries today</span>
                    </div>
                    <div style="font-size:13px;font-weight:700;margin-bottom:6px;color:{NAVY};">
                        Battery: <span style="color:{bc};">{bat}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(bat/100)
                st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"<h3 style='color:{NAVY};'>❤️ System Health</h3>", unsafe_allow_html=True)
        health = [("Battery Health",0.94),("GPS Accuracy",0.97),("Sensors",0.91),("Connectivity",0.88)]
        for label,val in health:
            pct=int(val*100); bc2=SUCCESS if val>=.90 else (WARNING if val>=.75 else DANGER)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:13px;font-weight:700;margin-bottom:4px;">
                <span style="color:{NAVY};">{label}</span>
                <span style="color:{bc2};">{pct}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(val)

        st.markdown(f"<h3 style='color:{NAVY};margin-top:16px;'>📊 System Metrics</h3>", unsafe_allow_html=True)
        m1,m2,m3,m4 = st.columns(4)
        with m1: metric_card("Uptime","99.2%","Last 30 days",color=SUCCESS)
        with m2: metric_card("Avg Temp","42 °C","Normal range")
        with m3: metric_card("Obstacle Avoids","34","This week")
        with m4: metric_card("Maintenance Due","TURBO #4","Battery swap",color=WARNING)

    with t_report:
        st.markdown(f"<h3 style='color:{NAVY};'>Report an Issue</h3>", unsafe_allow_html=True)
        with st.form("maintenance_form", clear_on_submit=True):
            c1,c2 = st.columns(2)
            with c1:
                unit_sel   = st.selectbox("🤖 TURBO Unit",[u["id"] for u in TURBO_UNITS])
                issue_type = st.selectbox("⚠️ Issue Type",["Battery Problem","Sensor Issue","Navigation Error","Mechanical Failure","Software Glitch","Other"])
            with c2:
                severity    = st.selectbox("🚦 Severity",["Low","Medium","High","Critical"])
                reported_by = st.text_input("👤 Reported By",placeholder="Your name")
            desc = st.text_area("📝 Description",placeholder="Describe the issue in detail…",height=100)
            sub  = st.form_submit_button("📨 Submit Report",use_container_width=True)
        if sub:
            if not reported_by.strip():
                st.warning("Please enter your name before submitting.")
            else:
                nid = f"MNT-{random.randint(100,999)}"
                st.session_state.maintenance_reports.insert(0,{
                    "id":nid,"issue":issue_type,
                    "desc":desc.strip() or "No description provided.",
                    "status":"Open","reported":datetime.datetime.now().strftime("%b %d"),
                })
                st.session_state.notifications.insert(0,{
                    "type":"warning","title":f"Maintenance Report {nid}",
                    "body":f"{unit_sel}: {issue_type} — {severity} severity.",
                    "time":"Just now",
                })
                st.success(f"Ticket **{nid}** created. Maintenance team notified!")

        st.markdown(f"<h3 style='color:{NAVY};margin-top:12px;'>📋 Maintenance Log</h3>", unsafe_allow_html=True)
        SCLS = {"In Progress":"badge-warning","Resolved":"badge-success","Open":"badge-danger"}
        for r in st.session_state.maintenance_reports:
            sc = SCLS.get(r["status"],"badge-info")
            st.markdown(f"""
            <div class="notif-card" style="border-left-color:{WARNING};">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                    <strong style="color:{NAVY};">{r['id']} — {r['issue']}</strong>
                    <span class="{sc}">{r['status']}</span>
                </div>
                <div style="font-size:13px;color:#475569;">{r['desc']}</div>
                <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Reported: {r['reported']}</div>
            </div>
            """, unsafe_allow_html=True)

# ── PAGE: COMMUNITY DASHBOARD ─────────────────────────────────────────────────
def page_dashboard():
    st.markdown(f"<h2 style='color:{NAVY};font-weight:900;'>📊 Community Dashboard</h2>", unsafe_allow_html=True)

    # KPIs
    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: metric_card("Total Requests","284","All time")
    with k2: metric_card("Active Now","3","Live",color=TEAL)
    with k3: metric_card("Completed Today","47","↑ 12 vs yesterday",color=SUCCESS)
    with k4: metric_card("Avg Delivery","8.2 min","↓ 0.8 min",color=WARNING)
    with k5: metric_card("Success Rate","98.6%","Last 7 days",color=PURPLE)

    st.markdown("<br>", unsafe_allow_html=True)

    # Action buttons
    ab1,ab2,ab3 = st.columns(3)
    with ab1:
        if st.button("🚨 Emergency Stop",use_container_width=True):
            st.error("⛔ Emergency stop sent to all TURBO units!")
    with ab2:
        if st.button("⏸ Pause All TURBO",use_container_width=True):
            st.warning("⏸ All TURBO units paused.")
    with ab3:
        if st.button("📄 Generate Report",use_container_width=True):
            st.success("📄 Report generation started!")

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([3,2])

    with col_l:
        # Bar chart
        days=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        vals=[38,52,45,61,47,29,12]
        bar_colors=[PURPLE if d=="Thu" else BLUE for d in days]
        fig_vol=go.Figure(go.Bar(
            x=days,y=vals,marker_color=bar_colors,
            text=vals,textposition="outside",
            textfont=dict(size=12,color=NAVY),
        ))
        fig_vol.update_layout(
            title=dict(text="Daily Delivery Volume",font=dict(size=15,color=NAVY,family="Arial Black")),
            plot_bgcolor="white",paper_bgcolor="white",
            yaxis=dict(showgrid=True,gridcolor="#f1f5f9",title="Deliveries",color="#64748b"),
            xaxis=dict(showgrid=False,color="#64748b"),
            margin=dict(l=0,r=0,t=48,b=20),height=260,
        )
        st.plotly_chart(fig_vol,use_container_width=True)

        # Donut
        cats=["Food","Parcel","Documents","Medicines"]
        counts=[35,28,22,15]
        fig_pie=go.Figure(go.Pie(
            labels=cats,values=counts,
            marker_colors=[BLUE,WARNING,SUCCESS,DANGER],
            hole=0.55,textinfo="label+percent",textfont_size=12,
            textfont_color=[NAVY]*4,
        ))
        fig_pie.update_layout(
            title=dict(text="Deliveries by Category",font=dict(size=15,color=NAVY,family="Arial Black")),
            paper_bgcolor="white",margin=dict(l=0,r=0,t=48,b=40),height=280,
            showlegend=True,
            legend=dict(orientation="h",yanchor="bottom",y=-0.25,xanchor="center",x=0.5,
                        font=dict(color=NAVY,size=12)),
        )
        st.plotly_chart(fig_pie,use_container_width=True)

    with col_r:
        # Area chart
        hours=list(range(7,23))
        hourly=[2,5,8,12,9,6,14,18,15,10,7,9,11,8,5,3]
        fig_hr=go.Figure(go.Scatter(
            x=hours,y=hourly,mode="lines+markers",
            line=dict(color=TEAL,width=2.5),
            marker=dict(size=6,color=TEAL),
            fill="tozeroy",fillcolor="rgba(6,182,212,0.12)",
        ))
        fig_hr.update_layout(
            title=dict(text="Hourly Requests (Today)",font=dict(size=15,color=NAVY,family="Arial Black")),
            plot_bgcolor="white",paper_bgcolor="white",
            yaxis=dict(showgrid=True,gridcolor="#f1f5f9",color="#64748b"),
            xaxis=dict(tickvals=hours,ticktext=[f"{h}:00" for h in hours],
                       showgrid=False,tickangle=-45,color="#64748b"),
            margin=dict(l=0,r=0,t=48,b=60),height=240,
        )
        st.plotly_chart(fig_hr,use_container_width=True)

        st.markdown(f"<h4 style='color:{NAVY};'>📍 Top Delivery Locations</h4>", unsafe_allow_html=True)
        locs=[("Library",61,BLUE),("Hostel A",48,SUCCESS),
              ("Cafeteria",39,WARNING),("Academic Block",31,PURPLE),("Medical Centre",18,DANGER)]
        for loc,pct,c in locs:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;
                        font-size:13px;font-weight:700;margin-bottom:4px;margin-top:8px;">
                <span style="color:{NAVY};">{loc}</span>
                <span style="color:{c};">{pct}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(pct/100)

    # Delivery table
    st.markdown(f"<h3 style='color:{NAVY};margin-top:20px;'>📋 Recent Delivery Records</h3>", unsafe_allow_html=True)
    all_reqs = st.session_state.requests[:8]

    if not all_reqs:
        st.info("No delivery records yet.")
    else:
        hs = f"background:{NAVY};color:white;padding:12px 14px;font-size:13px;font-weight:700;text-align:left;"
        rs = "padding:11px 14px;font-size:13px;border-bottom:1px solid #f1f5f9;color:#334155;"
        rows = ""
        for req in all_reqs:
            bs = STATUS_BADGE.get(req["status"],"badge-info")
            bp = PRIORITY_BADGE.get(req["priority"],"badge-success")
            rows += f"""
            <tr style="background:white;">
                <td style="{rs}font-weight:800;color:{BLUE};">{req['id']}</td>
                <td style="{rs}font-weight:600;color:{NAVY};">{req['name']}</td>
                <td style="{rs}">{req['category']}</td>
                <td style="{rs}">{req['pickup']}</td>
                <td style="{rs}">{req['dropoff']}</td>
                <td style="{rs}"><span class="{bp}">{req['priority']}</span></td>
                <td style="{rs}"><span class="{bs}">{req['status']}</span></td>
                <td style="{rs}color:#64748b;">{req['ts']}</td>
            </tr>
            """
        st.markdown(f"""
        <div style="overflow-x:auto;border-radius:16px;box-shadow:0 4px 20px rgba(10,37,64,.09);margin-top:8px;">
        <table style="width:100%;border-collapse:collapse;background:white;border-radius:16px;overflow:hidden;">
            <thead>
                <tr>
                    <th style="{hs}">ID</th><th style="{hs}">Customer</th>
                    <th style="{hs}">Category</th><th style="{hs}">Pickup</th>
                    <th style="{hs}">Drop-off</th><th style="{hs}">Priority</th>
                    <th style="{hs}">Status</th><th style="{hs}">Time</th>
                </tr>
            </thead>
            <tbody>{rows}</tbody>
        </table>
        </div>
        """, unsafe_allow_html=True)

# ── ROUTER ────────────────────────────────────────────────────────────────────
PAGE_MAP = {
    "Home":                page_home,
    "Request Delivery":    page_request,
    "Live Tracking":       page_tracking,
    "Notifications":       page_notifications,
    "Helpdesk":            page_helpdesk,
    "Feedback":            page_feedback,
    "Maintenance":         page_maintenance,
    "Community Dashboard": page_dashboard,
}
PAGE_MAP[st.session_state.page]()