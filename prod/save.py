import psycopg2
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
# Establish a connection to the PostgreSQL database
# Add the correct connection parameters
conn = psycopg2.connect(
    host=os.environ.get("DATABASE_HOST", ""),
    database=os.environ.get("DATABASE_NAME", ""),
    user= os.environ.get("DATABASE_USER", ""),
    password=os.environ.get("DATABASE_PASSWORD", ""),
    port=os.environ.get("DATABASE_PORT", ""),
)
cursor = conn.cursor()
### These queries are used to remove all the data so we will 

cursor.execute("DELETE FROM captini_exampletaskrecording;")
conn.commit()
cursor.execute("DELETE FROM captini_usertaskrecording;")
conn.commit()
cursor.execute("DELETE FROM captini_usertaskscorestats;")
conn.commit()
cursor.execute("DELETE FROM captini_task;")
conn.commit()
cursor.execute("DELETE FROM captini_prompt;")
conn.commit()
cursor.execute("DELETE FROM captini_lesson;")
conn.commit()
cursor.execute("DELETE FROM captini_topic;")
conn.commit()
with open('data.sql', encoding='utf-8') as file:
    for line in file:
        cursor.execute(line)
        conn.commit()
with open('audio.sql', encoding='utf-8') as file:
    for line in file:
        cursor.execute(line)
        conn.commit()
cursor.close()
conn.close()
