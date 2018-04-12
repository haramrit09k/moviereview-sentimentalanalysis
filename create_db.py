import sqlite3

db = "twit_data.db"

conn = sqlite3.connect(db)
c = conn.cursor()

try:
    c.execute("drop table twit_data")
except:
    # If nothing to drop, do nothing.
    pass

# Create tweet table
cmd = "CREATE TABLE twit_data (top_tweet TEXT, datetime TEXT)"
c.execute(cmd)

conn.commit()

conn.close()