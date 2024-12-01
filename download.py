import os
import requests
import pandas as pd
from tqdm import tqdm

def download_videos_from_links(csv_file, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    df = pd.read_csv(csv_file)

    if 'Video URL' not in df.columns:
        print("CSV file must contain a column named 'url'.")
        return

    for index, row in df.iterrows():
        video_url = row['Video URL']
        try:
            file_name = video_url.split("/")[-1]
            output_path = os.path.join(output_folder, file_name)

            print(f"Downloading video: {video_url}")
            response = requests.get(video_url, stream=True)
            response.raise_for_status()  

            total_size = int(response.headers.get('content-length', 0))
            with open(output_path, 'wb') as file, tqdm(
                desc=file_name,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
                    bar.update(len(chunk))

            print(f"Downloaded: {output_path}")
        except Exception as e:
            print(f"Failed to download {video_url}: {e}")


import os

def add_mp4_extension(folder_path):

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path) and '.' not in file_name:
            new_file_path = file_path + '.mp4'
            os.rename(file_path, new_file_path)
            print(f"Renamed: {file_path} -> {new_file_path}")
        else:
            print(f"Skipped: {file_name} (already has an extension or not a file)")


csv_file = './data/processed/performance_data.csv'  
output_folder = 'downloaded_videos' 
download_videos_from_links(csv_file, output_folder)
add_mp4_extension(output_folder)