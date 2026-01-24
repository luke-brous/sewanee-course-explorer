import pandas as pd
import re
import psycopg2
import os
from dotenv import load_dotenv # Standard way to import this

# 1. Load Environment Variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def clean_html_tags(text):
    if pd.isna(text): return text
    clean = re.compile('<.*?>')
    text = re.sub(clean, '', str(text))
    return " ".join(text.split())

def clean_times(text):
    if pd.isna(text): return text
    return str(text).replace(',', '').strip()

def get_cleaned_df(course_file):
    """This replaces your old cleanData function logic"""
    df = pd.read_csv(course_file)
    df = df.drop(columns=['available'], errors='ignore') 
    
    df['description'] = df['description'].apply(clean_html_tags).fillna("No description available.")
    df['times'] = df['times'].apply(clean_times)
    
    # Standardize column names for Postgres
    df.columns = [c.lower().replace(' ', '_') for c in df.columns]
    df = df.dropna(subset=['title'])
    
    print(f"Successfully cleaned {len(df)} courses.")
    return df

def upload_to_neon(df):
    """Handles the database connection and (eventually) the insert"""
    try:
        # Use the variable DATABASE_URL here, not the string "DATABASE_URL"
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        print("Successfully connected to the Neon database.")

        # NEXT STEP: We will add the logic to insert the rows here!

        cur.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    try:
        course_file = 'data/spring_26_courses.csv'
        
        # Step 1: Clean it
        cleaned_df = get_cleaned_df(course_file)
        
        # Step 2: Print preview to verify
        print(cleaned_df.head(5))
        
        # Step 3: Connect to DB
        upload_to_neon(cleaned_df)
        
    except Exception as e:
        print(f"An error occurred: {e}")