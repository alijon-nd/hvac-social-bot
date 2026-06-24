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
    print(f"📊 Already posted: {len(posted)} images")

    images = list_images_in_folder()
    if not images:
        print("📭 No images in bucket. Exiting.")
        return

    # Filter images already posted
    new_images = [img for img in images if img['name'] not in posted]
    if not new_images:
        print("✅ No new images to post. Exiting.")
        return

    # Pick one random image
    chosen = random.choice(new_images)
    blob = chosen['blob']
    filename = chosen['name']
    print(f"🖼️ Processing: {filename}")

    # Download image
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        original_path = tmp.name
    download_image(blob, original_path)

    # Overlay logo
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
        branded_path = tmp.name
    overlay_logo(original_path, LOGO_PATH, branded_path)

    # Generate captions with history
    desc = get_photo_description(filename)
    captions = generate_captions(desc, history)
    fb_cap = captions["facebook"]
    ig_cap = captions["instagram"]

    print(f"📝 FB: {fb_cap[:100]}...")
    print(f"📝 IG: {ig_cap[:100]}...")

    # Post
    try:
        if not DRY_RUN:
            fb_result = post_to_facebook(branded_path, fb_cap)
            print(f"✅ Facebook post ID: {fb_result.get('id')}")

            ig_result = post_to_instagram(branded_path, ig_cap)
            print(f"✅ Instagram post ID: {ig_result.get('id')}")
        else:
            print("🔍 DRY RUN - skipping actual posting")

        # Mark as posted
        posted.append(filename)
        save_posted_log(posted)

        # Update caption history
        history.append(fb_cap)
        history.append(ig_cap)
        save_history(history)

        # Optional: Delete from bucket after success
        # delete_image(blob)
        # print(f"🗑️ Deleted {filename} from bucket")

    except Exception as e:
        print(f"❌ Failed to post: {e}")

    # Cleanup temp files
    os.unlink(original_path)
    os.unlink(branded_path)
    print("✨ Done.")

if __name__ == "__main__":
    main()