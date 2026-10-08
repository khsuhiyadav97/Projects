import time

HALF_LIFE_DAYS = 60   # how fast old attempts fade
K = 5                 # how strongly small samples are pulled toward average


def weakness_scores(conn):
    now = time.time()

    prior = conn.execute(
        "SELECT AVG(verdict != 'OK') FROM submissions WHERE verdict IS NOT NULL"
    ).fetchone()[0]
    if prior is None:
        return []

    rows = conn.execute("""
        SELECT t.tag, s.verdict, s.time
        FROM submissions s
        JOIN submission_tags t ON t.submission_id = s.id
        WHERE s.verdict IS NOT NULL
    """).fetchall()

    totals = {}   # tag -> [weighted_fails, weighted_total, raw_count]
    for tag, verdict, ts in rows:
        age_days = max(0, (now - ts) / 86400)
        weight = 0.5 ** (age_days / HALF_LIFE_DAYS)
        entry = totals.setdefault(tag, [0.0, 0.0, 0])
        entry[1] += weight
        entry[2] += 1
        if verdict != "OK":
            entry[0] += weight

    scores = []
    for tag, (fails, total, count) in totals.items():
        score = (fails + K * prior) / (total + K)
        scores.append((tag, score, count))

    return sorted(scores, key=lambda x: x[1], reverse=True)