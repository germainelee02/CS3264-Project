import os
import urllib.request
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

# Set the search query and the number of images to download
query = "Marina Bay"
num_images = 20

# Configure Chrome webdriver options
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')

# Path to chromedriver executable on your system
chromedriver_path = "/path/to/chromedriver"

# Create a Service object
service = Service(chromedriver_path)

# Initialize the webdriver
driver = webdriver.Chrome(service=service, options=options)

# Navigate to Google Images
driver.get("https://www.google.com/imghp?hl=en")

# Find the search box and enter the query
search_box = driver.find_element(By.NAME, "q")
search_box.send_keys(query)
search_box.send_keys(Keys.RETURN)

# Scroll down to load more images
for i in range(10):
    driver.execute_script("window.scrollBy(0, 1000)")

# Find the image links and download the images
images = driver.find_elements(By.CSS_SELECTOR, ".rg_i")
image_urls = [image.get_attribute("src") for image in images]

# Create a folder to store the downloaded images
folder_name = query.replace(" ", "_")
os.makedirs(folder_name, exist_ok=True)

for i, url in enumerate(image_urls[:num_images]):
    try:
        # Download the image
        image_data = urllib.request.urlopen(url).read()
        image = Image.open(BytesIO(image_data))
        
        # Crop the image to 512x512 pixels
        image_width, image_height = image.size
        crop_size = min(image_width, image_height, 512)
        left = (image_width - crop_size) / 2
        top = (image_height - crop_size) / 2
        right = left + crop_size
        bottom = top + crop_size
        cropped_image = image.crop((left, top, right, bottom))
        cropped_image = cropped_image.resize((512, 512), Image.ANTIALIAS)

        # Save the image as a JPG file in the folder
        filename = f"{query}_{i+1}.jpg"
        save_path = os.path.join(folder_name, filename)
        cropped_image.save(save_path)
        print(f"Downloaded {save_path}")
    except Exception as e:
        print(f"Error downloading image {url}: {e}")

# Close the webdriver
driver.quit()
