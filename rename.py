import pandas as pd

file_path = "./reports/face_data.csv"
df = pd.read_csv(file_path)

df['video'] = df['video'].str.replace('.mp4', '', regex=False)  
df['video'] = 'https://fgimagestorage.blob.core.windows.net/facebook-assets/' + df['video']  

output_file_path = "./reports/updated_face_data.csv" 
df.to_csv(output_file_path, index=False)

print(f"Updated CSV saved to {output_file_path}")
