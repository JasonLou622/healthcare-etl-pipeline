import pandas as pd

# Load raw dataset
file_path = '/Users/jasonlou/Documents/cs/git-github/healthcare-etl-pipeline/data/raw/appointments.csv'
df = pd.read_csv(file_path)

# Display basic structural info
print("Dataset Shape:", df.shape)
print("\nColumn Info:")
df.info()

print("\nFirst 5 rows:")
print(df.head())

