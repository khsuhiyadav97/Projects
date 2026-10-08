def topic_stats(conn, min_submissions=5):
    query = """
        SELECT
            t.tag,
            COUNT(*)                                   AS submissions,
            SUM(s.verdict = 'OK')                      AS accepted,
            COUNT(DISTINCT s.problem)                  AS problems_tried,
            COUNT(DISTINCT CASE WHEN s.verdict = 'OK'
                                THEN s.problem END)    AS problems_solved
        FROM submissions s
        JOIN submission_tags t ON t.submission_id = s.id
        GROUP BY t.tag
        HAVING COUNT(*) >= ?
        ORDER BY (SUM(s.verdict = 'OK') * 1.0 / COUNT(*)) ASC
    """
    return conn.execute(query, (min_submissions,)).fetchall()