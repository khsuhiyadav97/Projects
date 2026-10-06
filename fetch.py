import re
import requests

API_URL = "https://codeforces.com/api/user.status"


def is_valid_handle(handle):
    """Codeforces handles use letters, digits, and _ . - only."""
    return bool(re.fullmatch(r"[A-Za-z0-9_.-]{3,24}", handle))


def fetch_submissions(handle, count=50):
    if not is_valid_handle(handle):
        raise ValueError("That doesn't look like a valid Codeforces handle.")

    params = {"handle": handle, "from": 1, "count": count}
    try:
        response = requests.get(API_URL, params=params, timeout=10)
        data = response.json()
    except (requests.RequestException, ValueError):
        raise RuntimeError("Couldn't reach Codeforces. Check your internet and try again.")

    if data.get("status") != "OK":
        raise ValueError(data.get("comment", "Codeforces returned an error."))

    return [keep_needed_fields(sub) for sub in data["result"]]


def keep_needed_fields(sub):
    """Keep only what the analysis needs."""
    problem = sub["problem"]
    return {
        "id": sub["id"],
        "time": sub["creationTimeSeconds"],
        "verdict": sub.get("verdict"),
        "problem": f'{problem["contestId"]}{problem["index"]}',
        "name": problem["name"],
        "rating": problem.get("rating"),
        "tags": problem.get("tags", []),
    }


if __name__ == "__main__":
    handle = input("Codeforces handle: ").strip()
    try:
        submissions = fetch_submissions(handle)
    except (ValueError, RuntimeError) as error:
        print("Error:", error)
    else:
        print("Fetched:", len(submissions))
        if submissions:
            print(submissions[0])