import os
import random
import time
from PIL import Image

# Configuration
SOURCE_DIR = 'scripts/source_images'
OUTPUT_IMG_DIR = 'content/img'
OUTPUT_SQL_FILE = 'content/seed_users.sql'
GRID_COLS = 5
GRID_ROWS = 2
IMG_SIZE = 96

# Mock Data
BIO_TEMPLATES = [
    "Looking for my soulmate.",
    "Love to travel and dance.",
    "Music is my life.",
    "Just a simple person.",
    "WAP enthusiast.",
    "Let's chat!",
    "Coffee lover.",
    "Dream big.",
    "Carpe Diem.",
    "Looking for fun."
]

def generate_users():
    users = []
    
    # Process Images
    image_files = sorted([f for f in os.listdir(SOURCE_DIR) if f.endswith('.png')])
    
    user_id_counter = 1
    # Start after existing 5 users (ids 1-5)
    user_id_counter = 6 
    
    sql_statements = []
    sql_statements.append("DELETE FROM users WHERE id > 5;")
    sql_statements.append("DELETE FROM user_photos WHERE user_id > 5;")
    
    for img_file in image_files:
        is_female = 'female' in img_file
        gender = 'F' if is_female else 'M'
        
        img_path = os.path.join(SOURCE_DIR, img_file)
        try:
            img = Image.open(img_path)
            width, height = img.size
            cell_width = width // GRID_COLS
            cell_height = height // GRID_ROWS
            
            for row in range(GRID_ROWS):
                for col in range(GRID_COLS):
                    # Crop
                    left = col * cell_width
                    top = row * cell_height
                    right = left + cell_width
                    bottom = top + cell_height
                    
                    crop = img.crop((left, top, right, bottom))
                    
                    # Resize to 96x96
                    crop = crop.resize((IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
                    
                    # Save
                    filename = f"user_{user_id_counter}.jpg"
                    save_path = os.path.join(OUTPUT_IMG_DIR, filename)
                    crop.save(save_path, "JPEG", quality=80)
                    
                    # Generate User Data
                    username = f"user{user_id_counter}"
                    password = "5f4dcc3b5aa765d61d8327deb882cf99" # md5('password')
                    age = random.randint(18, 35)
                    bio = random.choice(BIO_TEMPLATES).replace("'", "\\'")
                    now = int(time.time())
                    last_active = now - random.randint(0, 86400)
                    
                    # SQL
                    sql = f"INSERT INTO users (id, username, password, age, gender, bio, last_active, created_at) VALUES ({user_id_counter}, '{username}', '{password}', {age}, '{gender}', '{bio}', {last_active}, {now});"
                    sql_statements.append(sql)
                    
                    sql_photo = f"INSERT INTO user_photos (user_id, filename, is_primary) VALUES ({user_id_counter}, '{filename}', 1);"
                    sql_statements.append(sql_photo)
                    
                    user_id_counter += 1
                    
        except Exception as e:
            print(f"Error processing {img_file}: {e}")

    # Write SQL
    with open(OUTPUT_SQL_FILE, 'w') as f:
        f.write("\n".join(sql_statements))
    
    print(f"Generated {user_id_counter - 6} users. SQL saved to {OUTPUT_SQL_FILE}")

if __name__ == "__main__":
    if not os.path.exists(OUTPUT_IMG_DIR):
        os.makedirs(OUTPUT_IMG_DIR)
    generate_users()
