### File that will execute all the query locally

import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="db",
    database="captini",
    user="django",
    password="django",
    port="5432"
)

cursor = conn.cursor()
### These queries are used to remove all the data so we will not have conflict with the id
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
cursor.execute("DELETE FROM account_user;")
conn.commit()
with open('captini.sql', encoding='utf-8') as file:
    for line in file:
        cursor.execute(line)                    
        conn.commit()
cursor.execute("DELETE FROM captini_exampletaskrecording;")
conn.commit()
with open('audio.sql', encoding='utf-8') as file:
    for line in file:
        cursor.execute(line)
        conn.commit()
cursor.close()
conn.close()
