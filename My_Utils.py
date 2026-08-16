import requests
import numpy as np
from datetime import datetime
from collections import defaultdict


# Safe API call
def safe(url):
    try:
        r = requests.get(url, timeout=10).json()
        return r["result"] if r.get("status") == "OK" else None
    except Exception:
        return None


# Fetch submissions
def get_submissions(user):
    return safe(f"https://codeforces.com/api/user.status?handle={user}")


# Fetch rating history
def get_ratings(user):
    return safe(f"https://codeforces.com/api/user.rating?handle={user}")


# Extract features from submissions
def extract(subs, cutoff):
    subs = [
        s for s in subs
        if cutoff - 60 * 86400 <= s["creationTimeSeconds"] <= cutoff
    ]

    if len(subs) < 20:
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


# Rating trend (last 5 contests)
def trend(r):
    if len(r) < 5:
        return 0

    dif = [
        r[i]["newRating"] - r[i - 1]["newRating"]
        for i in range(1, len(r))
    ]

    return np.mean(dif[-5:])


# Rating volatility
def volatility(r):
    if len(r) < 5:
        return 0

    dif = [
        r[i]["newRating"] - r[i - 1]["newRating"]
        for i in range(1, len(r))
    ]

    return np.std(dif[-5:])


# Main feature extraction function
def get_features(user):
    subs = get_submissions(user)
    ratings = get_ratings(user)

    if not subs or not ratings:
        return None

    cutoff = ratings[-1]["ratingUpdateTimeSeconds"]
    features = extract(subs, cutoff)

    if not features:
        return None

    current_rating = ratings[-1]["newRating"]

    features.update({
        "current": current_rating,
        "trend": trend(ratings),
        "vol": volatility(ratings),
        "contest_count": len(ratings),
        "recent": len(ratings[-5:]),
        "gap": features["avg_rating"] - current_rating,
        "activity": features["problems"] * features["consistency"]
    })

    return features


# Optional test run
if __name__ == "__main__":
    user = input("Enter Codeforces handle: ")
    result = get_features(user)

    if result:
        print("\nExtracted Features:\n")
        for k, v in result.items():
            print(f"{k}: {v}")
    else:
        print("Not enough data or invalid user.")