import os
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


try:
    # Connect using the full string
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    print("✅ Connected to Neon Postgres!")

    df = pd.read_csv('../spring_26_courses.csv')
    print(df.head())


    
    cur.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed:", e)


