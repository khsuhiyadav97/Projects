from fetch import fetch_submissions
from db import connect, create_tables, save_submissions
from analysis import topic_stats

handle = input("Codeforces handle: ").strip()
subs = fetch_submissions(handle)

conn = connect()
create_tables(conn)
save_submissions(conn, subs)

count = conn.execute("SELECT COUNT(*) FROM submissions").fetchone()[0]
print("Submissions in database:", count)

print("\nTopic | submissions | accepted | success rate | solved/tried")
for tag, subs_count, accepted, tried, solved in topic_stats(conn):
    rate = accepted * 100 / subs_count
    print(f"{tag}: {subs_count} | {accepted} | {rate:.0f}% | {solved}/{tried}")

conn.close()
