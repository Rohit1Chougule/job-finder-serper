import streamlit as st, requests, pandas as pd

st.set_page_config(page_title="Data Analyst Jobs", layout="wide")
st.title("📊 Data Analyst — Latest Openings (Multi-Portal)")

# default title as requested
role = st.text_input("Role / Skills", "data analyst")
location = st.text_input("Location (city/country)", "Bengaluru")
mode = st.selectbox("Working Mode (optional)", ["", "remote", "onsite", "hybrid"])
exp = st.text_input("Experience keywords (optional)", "fresher OR 1-3 years OR junior")

# only these portals:
PORTALS = (
 "site:(naukri.com OR indeed.co.in OR glassdoor.co.in OR workindia.in OR apna.co OR foundit.in OR linkedin.com/jobs)"
)

# Helper: builds a search query that prefers recent/individual listings
def build_query():
    parts = [
        PORTALS,
        role,
        location,
        exp if exp.strip() else "",
        mode if mode.strip() else "",
        '"apply" OR "apply now"',
        '"posted today" OR "posted 1 day ago" OR "posted 2 days ago" OR "new"'
    ]
    return " ".join([p for p in parts if p]).strip()

q = build_query()
st.caption("Query sent to Serper/Google:")
st.code(q, language="text")

if st.button("🔎 Search latest"):
    headers = {"X-API-KEY": st.secrets["SERPER_KEY"]}
    body = {"q": q, "num": 20, "gl": "in"}  # gl=in to bias India; change if you want
    r = requests.post("https://google.serper.dev/search", headers=headers, json=body, timeout=45)
    data = r.json().get("organic", [])
    if not data:
        st.warning("No results (or API limit reached). Try changing location/filters.")
    else:
        rows = []
        for d in data:
            rows.append({
                "Title": d.get("title",""),
                "Link": d.get("link",""),
                "Snippet": d.get("snippet","")
            })
        df = pd.DataFrame(rows)
        st.success(f"Found {len(df)} results")
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button("📥 Download CSV", df.to_csv(index=False), "data-analyst-jobs.csv", "text/csv")
