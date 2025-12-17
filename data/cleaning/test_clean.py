# --- VERIFICATION CHECKS ---
import pandas as pd

df = pd.read_csv('../data/spring_26_courses.csv')


html_errors = df['info'].astype(str).str.contains('<br>|<|>', regex=True).sum()
assert html_errors == 0, f"Found {html_errors} rows with HTML tags!"



time_comma_errors = df['times'].astype(str).str.contains(',', regex=False).sum()
assert time_comma_errors == 0, f"Found {time_comma_errors} rows with commas in 'times'!"



assert 'available' not in df.columns, "The 'available' column was not dropped!"



assert df['title'].isnull().sum() == 0, "Found rows with missing titles!"
assert df['times'].isnull().sum() == 0, "Found rows with missing times!"





print("✅ All Data Quality Tests Passed!")