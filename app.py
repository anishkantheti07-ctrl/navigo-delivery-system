"""
NAVIGO — Smart Autonomous Campus Delivery Ecosystem
Streamlit prototype. All data is simulated/hardcoded.

Deploy locally or on GitHub Codespaces:
    pip install streamlit plotly
    streamlit run app.py

Streamlit Cloud:
    Push to GitHub → connect repo on share.streamlit.io
"""

import streamlit as st
import plotly.graph_objects as go
import datetime
import random

# ─────────────────────────────────────────────
# PAGE CONFIG  (must be FIRST Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="NAVIGO — Campus Delivery",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────
NAVY    = "#0a2540"
BLUE    = "#4589f5"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER  = "#ef4444"

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown(f"""
<style>
/* ── Body / background ── */
[data-testid="stAppViewContainer"] {{ background-color: #f0f4ff; }}
[data-testid="block-container"]    {{ padding-top: 1.5rem; padding-bottom: 2rem; }}

/* ── Sidebar ── */
[data-testid="stSidebar"]    {{ background-color: {NAVY} !important; }}
[data-testid="stSidebar"] *  {{ color: #e2e8f0 !important; }}
[data-testid="stSidebar"] .stButton > button {{
    width:100%; background:transparent; border:none;
    text-align:left; padding:10px 14px; border-radius:8px;
    color:#e2e8f0 !important; font-size:15px; transition:background .2s;
}}
[data-testid="stSidebar"] .stButton > button:hover {{
    background:rgba(255,255,255,0.1) !important;
}}

/* ── Cards ── */
.nav-card {{
    background:white; border-radius:16px; padding:22px 20px;
    box-shadow:0 2px 12px rgba(10,37,64,.08); margin-bottom:16px;
}}
.metric-card {{
    background:white; border-radius:14px; padding:20px 18px;
    box-shadow:0 2px 10px rgba(10,37,64,.07); text-align:center;
}}
.hero-card {{
    background:linear-gradient(135deg,{NAVY} 0%,#133e7c 100%);
    border-radius:24px; padding:28px 28px; color:white; margin-bottom:24px;
}}
.notif-card {{
    border-left:4px solid {BLUE}; background:white;
    border-radius:0 12px 12px 0; padding:14px 18px;
    margin-bottom:10px; box-shadow:0 1px 6px rgba(0,0,0,.05);
}}

/* ── Hover lifts ── */
.metric-card:hover, .nav-card:hover, .notif-card:hover {{
    transform:translateY(-3px); box-shadow:0 6px 20px rgba(10,37,64,.12);
    transition:all .25s ease;
}}

/* ── Badges ── */
.badge-success {{ background:{SUCCESS}22; color:{SUCCESS}; border-radius:8px; padding:3px 10px; font-size:12px; font-weight:700; }}
.badge-info    {{ background:{BLUE}22;    color:{BLUE};    border-radius:8px; padding:3px 10px; font-size:12px; font-weight:700; }}
.badge-warning {{ background:{WARNING}22; color:{WARNING}; border-radius:8px; padding:3px 10px; font-size:12px; font-weight:700; }}
.badge-danger  {{ background:{DANGER}22;  color:{DANGER};  border-radius:8px; padding:3px 10px; font-size:12px; font-weight:700; }}

/* ── Buttons ── */
.stButton > button {{
    background-color:{BLUE}; color:white; border:none;
    border-radius:10px; font-weight:600; padding:.45rem 1.4rem;
    transition:background .2s;
}}
.stButton > button:hover {{
    background-color:#2d6fd4 !important;
    color:white !important; border:none !important;
}}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea  > div > div > textarea,
.stSelectbox > div > div {{
    border-radius:10px !important;
    border:1.5px solid #d1d9e6 !important;
}}

/* ── Progress bar colour ── */
.stProgress > div > div > div > div {{ background-color:{BLUE} !important; }}

/* ── Tabs ── */
.stTabs [data-baseweb="tab"]           {{ font-weight:600; font-size:14px; }}
.stTabs [data-baseweb="tab-highlight"] {{ background-color:{BLUE} !important; }}

/* ── Pulse animation ── */
@keyframes pulse {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:.4; }} }}
.pulse {{ animation:pulse 1.5s infinite; }}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE — initialise once
# ─────────────────────────────────────────────
def init_state():
    defaults = {
        "page": "Home",
        "requests": [
            {"id": "NAV-1029", "name": "Ananya S.", "category": "Food",      "pickup": "Hostel A",      "dropoff": "Library",        "priority": "Normal",    "status": "Delivered",  "ts": "10:32 AM"},
            {"id": "NAV-1028", "name": "Rohan M.",  "category": "Parcel",    "pickup": "Cafeteria",     "dropoff": "Hostel B",       "priority": "Urgent",    "status": "En Route",   "ts": "10:45 AM"},
            {"id": "NAV-1027", "name": "Priya K.",  "category": "Medicines", "pickup": "Medical Centre","dropoff": "Academic Block", "priority": "Emergency", "status": "Delivered",  "ts": "09:58 AM"},
            {"id": "NAV-1026", "name": "Vijay R.",  "category": "Documents", "pickup": "Academic Block","dropoff": "Library",        "priority": "Normal",    "status": "Delivered",  "ts": "09:20 AM"},
            {"id": "NAV-1025", "name": "Neha T.",   "category": "Food",      "pickup": "Cafeteria",     "dropoff": "Hostel A",       "priority": "Normal",    "status": "Pending",    "ts": "11:10 AM"},
        ],
        "notifications": [
            {"type": "success", "title": "Delivery Completed", "body": "Package NAV-1029 delivered to Library.",            "time": "2 min ago"},
            {"type": "info",    "title": "TURBO En Route",     "body": "TURBO is heading from Cafeteria to Hostel B.",      "time": "8 min ago"},
            {"type": "info",    "title": "Request Confirmed",  "body": "Delivery NAV-1028 has been assigned to TURBO.",     "time": "10 min ago"},
            {"type": "warning", "title": "Path Rerouted",      "body": "TURBO rerouting due to obstacle near Cafeteria.",   "time": "1 hr ago"},
            {"type": "warning", "title": "Battery Alert",      "body": "TURBO #4 battery at 15 %. Returning after delivery.","time": "2 hrs ago"},
            {"type": "error",   "title": "GPS Degraded",       "body": "Signal temporarily weak. Backup navigation active.","time": "3 hrs ago"},
        ],
        "chat_messages": [
            {"role": "assistant", "text": "Hello! I'm the NAVIGO support bot. How can I help you today?"},
        ],
        "feedback_list": [],
        "maintenance_reports": [
            {"id": "MNT-001", "issue": "Battery Problem", "desc": "TURBO #4 battery depletes faster than expected.", "status": "In Progress", "reported": "Jun 12"},
            {"id": "MNT-002", "issue": "Sensor Issue",    "desc": "Proximity sensor giving false alerts on TURBO #2.", "status": "Resolved",    "reported": "Jun 10"},
        ],
        "tracking_step": 2,
        "tracking_eta":  512,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ─────────────────────────────────────────────
PAGES = [
    ("🏠", "Home"),
    ("📦", "Request Delivery"),
    ("📍", "Live Tracking"),
    ("🔔", "Notifications"),
    ("💬", "Helpdesk"),
    ("⭐", "Feedback"),
    ("🔧", "Maintenance"),
    ("📊", "Community Dashboard"),
]

with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center;padding:20px 0 20px;'>
        <div style='font-size:32px;'>🚚</div>
        <div style='font-size:24px;font-weight:900;color:white;letter-spacing:2px;margin:4px 0;'>NAVIGO</div>
        <div style='font-size:11px;color:#94a3b8;margin-bottom:12px;'>Smart Campus Delivery</div>
        <div style='font-size:12px;color:{SUCCESS};'>
            <span class='pulse' style='display:inline-block;width:8px;height:8px;
            background:{SUCCESS};border-radius:50%;margin-right:5px;'></span>
            TURBO Online
        </div>
    </div>
    <hr style='border-color:rgba(255,255,255,0.12);margin-bottom:8px;'>
    """, unsafe_allow_html=True)

    for icon, name in PAGES:
        if st.button(f"{icon}  {name}", key=f"nav_{name}"):
            st.session_state.page = name
            st.rerun()

    st.markdown("""
    <hr style='border-color:rgba(255,255,255,0.12);margin-top:16px;'>
    <div style='font-size:11px;color:rgba(255,255,255,0.3);text-align:center;padding:10px 0;'>
        NAVIGO v1.0 · Campus Logistics
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
STATUS_BADGE = {
    "Delivered": "badge-success",
    "En Route":  "badge-info",
    "Pending":   "badge-warning",
    "Assigned":  "badge-info",
    "Cancelled": "badge-danger",
}
PRIORITY_BADGE = {
    "Normal":    "badge-success",
    "Urgent":    "badge-warning",
    "Emergency": "badge-danger",
}
NOTIF_COLORS = {"success": SUCCESS, "info": BLUE, "warning": WARNING, "error": DANGER}
NOTIF_ICONS  = {"success": "✅", "info": "ℹ️", "warning": "⚠️", "error": "🚨"}


def metric_card(label: str, value: str, delta: str = "", color: str = BLUE):
    delta_html = f"<div style='font-size:12px;color:#64748b;margin-top:3px;'>{delta}</div>" if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div style='font-size:30px;font-weight:900;color:{color};line-height:1.1;'>{value}</div>
        <div style='font-size:13px;color:#64748b;font-weight:500;margin-top:5px;'>{label}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)


def notif_card(n: dict):
    color = NOTIF_COLORS.get(n["type"], BLUE)
    icon  = NOTIF_ICONS.get(n["type"], "ℹ️")
    st.markdown(f"""
    <div class="notif-card" style="border-left-color:{color};">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
            <strong style="font-size:14px;">{icon} {n['title']}</strong>
            <span style="font-size:12px;color:#94a3b8;">{n['time']}</span>
        </div>
        <div style="font-size:13px;color:#475569;">{n['body']}</div>
    </div>
    """, unsafe_allow_html=True)


def request_card(req: dict):
    """Render a delivery request as a styled card."""
    b_s = STATUS_BADGE.get(req["status"], "badge-info")
    b_p = PRIORITY_BADGE.get(req["priority"], "badge-success")
    st.markdown(f"""
    <div class="notif-card" style="border-left-color:{BLUE};">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
            <div>
                <strong style="font-size:15px;color:{NAVY};">{req['id']}</strong>
                <span style="color:#64748b;font-size:13px;margin-left:10px;">
                    {req['name']} · {req['category']}
                </span>
            </div>
            <div style="display:flex;gap:8px;">
                <span class="{b_p}">{req['priority']}</span>
                <span class="{b_s}">{req['status']}</span>
            </div>
        </div>
        <div style="font-size:13px;color:#475569;margin-top:6px;">
            📌 {req['pickup']} &nbsp;→&nbsp; 🏁 {req['dropoff']}
            &nbsp;·&nbsp; 🕐 {req['ts']}
        </div>
    </div>
    """, unsafe_allow_html=True)


def new_delivery_id() -> str:
    return f"NAV-{random.randint(1030, 9999)}"


# ─────────────────────────────────────────────
# PAGE: HOME
# ─────────────────────────────────────────────
def page_home():
    # Hero banner
    st.markdown(f"""
    <div class="hero-card">
        <div style='font-size:11px;letter-spacing:3px;color:{BLUE};font-weight:800;margin-bottom:6px;'>
            NAVIGO · AUTONOMOUS DELIVERY
        </div>
        <h1 style='color:white;margin:0 0 10px;font-size:2.4rem;font-weight:900;'>
            Meet TURBO 🚚
        </h1>
        <p style='color:rgba(255,255,255,0.72);font-size:15px;margin-bottom:20px;max-width:600px;'>
            Your Autonomous Campus Delivery Companion — faster, smarter, and fully trackable.
        </p>
        <div style='display:flex;gap:14px;flex-wrap:wrap;'>
            <div style='background:rgba(255,255,255,0.14);border-radius:10px;padding:9px 16px;font-size:13px;'>
                <span style='color:{SUCCESS};'>●</span>&nbsp; TURBO Online
            </div>
            <div style='background:rgba(255,255,255,0.14);border-radius:10px;padding:9px 16px;font-size:13px;'>
                ⚡ Avg Delivery: 8 min
            </div>
            <div style='background:rgba(255,255,255,0.14);border-radius:10px;padding:9px 16px;font-size:13px;'>
                🏆 284 Deliveries Completed
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric_card("Active Deliveries", "3",       "↑ 1 from yesterday")
    with c2: metric_card("Total Completed",   "284",     "All time",           color=SUCCESS)
    with c3: metric_card("Avg Delivery Time", "8 min",   "↓ 1 min this week",  color=WARNING)
    with c4: metric_card("TURBO Units",       "4",       "3 active · 1 charging")

    st.markdown("<br>", unsafe_allow_html=True)

    # Problem / Solution
    col_ps1, col_ps2 = st.columns(2)
    with col_ps1:
        st.markdown(f"""
        <div class="nav-card">
            <div style='font-size:18px;font-weight:800;color:{NAVY};margin-bottom:8px;'>🚨 Problem We Solve</div>
            <p style='color:#475569;font-size:14px;margin:0;'>
                Students and residents face delays in short-distance deliveries because existing
                systems depend on manual coordination and human availability — leading to
                inconsistent service and lost time.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_ps2:
        st.markdown(f"""
        <div class="nav-card">
            <div style='font-size:18px;font-weight:800;color:{NAVY};margin-bottom:8px;'>✅ Our Solution</div>
            <p style='color:#475569;font-size:14px;margin:0;'>
                NAVIGO deploys autonomous delivery rovers (TURBO) to automate secure, trackable,
                and efficient last-mile deliveries across campuses and gated communities — with
                real-time tracking and zero human intervention.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Features & designed-for
    st.markdown(f"<h3 style='color:{NAVY};margin-top:8px;'>🚀 Core Features</h3>", unsafe_allow_html=True)
    fc1, fc2, fc3, fc4 = st.columns(4)
    features = [
        ("📍", "Geo Tracking",         "Real-time live map of TURBO's position."),
        ("🔒", "End-to-End Security",  "Lockable compartment + live camera monitoring."),
        ("🔔", "Smart Notifications",  "Instant alerts for every delivery milestone."),
        ("🛠", "Maintenance Support",  "Fleet health dashboard and issue reporting."),
    ]
    for col, (icon, title, desc) in zip([fc1, fc2, fc3, fc4], features):
        with col:
            st.markdown(f"""
            <div class="metric-card" style="text-align:left;padding:18px;">
                <div style='font-size:26px;margin-bottom:8px;'>{icon}</div>
                <div style='font-weight:700;font-size:14px;color:{NAVY};margin-bottom:4px;'>{title}</div>
                <div style='font-size:12px;color:#64748b;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_how, col_recent = st.columns([3, 2])

    with col_how:
        st.markdown(f"<h3 style='color:{NAVY};'>📦 How NAVIGO Works</h3>", unsafe_allow_html=True)
        steps = [
            ("1", "Place Request",  "Submit via the app in seconds — pick item, location, priority."),
            ("2", "TURBO Assigned", "The nearest available TURBO unit is dispatched automatically."),
            ("3", "Live Tracking",  "Follow TURBO on the campus map in real-time."),
            ("4", "Delivered",      "Package arrives at your door. Rate your experience!"),
        ]
        for num, title, desc in steps:
            st.markdown(f"""
            <div style='display:flex;gap:14px;margin-bottom:16px;align-items:flex-start;'>
                <div style='background:{BLUE};color:white;border-radius:50%;
                            min-width:32px;height:32px;display:flex;align-items:center;
                            justify-content:center;font-weight:900;font-size:14px;'>{num}</div>
                <div>
                    <div style='font-weight:700;font-size:15px;color:{NAVY};'>{title}</div>
                    <div style='color:#64748b;font-size:13px;margin-top:2px;'>{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"<h3 style='color:{NAVY};margin-top:12px;'>🌍 Designed For</h3>", unsafe_allow_html=True)
        venues = [("🏫", "Universities"), ("🏘", "Gated Communities"), ("🏢", "Corporate Parks"), ("🌳", "Smart Public Spaces")]
        v_cols = st.columns(4)
        for col, (icon, label) in zip(v_cols, venues):
            with col:
                st.markdown(f"""
                <div class="metric-card" style="padding:14px;">
                    <div style='font-size:22px;'>{icon}</div>
                    <div style='font-size:12px;font-weight:600;color:{NAVY};margin-top:4px;'>{label}</div>
                </div>
                """, unsafe_allow_html=True)

    with col_recent:
        st.markdown(f"<h3 style='color:{NAVY};'>🕐 Recent Activity</h3>", unsafe_allow_html=True)
        for req in st.session_state.requests[:4]:
            request_card(req)
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📦  Request New Delivery →", key="home_cta"):
            st.session_state.page = "Request Delivery"
            st.rerun()


# ─────────────────────────────────────────────
# PAGE: REQUEST DELIVERY
# ─────────────────────────────────────────────
LOCATIONS = ["Hostel A", "Hostel B", "Library", "Cafeteria", "Academic Block", "Medical Centre"]

def page_request():
    st.markdown(f"<h2 style='color:{NAVY};'>📦 Request Delivery</h2>", unsafe_allow_html=True)
    st.markdown("Fill in the details below and TURBO will be dispatched to you.")
    st.divider()

    with st.form("delivery_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            name    = st.text_input("👤 Customer Name",  placeholder="e.g. Arjun Sharma")
            contact = st.text_input("📱 Contact Number", placeholder="e.g. 9876543210")
        with c2:
            category = st.selectbox("📦 Item Category", ["Food", "Medicines", "Parcel", "Documents"])
            priority  = st.selectbox("🚦 Priority Level", ["Normal", "Urgent", "Emergency"])

        c3, c4 = st.columns(2)
        with c3:
            pickup  = st.selectbox("📌 Pickup Location",   LOCATIONS)
        with c4:
            dropoff = st.selectbox("🏁 Delivery Location", LOCATIONS)

        notes = st.text_area(
            "📝 Special Instructions (optional)",
            placeholder="e.g. Fragile item, leave at door, call on arrival…",
            height=80,
        )
        submitted = st.form_submit_button("🤖 Assign TURBO", use_container_width=True)

    if submitted:
        if not name.strip() or not contact.strip():
            st.error("⚠️ Please enter your name and contact number.")
        elif pickup == dropoff:
            st.warning("⚠️ Pickup and delivery location cannot be the same. Please choose different locations.")
        else:
            new_id = new_delivery_id()
            now_ts = datetime.datetime.now().strftime("%I:%M %p")
            st.session_state.requests.insert(0, {
                "id":       new_id,
                "name":     name.strip(),
                "category": category,
                "pickup":   pickup,
                "dropoff":  dropoff,
                "priority": priority,
                "status":   "Assigned",
                "ts":       now_ts,
            })
            st.session_state.notifications.insert(0, {
                "type":  "info",
                "title": f"TURBO Assigned — {new_id}",
                "body":  f"TURBO is heading from {pickup} to {dropoff}.",
                "time":  "Just now",
            })
            st.success(f"✅ TURBO has been assigned! **Delivery ID: {new_id}**")
            st.balloons()
            r1, r2, r3 = st.columns(3)
            r1.metric("Delivery ID",     new_id)
            r2.metric("Estimated Time",  "8–12 min")
            r3.metric("Status",          "Assigned → En Route")

    # Delivery list
    st.markdown(f"<h3 style='color:{NAVY};margin-top:16px;'>📋 All Delivery Requests</h3>", unsafe_allow_html=True)
    if not st.session_state.requests:
        st.info("No delivery requests yet.")
    for req in st.session_state.requests:
        request_card(req)


# ─────────────────────────────────────────────
# PAGE: LIVE TRACKING
# ─────────────────────────────────────────────
TRACK_STEPS = ["Request Received", "TURBO Assigned", "En Route", "Near Destination", "Delivered"]

BUILDINGS = {
    "Hostel A":       (0.12, 0.88),
    "Cafeteria":      (0.38, 0.65),
    "Academic Block": (0.60, 0.44),
    "Library":        (0.85, 0.12),
    "Medical Centre": (0.20, 0.44),
    "Hostel B":       (0.76, 0.80),
}
WAYPOINTS_X = [0.12, 0.38, 0.60, 0.85]
WAYPOINTS_Y = [0.88, 0.65, 0.44, 0.12]


def compute_turbo_position(step: int) -> tuple:
    """Interpolate TURBO's (x, y) position based on current step."""
    total_steps = len(TRACK_STEPS) - 1
    frac = min(step / total_steps, 1.0)
    seg  = min(int(frac * (len(WAYPOINTS_X) - 1)), len(WAYPOINTS_X) - 2)
    t    = (frac * (len(WAYPOINTS_X) - 1)) - seg
    x = WAYPOINTS_X[seg] + t * (WAYPOINTS_X[seg + 1] - WAYPOINTS_X[seg])
    y = WAYPOINTS_Y[seg] + t * (WAYPOINTS_Y[seg + 1] - WAYPOINTS_Y[seg])
    return x, y


def page_tracking():
    st.markdown(f"<h2 style='color:{NAVY};'>📍 Live Tracking</h2>", unsafe_allow_html=True)

    active  = st.session_state.tracking_step
    eta_sec = st.session_state.tracking_eta
    mins, secs = divmod(eta_sec, 60)

    # ETA + progress side by side
    col_eta, col_prog = st.columns([1, 2])

    with col_eta:
        st.markdown(f"""
        <div class="metric-card" style="padding:28px 20px;">
            <div style="font-size:11px;color:#64748b;font-weight:700;letter-spacing:1.5px;margin-bottom:10px;">
                ESTIMATED ARRIVAL
            </div>
            <div style="font-size:48px;font-weight:900;color:{NAVY};letter-spacing:3px;line-height:1;">
                {mins:02d}:{secs:02d}
            </div>
            <div style="font-size:13px;color:{BLUE};margin-top:12px;font-weight:600;">
                <span class="pulse" style="display:inline-block;width:8px;height:8px;
                background:{SUCCESS};border-radius:50%;margin-right:6px;"></span>
                TURBO Online · Live
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_prog:
        st.markdown(f"""
        <div class="nav-card">
            <div style="font-weight:700;font-size:16px;color:{NAVY};margin-bottom:14px;">
                📦 Delivery Progress
            </div>
        """, unsafe_allow_html=True)
        for i, step in enumerate(TRACK_STEPS):
            if i < active:
                icon, color, fw = "✅", SUCCESS, "600"
            elif i == active:
                icon, color, fw = "🔵", BLUE, "800"
            else:
                icon, color, fw = "⚪", "#94a3b8", "400"
            current_tag = (
                "<span style='margin-left:auto;font-size:11px;color:#94a3b8;'>← Current</span>"
                if i == active else ""
            )
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:12px;margin-bottom:10px;">
                <span style="font-size:18px;">{icon}</span>
                <span style="color:{color};font-weight:{fw};font-size:14px;">{step}</span>
                {current_tag}
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Campus Map ──
    st.markdown(f"<h3 style='color:{NAVY};'>🗺️ Campus Map — TURBO Location</h3>", unsafe_allow_html=True)

    turbo_x, turbo_y = compute_turbo_position(active)

    fig = go.Figure()

    # Route path
    fig.add_trace(go.Scatter(
        x=WAYPOINTS_X, y=WAYPOINTS_Y,
        mode="lines",
        line=dict(color=BLUE, width=3, dash="dot"),
        name="Route",
        hoverinfo="skip",
    ))

    # Buildings
    fig.add_trace(go.Scatter(
        x=[v[0] for v in BUILDINGS.values()],
        y=[v[1] for v in BUILDINGS.values()],
        mode="markers+text",
        marker=dict(size=18, color=NAVY, symbol="square"),
        text=list(BUILDINGS.keys()),
        textposition="top center",
        textfont=dict(size=11, color=NAVY),
        name="Buildings",
        hoverinfo="text",
    ))

    # TURBO marker
    fig.add_trace(go.Scatter(
        x=[turbo_x], y=[turbo_y],
        mode="markers+text",
        marker=dict(size=24, color=BLUE, symbol="circle",
                    line=dict(color="white", width=3)),
        text=["🚚 TURBO"],
        textposition="top center",
        textfont=dict(size=12, color=BLUE),
        name="TURBO",
    ))

    fig.update_layout(
        height=340,
        margin=dict(l=0, r=0, t=10, b=10),
        plot_bgcolor="#f0f4ff",
        paper_bgcolor="white",
        showlegend=False,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05, 1.05]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05, 1.05]),
        shapes=[dict(
            type="rect", x0=-0.02, y0=-0.02, x1=1.02, y1=1.02,
            line=dict(color="#e2e8f0", width=1), fillcolor="rgba(0,0,0,0)",
        )],
    )
    st.plotly_chart(fig, use_container_width=True)

    # Controls
    btn1, btn2, _ = st.columns([1, 1, 4])
    with btn1:
        if st.button("⏩ Advance Step"):
            st.session_state.tracking_step = (active + 1) % len(TRACK_STEPS)
            st.session_state.tracking_eta  = max(0, eta_sec - 120)
            st.rerun()
    with btn2:
        if st.button("🔄 Reset"):
            st.session_state.tracking_step = 0
            st.session_state.tracking_eta  = 600
            st.rerun()

    # Active delivery details
    active_req = next((r for r in st.session_state.requests if r["status"] == "En Route"), None)
    if active_req:
        st.markdown(f"<h3 style='color:{NAVY};margin-top:8px;'>📦 Active Delivery Details</h3>", unsafe_allow_html=True)
        d1, d2, d3, d4 = st.columns(4)
        d1.metric("Delivery ID", active_req["id"])
        d2.metric("Item",        active_req["category"])
        d3.metric("Customer",    active_req["name"])
        d4.metric("Priority",    active_req["priority"])
    else:
        st.info("No active En Route delivery at the moment.")


# ─────────────────────────────────────────────
# PAGE: NOTIFICATIONS
# ─────────────────────────────────────────────
def page_notifications():
    st.markdown(f"<h2 style='color:{NAVY};'>🔔 Notifications</h2>", unsafe_allow_html=True)

    tab_all, tab_ok, tab_warn, tab_err = st.tabs(
        ["All", "✅ Success", "⚠️ Warnings", "🚨 Alerts"]
    )

    def render_tab(items):
        if items:
            for n in items:
                notif_card(n)
        else:
            st.info("No notifications in this category.")

    with tab_all:  render_tab(st.session_state.notifications)
    with tab_ok:   render_tab([n for n in st.session_state.notifications if n["type"] == "success"])
    with tab_warn: render_tab([n for n in st.session_state.notifications if n["type"] == "warning"])
    with tab_err:  render_tab([n for n in st.session_state.notifications if n["type"] == "error"])

    st.divider()
    if st.button("🗑️ Clear All Notifications"):
        st.session_state.notifications = []
        st.rerun()


# ─────────────────────────────────────────────
# PAGE: HELPDESK
# ─────────────────────────────────────────────
BOT_ANSWERS = {
    "where":   "TURBO is currently near the Academic Block and will reach you in ~3 minutes.",
    "cancel":  "Cancellations are only possible within 2 minutes of placing a request. Please act quickly!",
    "time":    "Average delivery time within campus is 8–12 minutes. Peak hours may add 3–5 minutes.",
    "track":   "You can track TURBO live on the 'Live Tracking' page — click 📍 Live Tracking in the sidebar.",
    "help":    "I can assist with tracking, cancellations, delivery times, item categories, and general queries.",
    "default": "I've noted your concern and escalated it to our support team. A human agent will respond shortly.",
}

FAQS = [
    ("Where is my delivery?",        "TURBO is en route — open Live Tracking for the real-time map."),
    ("How do I cancel a request?",   "Contact support within 2 minutes of placing the request."),
    ("How long does delivery take?", "8–12 minutes on average. Peak hours may add a few minutes."),
    ("What can TURBO carry?",        "Up to 5 kg — food, medicines, documents, parcels."),
    ("What are TURBO's hours?",      "7:00 AM – 10:00 PM daily, including weekends."),
    ("Is my item safe with TURBO?",  "Yes! TURBO has a lockable compartment and live camera monitoring."),
]


def get_bot_response(text: str) -> str:
    t = text.lower()
    if any(w in t for w in ["where", "location", "find"]): return BOT_ANSWERS["where"]
    if "cancel" in t:                                        return BOT_ANSWERS["cancel"]
    if any(w in t for w in ["time", "long", "minute"]):     return BOT_ANSWERS["time"]
    if "track" in t:                                         return BOT_ANSWERS["track"]
    if "help"  in t:                                         return BOT_ANSWERS["help"]
    return BOT_ANSWERS["default"]


def page_helpdesk():
    st.markdown(f"<h2 style='color:{NAVY};'>💬 Helpdesk & Support</h2>", unsafe_allow_html=True)
    tab_chat, tab_faq = st.tabs(["💬 Live Chat", "❓ FAQs"])

    with tab_chat:
        st.markdown("Chat with the NAVIGO support assistant.")
        for msg in st.session_state.chat_messages:
            avatar = "🤖" if msg["role"] == "assistant" else "👤"
            with st.chat_message(msg["role"], avatar=avatar):
                st.markdown(msg["text"])

        user_input = st.chat_input("Type your message…")
        if user_input:
            st.session_state.chat_messages.append({"role": "user", "text": user_input})
            st.session_state.chat_messages.append(
                {"role": "assistant", "text": get_bot_response(user_input)}
            )
            st.rerun()

        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_messages = [
                {"role": "assistant", "text": "Hello! I'm the NAVIGO support bot. How can I help you today?"}
            ]
            st.rerun()

    with tab_faq:
        st.markdown(f"<h3 style='color:{NAVY};'>Frequently Asked Questions</h3>", unsafe_allow_html=True)
        for q, a in FAQS:
            with st.expander(q):
                st.markdown(a)


# ─────────────────────────────────────────────
# PAGE: FEEDBACK
# ─────────────────────────────────────────────
SAMPLE_REVIEWS = [
    ("★★★★★", "Fast delivery and accurate tracking. Loved it!",        "Rohan M."),
    ("★★★★★", "TURBO arrived exactly on time, packaging was perfect.", "Priya K."),
    ("★★★★☆", "Smooth experience and super easy to use.",              "Ananya S."),
]


def page_feedback():
    st.markdown(f"<h2 style='color:{NAVY};'>⭐ Feedback</h2>", unsafe_allow_html=True)
    st.markdown("Help us improve NAVIGO and TURBO by sharing your experience.")
    st.divider()

    with st.form("feedback_form", clear_on_submit=True):
        delivery_id = st.text_input("📦 Delivery ID (optional)", placeholder="e.g. NAV-1029")
        rating = st.select_slider(
            "⭐ Overall Rating",
            options=[1, 2, 3, 4, 5],
            value=5,
            format_func=lambda x: "⭐" * x,
        )
        categories = st.multiselect(
            "👍 What went well?",
            ["Speed", "Punctuality", "Packaging", "TURBO behaviour", "App experience", "Customer service"],
        )
        comment = st.text_area("💬 Your Comments", placeholder="Tell us about your experience…", height=100)
        recommend = st.radio(
            "Would you recommend NAVIGO?",
            ["Yes, definitely!", "Maybe", "No"],
            horizontal=True,
        )
        submitted = st.form_submit_button("📨 Submit Feedback", use_container_width=True)

    if submitted:
        if rating == 0:
            st.warning("Please select a rating before submitting.")
        else:
            entry = {
                "id":         delivery_id.strip() or "—",
                "rating":     rating,
                "categories": categories,
                "comment":    comment.strip(),
                "recommend":  recommend,
                "ts":         datetime.datetime.now().strftime("%b %d, %I:%M %p"),
            }
            st.session_state.feedback_list.insert(0, entry)
            st.success("Thank you for your feedback! 🙏 We'll keep improving TURBO for you.")
            st.balloons()

    # Sample reviews
    st.markdown(f"<h3 style='color:{NAVY};margin-top:8px;'>🌟 Sample Reviews</h3>", unsafe_allow_html=True)
    for stars, text, author in SAMPLE_REVIEWS:
        st.markdown(f"""
        <div class="notif-card" style="border-left-color:{SUCCESS};">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="font-size:16px;color:{WARNING};">{stars}</span>
                <span style="font-size:12px;color:#94a3b8;">{author}</span>
            </div>
            <div style="font-size:14px;color:#475569;">{text}</div>
        </div>
        """, unsafe_allow_html=True)

    # Submitted feedback
    if st.session_state.feedback_list:
        st.markdown(f"<h3 style='color:{NAVY};'>📋 Your Submitted Feedback</h3>", unsafe_allow_html=True)
        for fb in st.session_state.feedback_list:
            stars = "⭐" * fb["rating"]
            cats  = ", ".join(fb["categories"]) if fb["categories"] else "—"
            st.markdown(f"""
            <div class="notif-card" style="border-left-color:{BLUE};">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                    <strong style="color:{NAVY};">{fb['id']}</strong>
                    <span style="font-size:16px;">{stars}</span>
                    <span style="font-size:12px;color:#94a3b8;">{fb['ts']}</span>
                </div>
                <div style="font-size:13px;color:#64748b;margin-bottom:4px;">👍 {cats}</div>
                <div style="font-size:14px;color:#475569;">{fb['comment'] or '<em>No comment provided</em>'}</div>
                <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Recommend: {fb['recommend']}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: MAINTENANCE
# ─────────────────────────────────────────────
TURBO_UNITS = [
    {"id": "TURBO #1", "battery": 87, "status": "Active",   "location": "Hostel A",     "deliveries": 12},
    {"id": "TURBO #2", "battery": 62, "status": "Active",   "location": "Library",      "deliveries": 9},
    {"id": "TURBO #3", "battery": 95, "status": "Active",   "location": "Cafeteria",    "deliveries": 15},
    {"id": "TURBO #4", "battery": 15, "status": "Charging", "location": "Base Station", "deliveries": 6},
]


def battery_color(pct: int) -> str:
    return SUCCESS if pct > 50 else (WARNING if pct > 20 else DANGER)


def page_maintenance():
    st.markdown(f"<h2 style='color:{NAVY};'>🔧 Maintenance</h2>", unsafe_allow_html=True)
    tab_status, tab_report = st.tabs(["🤖 TURBO Fleet", "📝 Report Issue"])

    with tab_status:
        st.markdown(f"<h3 style='color:{NAVY};'>Fleet Overview</h3>", unsafe_allow_html=True)

        # 2-column grid for units
        cols = st.columns(2)
        for i, unit in enumerate(TURBO_UNITS):
            bat   = unit["battery"]
            bc    = battery_color(bat)
            s_cls = "badge-success" if unit["status"] == "Active" else "badge-warning"
            with cols[i % 2]:
                st.markdown(f"""
                <div class="nav-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <strong style="font-size:16px;color:{NAVY};">🤖 {unit['id']}</strong>
                        <span class="{s_cls}">{unit['status']}</span>
                    </div>
                    <div style="display:flex;gap:20px;font-size:13px;color:#64748b;margin-bottom:10px;">
                        <span>📌 {unit['location']}</span>
                        <span>📦 {unit['deliveries']} deliveries today</span>
                    </div>
                    <div style="font-size:13px;font-weight:600;margin-bottom:4px;">
                        Battery: <span style="color:{bc};">{bat}%</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.progress(bat / 100)
                st.markdown("<br>", unsafe_allow_html=True)

        # System health
        st.markdown(f"<h3 style='color:{NAVY};'>❤️ System Health</h3>", unsafe_allow_html=True)
        health_items = [
            ("Battery Health", 0.94),
            ("GPS Accuracy",   0.97),
            ("Sensors",        0.91),
            ("Connectivity",   0.88),
        ]
        for label, val in health_items:
            pct = int(val * 100)
            bar_color = SUCCESS if val >= 0.90 else (WARNING if val >= 0.75 else DANGER)
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;font-size:13px;
                        font-weight:600;margin-bottom:4px;">
                <span style="color:{NAVY};">{label}</span>
                <span style="color:{bar_color};">{pct}%</span>
            </div>
            """, unsafe_allow_html=True)
            st.progress(val)
            st.markdown("<br style='margin:-12px;'>", unsafe_allow_html=True)

        # System metrics
        st.markdown(f"<h3 style='color:{NAVY};margin-top:8px;'>📊 System Metrics</h3>", unsafe_allow_html=True)
        mc1, mc2, mc3, mc4 = st.columns(4)
        with mc1: metric_card("Uptime",           "99.2%",    "Last 30 days",  color=SUCCESS)
        with mc2: metric_card("Avg Temperature",  "42 °C",    "Normal range")
        with mc3: metric_card("Obstacle Avoids",  "34",       "This week")
        with mc4: metric_card("Maintenance Due",  "TURBO #4", "Battery swap",  color=WARNING)

    with tab_report:
        st.markdown(f"<h3 style='color:{NAVY};'>Report an Issue</h3>", unsafe_allow_html=True)
        with st.form("maintenance_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                unit_sel   = st.selectbox("🤖 TURBO Unit",  [u["id"] for u in TURBO_UNITS])
                issue_type = st.selectbox("⚠️ Issue Type", [
                    "Battery Problem", "Sensor Issue", "Navigation Error",
                    "Mechanical Failure", "Software Glitch", "Other",
                ])
            with c2:
                severity    = st.selectbox("🚦 Severity", ["Low", "Medium", "High", "Critical"])
                reported_by = st.text_input("👤 Reported By", placeholder="Your name")
            description = st.text_area("📝 Description", placeholder="Describe the issue in detail…", height=100)
            submitted   = st.form_submit_button("📨 Submit Report", use_container_width=True)

        if submitted:
            if not reported_by.strip():
                st.warning("Please enter your name before submitting.")
            else:
                new_id = f"MNT-{random.randint(100, 999)}"
                st.session_state.maintenance_reports.insert(0, {
                    "id":       new_id,
                    "issue":    issue_type,
                    "desc":     description.strip() or "No description provided.",
                    "status":   "Open",
                    "reported": datetime.datetime.now().strftime("%b %d"),
                })
                st.session_state.notifications.insert(0, {
                    "type":  "warning",
                    "title": f"Maintenance Report {new_id}",
                    "body":  f"{unit_sel}: {issue_type} — {severity} severity.",
                    "time":  "Just now",
                })
                st.success(f"Issue reported! Ticket **{new_id}** created. Our team has been notified.")

        st.markdown(f"<h3 style='color:{NAVY};margin-top:12px;'>📋 Maintenance Log</h3>", unsafe_allow_html=True)
        STATUS_CLS = {
            "In Progress": "badge-warning",
            "Resolved":    "badge-success",
            "Open":        "badge-danger",
        }
        for report in st.session_state.maintenance_reports:
            s_cls = STATUS_CLS.get(report["status"], "badge-info")
            st.markdown(f"""
            <div class="notif-card" style="border-left-color:{WARNING};">
                <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                    <strong style="color:{NAVY};">{report['id']} — {report['issue']}</strong>
                    <span class="{s_cls}">{report['status']}</span>
                </div>
                <div style="font-size:13px;color:#475569;">{report['desc']}</div>
                <div style="font-size:12px;color:#94a3b8;margin-top:4px;">Reported: {report['reported']}</div>
            </div>
            """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PAGE: COMMUNITY DASHBOARD
# ─────────────────────────────────────────────
def page_dashboard():
    st.markdown(f"<h2 style='color:{NAVY};'>📊 Community Dashboard</h2>", unsafe_allow_html=True)

    # KPIs
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1: metric_card("Total Requests",    "284",     "All time")
    with k2: metric_card("Active Now",        "3",       "Live",               color=BLUE)
    with k3: metric_card("Completed Today",   "47",      "↑ 12 vs yesterday",  color=SUCCESS)
    with k4: metric_card("Avg Delivery Time", "8.2 min", "↓ 0.8 min",          color=WARNING)
    with k5: metric_card("Success Rate",      "98.6 %",  "Last 7 days",        color=SUCCESS)

    st.markdown("<br>", unsafe_allow_html=True)

    # Action buttons
    ab1, ab2, ab3 = st.columns(3)
    with ab1:
        if st.button("🚨 Emergency Stop", use_container_width=True):
            st.error("Emergency stop signal sent to all TURBO units!")
    with ab2:
        if st.button("⏸ Pause All TURBO", use_container_width=True):
            st.warning("All TURBO units paused.")
    with ab3:
        if st.button("📄 Generate Report", use_container_width=True):
            st.success("Report generation started. Download will be ready shortly.")

    st.markdown("<br>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        # Daily volume
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        vals = [38, 52, 45, 61, 47, 29, 12]
        fig_vol = go.Figure(go.Bar(
            x=days, y=vals,
            marker_color=[BLUE if d != "Thu" else "#1a3d6b" for d in days],
            text=vals, textposition="outside",
            textfont=dict(size=12, color=NAVY),
        ))
        fig_vol.update_layout(
            title=dict(text="Daily Delivery Volume (This Week)", font=dict(size=15, color=NAVY)),
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(showgrid=True, gridcolor="#e2e8f0", title="Deliveries"),
            xaxis=dict(showgrid=False),
            margin=dict(l=0, r=0, t=48, b=20),
            height=280,
        )
        st.plotly_chart(fig_vol, use_container_width=True)

        # Category donut
        cats   = ["Food", "Parcel", "Documents", "Medicines"]
        counts = [35, 28, 22, 15]
        fig_pie = go.Figure(go.Pie(
            labels=cats, values=counts,
            marker_colors=[BLUE, WARNING, SUCCESS, DANGER],
            hole=0.50,
            textinfo="label+percent",
            textfont_size=12,
        ))
        fig_pie.update_layout(
            title=dict(text="Deliveries by Category", font=dict(size=15, color=NAVY)),
            paper_bgcolor="white",
            margin=dict(l=0, r=0, t=48, b=20),
            height=280,
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        # Hourly trend
        hours  = list(range(7, 23))
        hourly = [2, 5, 8, 12, 9, 6, 14, 18, 15, 10, 7, 9, 11, 8, 5, 3]
        fig_hr = go.Figure(go.Scatter(
            x=hours, y=hourly,
            mode="lines+markers",
            line=dict(color=BLUE, width=2.5),
            marker=dict(size=6, color=BLUE),
            fill="tozeroy",
            fillcolor="rgba(69,137,245,0.12)",
        ))
        fig_hr.update_layout(
            title=dict(text="Hourly Requests (Today)", font=dict(size=15, color=NAVY)),
            plot_bgcolor="white", paper_bgcolor="white",
            yaxis=dict(showgrid=True, gridcolor="#e2e8f0"),
            xaxis=dict(
                tickvals=hours,
                ticktext=[f"{h}:00" for h in hours],
                showgrid=False, tickangle=-45,
            ),
            margin=dict(l=0, r=0, t=48, b=60),
            height=240,
        )
        st.plotly_chart(fig_hr, use_container_width=True)

        # Top locations
        st.markdown(f"<h4 style='color:{NAVY};'>📍 Top Delivery Locations</h4>", unsafe_allow_html=True)
        locations = [
            ("Library",        61, BLUE),
            ("Hostel A",       48, SUCCESS),
            ("Cafeteria",      39, WARNING),
            ("Academic Block", 31, NAVY),
            ("Medical Centre", 18, DANGER),
        ]
        for loc, pct, color in locations:
            st.markdown(f"""
            <div style="margin-bottom:6px;">
                <div style="display:flex;justify-content:space-between;
                            font-size:13px;font-weight:600;margin-bottom:3px;">
                    <span style="color:{NAVY};">{loc}</span>
                    <span style="color:{color};">{pct}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.progress(pct / 100)

    # Delivery records table
    st.markdown(f"<h3 style='color:{NAVY};margin-top:16px;'>📋 Recent Delivery Records</h3>", unsafe_allow_html=True)

    h_style = f"background:{NAVY};color:white;padding:11px 14px;font-size:13px;font-weight:700;text-align:left;"
    r_style = "padding:10px 14px;font-size:13px;border-bottom:1px solid #e2e8f0;"

    rows_html = ""
    for req in st.session_state.requests[:8]:
        b_s = STATUS_BADGE.get(req["status"], "badge-info")
        b_p = PRIORITY_BADGE.get(req["priority"], "badge-success")
        rows_html += f"""
        <tr>
            <td style="{r_style} font-weight:700;color:{BLUE};">{req['id']}</td>
            <td style="{r_style}">{req['name']}</td>
            <td style="{r_style}">{req['category']}</td>
            <td style="{r_style}">{req['pickup']}</td>
            <td style="{r_style}">{req['dropoff']}</td>
            <td style="{r_style}"><span class="{b_p}">{req['priority']}</span></td>
            <td style="{r_style}"><span class="{b_s}">{req['status']}</span></td>
            <td style="{r_style}">{req['ts']}</td>
        </tr>
        """

    st.markdown(f"""
    <div style="overflow-x:auto;border-radius:14px;
                box-shadow:0 2px 10px rgba(0,0,0,0.07);margin-top:8px;">
        <table style="width:100%;border-collapse:collapse;background:white;
                      border-radius:14px;overflow:hidden;">
            <thead>
                <tr>
                    <th style="{h_style}">ID</th>
                    <th style="{h_style}">Customer</th>
                    <th style="{h_style}">Category</th>
                    <th style="{h_style}">Pickup</th>
                    <th style="{h_style}">Drop-off</th>
                    <th style="{h_style}">Priority</th>
                    <th style="{h_style}">Status</th>
                    <th style="{h_style}">Time</th>
                </tr>
            </thead>
            <tbody>{rows_html}</tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
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