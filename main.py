import os
import json
import tempfile
import random
from config import LOGO_PATH, POSTED_LOG, DRY_RUN
from storage_utils import list_images_in_folder, download_image
from image_utils import overlay_logo
from caption_utils import generate_captions, load_history, save_history, get_photo_description
from social_utils import post_to_facebook, post_to_instagram

def load_posted_log():
    if os.path.exists(POSTED_LOG):
        with open(POSTED_LOG, "r") as f:
            return json.load(f)
    return []

def save_posted_log(log):
    with open(POSTED_LOG, "w") as f:
        json.dump(log, f, indent=2)

def main():
    print("🚀 Starting HVAC Social Bot...")
    
    posted = load_posted_log()
    history = load_history()
    print(f"📊 Previously posted: {len(posted)} images")
    
    # Get images from Cloud Storage
    images = list_images_in_folder()
    if not images:
        print("📭 No images found in bucket")
        return
    
    # Filter new images
    new_images = [img for img in images if img['name'] not in posted]
    if not new_images:
        print("✅ No new images to post")
        return
    
    # Pick random image
    chosen = random.choice(new_images)
    blob = chosen['blob']
    filename = chosen['name']
    print(f"🖼️ Processing: {filename}")
    
    # Download
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        original_path = tmp.name
    download_image(blob, original_path)
    
    # Add logo
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        branded_path = tmp.name
    overlay_logo(original_path, LOGO_PATH, branded_path)
    
    # Generate captions
    desc = get_photo_description(filename)
    captions = generate_captions(desc, history)
    
    print(f"\n📝 FB: {captions['facebook'][:150]}...")
    print(f"\n📝 IG: {captions['instagram'][:150]}...")
    
    # Post
    try:
        if DRY_RUN:
            print("🔍 DRY RUN - skipping actual posting")
        else:
            fb_result = post_to_facebook(branded_path, captions['facebook'])
            print(f"✅ Facebook post ID: {fb_result.get('id')}")
            
            ig_result = post_to_instagram(branded_path, captions['instagram'])
            print(f"✅ Instagram post ID: {ig_result.get('id')}")
        
        # Mark as posted
        posted.append(filename)
        save_posted_log(posted)
        
        # Update history
        history.append(captions['facebook'])
        history.append(captions['instagram'])
        save_history(history)
        
        print("✨ Done!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Cleanup
    os.unlink(original_path)
    os.unlink(branded_path)



# Save captions to file
with open("last_captions.txt", "w") as f:
    f.write(f"FACEBOOK:\n{captions['facebook']}\n\n")
    f.write(f"INSTAGRAM:\n{captions['instagram']}\n")
print("📄 Captions saved to last_captions.txt")

if __name__ == "__main__":
    main()
