import streamlit as st, requests, pandas as pd

st.set_page_config(page_title="Job Finder", layout="wide")
st.title("🌐 Advanced Job Finder")

query = st.text_input("Enter job title / skills / location", "python developer Bengaluru")

if st.button("Search"):
    headers = {"X-API-KEY": st.secrets["SERPER_KEY"]}
    body = {
        "q": f"site:(naukri.com OR indeed.co.in OR foundit.in OR linkedin.com/jobs OR weworkremotely.com OR remotive.io OR upwork.com OR freelancer.in OR glassdoor.co.in OR shine.com OR timesjobs.com) {query}",
        "num": 20,
        "gl": "in",
    }
    r = requests.post("https://google.serper.dev/search", headers=headers, json=body)
    data = r.json().get("organic", [])
    if not data:
        st.warning("No jobs found or API limit reached.")
    else:
        jobs = [{"Title": d["title"], "Link": d["link"], "Snippet": d.get("snippet","")} for d in data]
        df = pd.DataFrame(jobs)
        st.dataframe(df, use_container_width=True)
        st.download_button("📥 Download CSV", df.to_csv(index=False), "jobs.csv", "text/csv")
