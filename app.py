import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

st.set_page_config(page_title="Skill Gap Analyzer", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Syne:wght@700;800&display=swap');
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;}
.stApp{background:linear-gradient(135deg,#0f0c29,#1a1040,#0d1b3e,#0a2547);}
.stApp::before{content:'';position:fixed;top:-20%;left:-15%;width:55vw;height:55vw;background:radial-gradient(circle,rgba(120,80,255,0.18),transparent 70%);border-radius:50%;pointer-events:none;z-index:0;}
.stApp::after{content:'';position:fixed;bottom:-15%;right:-10%;width:45vw;height:45vw;background:radial-gradient(circle,rgba(0,180,255,0.14),transparent 70%);border-radius:50%;pointer-events:none;z-index:0;}
section[data-testid="stSidebar"]{background:rgba(255,255,255,0.04)!important;backdrop-filter:blur(24px)!important;border-right:1px solid rgba(255,255,255,0.10)!important;}
section[data-testid="stSidebar"] label{color:rgba(255,255,255,0.7)!important;font-size:0.83rem!important;}
section[data-testid="stSidebar"] .stSelectbox>div>div,section[data-testid="stSidebar"] input{background:rgba(255,255,255,0.07)!important;border:1px solid rgba(255,255,255,0.14)!important;border-radius:12px!important;color:#fff!important;}
[data-testid="collapsedControl"]{visibility:visible!important;display:flex!important;opacity:1!important;}
.main .block-container{padding:2rem 2.5rem;max-width:1280px;}
.hero{font-family:'Syne',sans-serif;font-size:2.6rem;font-weight:800;background:linear-gradient(135deg,#fff 30%,#a5b4fc 70%,#7dd3fc);-webkit-background-clip:text;-webkit-text-fill-color:transparent;margin-bottom:0.2rem;}
.hero-sub{color:rgba(255,255,255,0.4);font-size:0.9rem;font-weight:300;margin-bottom:2rem;}
.glass{background:rgba(255,255,255,0.055);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:1.6rem 1.8rem;margin-bottom:1.2rem;box-shadow:0 4px 30px rgba(0,0,0,0.3);}
.lbl{font-size:0.68rem;font-weight:600;letter-spacing:0.14em;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-bottom:0.8rem;}
.grid4{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:0.9rem;}
.chip{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.10);border-radius:14px;padding:0.8rem 1rem;}
.chip .k{font-size:0.68rem;font-weight:600;letter-spacing:0.10em;text-transform:uppercase;color:rgba(255,255,255,0.35);margin-bottom:0.25rem;}
.chip .v{font-size:0.92rem;font-weight:500;color:#fff;}
.pills{display:flex;flex-wrap:wrap;gap:0.45rem;margin-top:0.5rem;}
.pill{padding:0.28rem 0.78rem;border-radius:999px;font-size:0.77rem;font-weight:500;}
.pm{background:rgba(52,211,153,0.15);border:1px solid rgba(52,211,153,0.38);color:#6ee7b7;}
.px{background:rgba(248,113,113,0.13);border:1px solid rgba(248,113,113,0.35);color:#fca5a5;}
.pr{background:rgba(165,180,252,0.13);border:1px solid rgba(165,180,252,0.35);color:#c7d2fe;}
.score-big{font-family:'Syne',sans-serif;font-size:4rem;font-weight:800;line-height:1;}
.track{background:rgba(255,255,255,0.08);border-radius:999px;height:8px;overflow:hidden;margin-top:0.7rem;}
.fill{height:100%;border-radius:999px;background:linear-gradient(90deg,#818cf8,#38bdf8,#34d399);}
#MainMenu,footer{visibility:hidden;}
.stSelectbox>div>div{color:#fff!important;}
.stSelectbox svg{fill:rgba(255,255,255,0.5)!important;}
[data-testid="stDataFrame"]{border-radius:14px!important;border:1px solid rgba(255,255,255,0.10)!important;}
</style>
""", unsafe_allow_html=True)

# ── Data & helpers ────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("candidate_dataset_9999.csv")
    df["skills_list"] = df["resume_skills"].str.lower().str.split(",").apply(lambda x: [s.strip() for s in x])
    return df

def role_req_skills(df, role, n):
    skills = [s for sl in df[df["job_role"]==role]["skills_list"] for s in sl]
    return [s for s,_ in Counter(skills).most_common(n)]

def skill_gap(c_skills, req):
    c, r = set(c_skills), set(req)
    matched, missing = sorted(c&r), sorted(r-c)
    return matched, missing, (len(matched)/len(r)*100 if r else 0)

def style_ax(fig, ax):
    fig.patch.set_alpha(0); ax.set_facecolor((0,0,0,0))
    for sp in ax.spines.values(): sp.set_edgecolor("#1e3a5f"); sp.set_linewidth(0.8)
    ax.tick_params(colors="white", labelsize=9)
    ax.xaxis.label.set_color("white"); ax.yaxis.label.set_color("white"); ax.title.set_color("white")
    ax.grid(axis="y", color=(1,1,1,0.06), linewidth=0.7, linestyle="--")

df = load_data()
roles = sorted(df["job_role"].unique())

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✦ Controls")
    search = st.text_input("🔍 Search Candidate", placeholder="Type a name…")
    opts = df[df["candidate_name"].str.contains(search, case=False, na=False)]["candidate_name"].tolist() if search else df["candidate_name"].tolist()
    sel_c = st.selectbox("👤 Candidate", opts)
    sel_j = st.selectbox("💼 Job Role", roles)
    top_n = st.slider("🎯 Required Skills Count", 3, 12, 6)
    st.caption("✦ Skill Gap Analyzer · v2.0")

# ── Compute ───────────────────────────────────────────────────────────────────
row = df[df["candidate_name"]==sel_c].iloc[0]
req = role_req_skills(df, sel_j, top_n)
matched, missing, score = skill_gap(row["skills_list"], req)
pct = round(score, 1)
job_cands = df[df["job_role"]==sel_j]
score_color = "#34d399" if pct>=70 else "#f59e0b" if pct>=40 else "#f87171"

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero">Skill Gap Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Candidate intelligence · Resume analysis · Role matching</div>', unsafe_allow_html=True)

# ── Profile card ──────────────────────────────────────────────────────────────
st.markdown(f"""<div class="glass"><div class="lbl">👤 Candidate Profile</div>
<div class="grid4">
  <div class="chip"><div class="k">ID</div><div class="v">#{row["candidate_id"]}</div></div>
  <div class="chip"><div class="k">Name</div><div class="v">{row["candidate_name"]}</div></div>
  <div class="chip"><div class="k">Applied Role</div><div class="v">{row["job_role"]}</div></div>
  <div class="chip"><div class="k">Education</div><div class="v">{row["education"]}</div></div>
  <div class="chip"><div class="k">Experience</div><div class="v">{row["experience_years"]} yrs</div></div>
</div>
<div style="margin-top:1rem"><div class="lbl">Resume Skills</div>
<div class="pills">{"".join(f'<span class="pill pm">{s}</span>' for s in row["skills_list"])}</div>
</div></div>""", unsafe_allow_html=True)

# ── Score + Gap ───────────────────────────────────────────────────────────────
mp = "".join(f'<span class="pill pm">{s}</span>' for s in matched) or '<span style="color:rgba(255,255,255,0.3)">None</span>'
xp = "".join(f'<span class="pill px">{s}</span>' for s in missing) or '<span style="color:rgba(255,255,255,0.3)">All matched! 🎉</span>'
rp = "".join(f'<span class="pill pr">{s}</span>' for s in req)

c1, c2 = st.columns(2, gap="medium")
with c1:
    st.markdown(f"""<div class="glass"><div class="lbl">📊 Match Score · {sel_j}</div>
<span class="score-big" style="color:{score_color}">{pct}<span style="font-size:2rem;color:rgba(255,255,255,0.35)">%</span></span>
<div class="track"><div class="fill" style="width:{pct}%"></div></div>
<div style="display:flex;gap:0.8rem;margin-top:1.2rem;">
  <div class="chip"><div class="k">✅ Matched</div><div class="v" style="color:#6ee7b7">{len(matched)}</div></div>
  <div class="chip"><div class="k">❌ Missing</div><div class="v" style="color:#fca5a5">{len(missing)}</div></div>
  <div class="chip"><div class="k">🎯 Required</div><div class="v" style="color:#c7d2fe">{len(req)}</div></div>
</div>
<div style="margin-top:1rem"><div class="lbl">Required Skills</div><div class="pills">{rp}</div></div>
</div>""", unsafe_allow_html=True)

with c2:
    st.markdown(f"""<div class="glass"><div class="lbl">🔬 Gap Details · {sel_j}</div>
<div class="lbl" style="color:rgba(110,231,183,0.7)">✓ Matched</div><div class="pills">{mp}</div>
<div class="lbl" style="margin-top:1rem;color:rgba(252,165,165,0.7)">✗ Missing</div><div class="pills">{xp}</div>
</div>""", unsafe_allow_html=True)

# ── Charts ────────────────────────────────────────────────────────────────────
d1, d2 = st.columns(2, gap="medium")
with d1:
    st.markdown('<div class="glass"><div class="lbl">📊 Skill Coverage</div>', unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(5,3), dpi=120)
    ax.bar(["Matched","Missing"], [len(matched),len(missing)], color=["#34d399","#f87171"], width=0.45, zorder=3)
    for i,(v,c) in enumerate(zip([len(matched),len(missing)],["#34d399","#f87171"])):
        ax.text(i, v+0.05, str(v), ha="center", va="bottom", color=c, fontsize=13, fontweight="bold")
    ax.set_title("Matched vs Missing", fontsize=11, pad=8); ax.set_ylim(0, max(len(matched),len(missing),1)*1.4+1); ax.set_yticks([])
    style_ax(fig,ax); fig.tight_layout(); st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with d2:
    st.markdown('<div class="glass"><div class="lbl">📈 Experience Distribution</div>', unsafe_allow_html=True)
    fig2, ax2 = plt.subplots(figsize=(5,3), dpi=120)
    ax2.hist(job_cands["experience_years"], bins=15, color="#818cf8", zorder=3, edgecolor="#0d1b3e", linewidth=0.5)
    ax2.axvline(row["experience_years"], color="#f59e0b", linewidth=2, linestyle="--", label=f"This candidate ({row['experience_years']} yrs)")
    ax2.legend(fontsize=8, labelcolor="white", framealpha=0)
    ax2.set_xlabel("Years"); ax2.set_ylabel("Candidates"); ax2.set_title(sel_j, fontsize=10, pad=8)
    style_ax(fig2,ax2); fig2.tight_layout(); st.pyplot(fig2)
    st.markdown("</div>", unsafe_allow_html=True)

d3, d4 = st.columns(2, gap="medium")
with d3:
    st.markdown('<div class="glass"><div class="lbl">🛠 Top Skills in Role</div>', unsafe_allow_html=True)
    all_skills = [s for sl in job_cands["skills_list"] for s in sl]
    labels, counts = zip(*Counter(all_skills).most_common(10))
    fig3, ax3 = plt.subplots(figsize=(5,3.5), dpi=120)
    ax3.barh(labels[::-1], counts[::-1], color="#38bdf8", zorder=3, height=0.6, edgecolor="#0d1b3e", linewidth=0.4)
    ax3.set_title(f"Most Common · {sel_j}", fontsize=10, pad=8); ax3.set_xlabel("Frequency")
    ax3.grid(axis="x", color=(1,1,1,0.06), linewidth=0.7, linestyle="--")
    style_ax(fig3,ax3); fig3.tight_layout(); st.pyplot(fig3)
    st.markdown("</div>", unsafe_allow_html=True)

with d4:
    st.markdown('<div class="glass"><div class="lbl">🎓 Education Breakdown</div>', unsafe_allow_html=True)
    edu = job_cands["education"].value_counts()
    fig4, ax4 = plt.subplots(figsize=(5,3.5), dpi=120)
    ax4.pie(edu.values, labels=edu.index, autopct="%1.0f%%", startangle=140,
            colors=["#818cf8","#38bdf8","#34d399","#f59e0b","#f87171","#a78bfa","#fb923c"][:len(edu)],
            wedgeprops=dict(linewidth=0.5, edgecolor="#0d1b3e"), textprops=dict(color="white", fontsize=8))
    ax4.set_title(f"Education · {sel_j}", fontsize=10, pad=8, color="white")
    fig4.patch.set_alpha(0); fig4.tight_layout(); st.pyplot(fig4)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Top candidates ────────────────────────────────────────────────────────────
st.markdown(f'<div class="glass"><div class="lbl">🏆 Top Candidates · {sel_j}</div>', unsafe_allow_html=True)
top = sorted([(r["candidate_name"], r["education"], r["experience_years"], round(skill_gap(r["skills_list"],req)[2],1))
              for _,r in job_cands.iterrows()], key=lambda x: x[3], reverse=True)
top_df = pd.DataFrame(top[:10], columns=["Candidate","Education","Experience (yrs)","Match %"])
st.dataframe(top_df.style.background_gradient(subset=["Match %"], cmap="Purples"), use_container_width=True, hide_index=True)
st.markdown("</div>", unsafe_allow_html=True)

with st.expander("📂 Dataset Preview"):
    st.dataframe(df.drop(columns=["skills_list"]).head(30), use_container_width=True, hide_index=True)