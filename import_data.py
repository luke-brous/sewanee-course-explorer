import pandas as pd
import re
import psycopg2
import os
from dotenv import load_dotenv

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
    df = pd.read_csv(course_file)
    
    df['description'] = df['description'].apply(clean_html_tags).fillna("No description available.")
    df['times'] = df['times'].apply(clean_times)
    
    df['cat_term_str'] = df['cat_term'].astype(str)
    df['year'] = df['cat_term_str'].str[:4].astype(int)
    
    term_map = {'10': 'Fall', '20': 'Spring', '30': 'Summer'}
    df['term_code'] = df['cat_term_str'].str[-2:]
    df['term'] = df['term_code'].map(term_map)
    
    # Use r'(\d+)' to avoid the SyntaxWarning
    df['credits_int'] = df['hours'].astype(str).str.extract(r'(\d+)').fillna(0).astype(int)

    return df

def upload_to_neon(df):
    sql = """
    INSERT INTO "Course" (
        id, uid, crn, title, level, section, term, year, 
        credits, "meetingTime", faculty, location, "limit", 
        enrolled, description, major, subject
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT ON CONSTRAINT unique_class DO UPDATE SET
        title = EXCLUDED.title,
        faculty = EXCLUDED.faculty,
        "meetingTime" = EXCLUDED."meetingTime";
    """
    
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                print("Starting upload...")
                for _, row in df.iterrows():
                    # Mapping exactly to YOUR CSV headers
                    data = (
                        f"cuid_{row['crn']}_{row['cat_term']}", # Unique ID
                        row['uid'],
                        int(row['crn']),
                        row['title'],
                        str(row['num']),      # level
                        row['section'],
                        row['term'],          # From our mapping
                        row['year'],          # From our mapping
                        int(row['credits_int']),
                        row['times'],         # meetingTime
                        row['faculty'],       # Was 'instructor'
                        row['location'] if pd.notna(row['location']) else "TBA", # Was 'where'
                        int(row['limit']),     # Was 'lim'
                        int(row['enrolled']),  # Was 'enr'
                        row['description'],
                        row['subj'],          # major (e.g. ENGL)
                        row['subject']        # subject (e.g. African Studies)
                    )
                    cur.execute(sql, data)
                
                conn.commit()
                print(f"Successfully uploaded {len(df)} courses to Neon.")
                
    except Exception as e:
        print(f"❌ Database error: {e}")

if __name__ == "__main__":
    try:
        course_file = 'data/spring_26_courses.csv'
        cleaned_df = get_cleaned_df(course_file)
        upload_to_neon(cleaned_df)
    except Exception as e:
        print(f"An error occurred: {e}")