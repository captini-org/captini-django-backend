### File that will execute all the query locally

import psycopg2

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="captini",
    user="postgres",
    password="",
    port="5432"
)
cursor = conn.cursor()
cursor.execute("DELETE FROM captini_exampletaskrecording;")
conn.commit()
with open('audio.sql', encoding='utf-8') as file:
    for line in file:
        cursor.execute(line)
        conn.commit()
cursor.close()
conn.close()

