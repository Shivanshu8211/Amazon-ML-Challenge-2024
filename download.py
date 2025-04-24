import pandas as pd
import requests
import os

# Load the Excel file
file_path = 'train.csv'  # Replace with your Excel file path
df = pd.read_csv(file_path)

# Create a directory to save images
os.makedirs('downloaded_images', exist_ok=True)

# Iterate through the DataFrame and download images
c=0
for index, row in df.iterrows():
    image_url = row['image_link']
    image_name = os.path.basename(image_url)  # Extract the image file name from the URL
    image_path = os.path.join('downloaded_images', image_name)
    c+=1
    # Download the image
    try:
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an error for bad responses
        with open(image_path, 'wb') as file:
            file.write(response.content)
        print(f'Downloaded: {image_name}')
    except requests.exceptions.RequestException as e:
        print(f'Failed to download {image_name}: {e}')
    if c>1000:
        break