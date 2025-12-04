from PIL import Image
import os

# Configuration
INPUT_PATH = 'content/img/logo.png'
OUTPUT_PATH = 'content/img/logo.jpg'
TARGET_SIZE = (20, 20)
QUALITY = 30 # Low quality for "of the time" look

def process_logo():
    if not os.path.exists(INPUT_PATH):
        print(f"Error: {INPUT_PATH} not found.")
        return

    try:
        # Open image
        img = Image.open(INPUT_PATH)
        
        # Convert to RGB (remove transparency, replace with white)
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
        
        # Resize
        resized = bg.resize(TARGET_SIZE, Image.Resampling.NEAREST) # Nearest neighbor for pixel art look
        
        # Save as JPG
        resized.save(OUTPUT_PATH, "JPEG", quality=QUALITY)
        print(f"Saved processed logo to {OUTPUT_PATH}")
        
    except Exception as e:
        print(f"Error processing logo: {e}")

if __name__ == "__main__":
    process_logo()
