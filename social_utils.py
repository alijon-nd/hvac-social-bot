import requests
from config import FACEBOOK_PAGE_ID, FACEBOOK_ACCESS_TOKEN, INSTAGRAM_BUSINESS_ACCOUNT_ID, DRY_RUN

GRAPH_API_URL = "https://graph.facebook.com/v18.0"

def post_to_facebook(image_path, caption):
    """Post to Facebook Page."""
    if DRY_RUN:
        print(f"[DRY RUN] Facebook:\n{caption}\n")
        return {"id": "dryrun"}

    if not FACEBOOK_ACCESS_TOKEN or FACEBOOK_ACCESS_TOKEN == "your_token":
        print("[ERROR] Facebook token not configured.")
        return {"error": "no token"}

    url = f"{GRAPH_API_URL}/{FACEBOOK_PAGE_ID}/photos"
    files = {"source": open(image_path, "rb")}
    data = {
        "caption": caption,
        "access_token": FACEBOOK_ACCESS_TOKEN,
        "published": True
    }
    resp = requests.post(url, files=files, data=data)
    resp.raise_for_status()
    return resp.json()

def post_to_instagram(image_path, caption):
    """Post to Instagram Business Account."""
    if DRY_RUN:
        print(f"[DRY RUN] Instagram:\n{caption}\n")
        return {"id": "dryrun"}

    if not FACEBOOK_ACCESS_TOKEN or FACEBOOK_ACCESS_TOKEN == "your_token":
        print("[ERROR] Meta token not configured.")
        return {"error": "no token"}

    # Step 1: Create container
    create_url = f"{GRAPH_API_URL}/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media"
    files = {"image": open(image_path, "rb")}
    data = {
        "caption": caption,
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    resp = requests.post(create_url, files=files, data=data)
    resp.raise_for_status()
    creation_id = resp.json().get("id")

    # Step 2: Publish
    publish_url = f"{GRAPH_API_URL}/{INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish"
    publish_data = {
        "creation_id": creation_id,
        "access_token": FACEBOOK_ACCESS_TOKEN
    }
    pub_resp = requests.post(publish_url, data=publish_data)
    pub_resp.raise_for_status()
    return pub_resp.json()