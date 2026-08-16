import pandas as pd
import requests
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from collections import defaultdict


# ---------------- API ----------------
def safe(url):
    try:
        r = requests.get(url, timeout=10).json()
        return r["result"] if r.get("status") == "OK" else None
    except Exception:
        return None


def get_submissions(user):
    return safe(f"https://codeforces.com/api/user.status?handle={user}")


def get_ratings(user):
    return safe(f"https://codeforces.com/api/user.rating?handle={user}")


# ---------------- FEATURE ----------------
def extract(subs, cutoff):
    subs = [
        s for s in subs
        if cutoff - 60 * 86400 <= s["creationTimeSeconds"] <= cutoff
    ]

    if len(subs) < 25:
        return None

    days = set()
    ratings = []
    tags = defaultdict(int)

    for s in subs:
        days.add(datetime.fromtimestamp(s["creationTimeSeconds"]).date())
        p = s["problem"]

        if "rating" in p:
            ratings.append(p["rating"])

        for t in p.get("tags", []):
            tags[t] += 1

    avg = np.mean(ratings) if ratings else 0

    return {
        "problems": len(subs),
        "active_days": len(days),
        "consistency": len(days) / 60,
        "ppd": len(subs) / 60,
        "avg_rating": avg,
        "max_rating": max(ratings) if ratings else 0,
        "std_rating": np.std(ratings) if ratings else 0,
        "tag_dp": tags["dp"],
        "tag_graph": tags["graphs"],
        "tag_greedy": tags["greedy"],
        "tag_math": tags["math"],
        "tag_div": len(tags),
        "tag_counts": dict(tags)
    }


def trend(r):
    if len(r) < 5:
        return 0
    dif = [r[i]["newRating"] - r[i - 1]["newRating"] for i in range(1, len(r))]
    return np.mean(dif[-5:])


def vol(r):
    if len(r) < 5:
        return 0
    dif = [r[i]["newRating"] - r[i - 1]["newRating"] for i in range(1, len(r))]
    return np.std(dif[-5:])


# ---------------- PROCESS USER ----------------
def process_user(user):
    subs = get_submissions(user)
    ratings = get_ratings(user)

    if not subs or not ratings:
        return []

    rows = []

    for i in range(5, len(ratings) - 3):

        feat = extract(subs, ratings[i]["ratingUpdateTimeSeconds"])
        if not feat:
            continue

        if feat["active_days"] < 10:
            continue

        cur = ratings[i]["newRating"]

        feat.update({
            "current": cur,
            "trend": trend(ratings[:i]),
            "vol": vol(ratings[:i]),
            "contest_count": i,
            "recent": len(ratings[max(0, i - 5):i]),
            "gap": feat["avg_rating"] - cur,
            "activity": feat["problems"] * feat["consistency"]
        })

        # 🔥 Smooth target (important for ML stability)
        future = [ratings[i + j]["newRating"] for j in range(1, 4)]
        target = np.mean(future) - cur

        # Remove outliers
        if abs(target) > 200:
            continue

        feat["target"] = target / 100

        # Remove non-numeric column
        feat.pop("tag_counts", None)

        rows.append(feat)

    return rows


# ---------------- MAIN ----------------
def main():
    print("🚀 STEP 1: Fetch users")

    try:
        users = requests.get(
            "https://codeforces.com/api/user.ratedList?activeOnly=true",
            timeout=15
        ).json()["result"]
    except Exception:
        print("❌ Failed to fetch users")
        return

    handles = [
        u["handle"]
        for u in users
        if 1300 <= u.get("rating", 0) <= 2400
    ][:500]

    print(f"✅ Users fetched: {len(handles)}")

    print("🚀 STEP 2: Building dataset (parallel)")

    data = []
    done = 0

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(process_user, u) for u in handles]

        for f in as_completed(futures):
            try:
                res = f.result()
                data.extend(res)
            except Exception:
                continue

            done += 1
            if done % 20 == 0:
                print(f"⏳ Processed {done}/{len(handles)} users")

    print("🚀 STEP 3: Cleaning dataset")

    df = pd.DataFrame(data)
    df = df.drop_duplicates()

    print(f"✅ Final dataset size: {len(df)}")

    df.to_csv("cf_training_data.csv", index=False)

    print("🎉 DATASET READY → cf_training_data.csv")


# ---------------- RUN ----------------
if __name__ == "__main__":
    main()