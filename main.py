from fetch import fetch_submissions
from db import connect, create_tables, save_submissions

handle = input("Codeforces handle: ").strip()
subs = fetch_submissions(handle)

conn = connect()
create_tables(conn)
save_submissions(conn, subs)

count = conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
print("Submissions in database:", count)
conn.close()