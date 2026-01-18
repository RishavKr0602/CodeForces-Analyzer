# CodeForces-Analyzer
Made to Analyze the Performance of the Programmers on the Website.
import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

st.set_page_config(page_title="Codeforces Profile Analyzer", layout="wide")

# -----------------------------
# API Functions
# -----------------------------
def get_user_info(username):
    return requests.get(
        f"https://codeforces.com/api/user.info?handles={username}"
    ).json()

def get_rating_history(username):
    return requests.get(
        f"https://codeforces.com/api/user.rating?handle={username}"
    ).json()["result"]

def get_submissions(username):
    return requests.get(
        f"https://codeforces.com/api/user.status?handle={username}"
    ).json()["result"]

# -----------------------------
# Analyze Submissions
# -----------------------------
def analyze_submissions(submissions):
    solved = set()
    tag_count = defaultdict(int)
    for sub in submissions:
        if sub["verdict"] == "OK":
            prob = sub["problem"]
            pid = (prob["contestId"], prob["index"])
            if pid not in solved:
                solved.add(pid)
                for tag in prob["tags"]:
                    tag_count[tag] += 1
    return len(solved), dict(tag_count)

# -----------------------------
# UI
# -----------------------------
st.title("📊 Codeforces Profile Analyzer")
st.write("Compare two Codeforces users with tag-based problem analysis")

c1, c2 = st.columns(2)
user1 = c1.text_input("First Username")
user2 = c2.text_input("Second Username")

if st.button("Compare Profiles"):
    if not user1 or not user2:
        st.warning("Please enter both usernames")
    else:
        with st.spinner("Fetching data..."):
            u1_info = get_user_info(user1)
            u2_info = get_user_info(user2)
        if u1_info["status"] != "OK" or u2_info["status"] != "OK":
            st.error("Invalid username(s)")
        else:
            u1 = u1_info["result"][0]
            u2 = u2_info["result"][0]
            r1 = get_rating_history(user1)
            r2 = get_rating_history(user2)
            s1 = get_submissions(user1)
            s2 = get_submissions(user2)
            solved1, tags1 = analyze_submissions(s1)
            solved2, tags2 = analyze_submissions(s2)
            # -----------------------------
            # Summary Table
            # -----------------------------
            st.subheader("📌 Profile Comparison")
            df = pd.DataFrame({
                user1: [
                    u1.get("rating", "Unrated"),
                    u1.get("maxRating", "N/A"),
                    u1.get("rank", "N/A"),
                    len(r1),
                    solved1
                ],
                user2: [
                    u2.get("rating", "Unrated"),
                    u2.get("maxRating", "N/A"),
                    u2.get("rank", "N/A"),
                    len(r2),
                    solved2
                ]
            }, index=[
                "Current Rating",
                "Max Rating",
                "Rank",
                "Contests",
                "Problems Solved"
            ])
            st.table(df)
            # -----------------------------
            # Rating Graph
            # -----------------------------
            st.subheader("📈 Rating Progress Comparison")
            fig, ax = plt.subplots()
            ax.plot([x["newRating"] for x in r1], label=user1)
            ax.plot([x["newRating"] for x in r2], label=user2)
            ax.set_xlabel("Contest Number")
            ax.set_ylabel("Rating")
            ax.legend()
            ax.grid()
            st.pyplot(fig)
            # -----------------------------
            # TAG ANALYSIS
            # -----------------------------
            st.subheader("🏷️ Problems Solved by Tags")
            col1, col2 = st.columns(2)
            # User 1 Tags
            top_tags1 = dict(sorted(tags1.items(), key=lambda x: x[1], reverse=True)[:10])
            col1.write(f"**Top Tags – {user1}**")
            fig1, ax1 = plt.subplots()
            ax1.bar(top_tags1.keys(), top_tags1.values())
            ax1.set_xticklabels(top_tags1.keys(), rotation=45, ha="right")
            ax1.set_ylabel("Problems Solved")
            col1.pyplot(fig1)
            # User 2 Tags
            top_tags2 = dict(sorted(tags2.items(), key=lambda x: x[1], reverse=True)[:10])
            col2.write(f"**Top Tags – {user2}**")
            fig2, ax2 = plt.subplots()
            ax2.bar(top_tags2.keys(), top_tags2.values())
            ax2.set_xticklabels(top_tags2.keys(), rotation=45, ha="right")
            ax2.set_ylabel("Problems Solved")
            col2.pyplot(fig2)
            st.success("Tag-based comparison completed 🎉")
