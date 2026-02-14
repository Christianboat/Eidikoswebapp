import os
import secrets
from PIL import Image
from flask import current_app, url_for
import re

def slugify(s):
    """
    Converts a string to a URL-safe slug.
    """
    s = s.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[\s_-]+', '-', s)
    s = re.sub(r'^-+|-+$', '', s)
    return s

def save_picture(form_picture, folder=''):
    """
    Saves an uploaded picture to the static/uploads directory.
    If 'folder' is provided, it saves to static/uploads/folder.
    Returns the filename.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    
    # Ensure directory exists
    upload_path = os.path.join(current_app.root_path, 'static', 'uploads', folder)
    os.makedirs(upload_path, exist_ok=True)
    
    picture_path = os.path.join(upload_path, picture_fn)

    # Optional: Resize image if needed (using Pillow)
    # output_size = (800, 800)
    # i = Image.open(form_picture)
    # i.thumbnail(output_size)
    # i.save(picture_path)
    
    # Just save for now without resizing to preserve quality/animations
    form_picture.save(picture_path)

    return picture_fn

def get_image_url(filename, folder=''):
    """Returns the URL for the image."""
    if not filename:
        return None
        
    path = f'uploads/{folder}/{filename}' if folder else f'uploads/{filename}'
    return url_for('static', filename=path)

def get_video_embed_url(url):
    """
    Extracts the video ID from a URL and returns the embed URL.
    Supports:
    - YouTube: youtube.com/watch?v=ID, youtu.be/ID, youtube.com/embed/ID, youtube.com/shorts/ID
    - Google Drive: drive.google.com/file/d/ID/view, drive.google.com/open?id=ID
    """
    if not url:
        return None
    
    # Check if it's a Google Drive URL
    if 'drive.google.com' in url:
        # Extract file ID from various Google Drive URL formats
        drive_regex = r'drive\.google\.com\/(?:file\/d\/|open\?id=)([-a-zA-Z0-9_]+)'
        match = re.search(drive_regex, url)
        if match:
            file_id = match.group(1)
            return f"https://drive.google.com/file/d/{file_id}/preview"
    
    # Check if it's a YouTube URL
    if 'youtube.com' in url or 'youtu.be' in url:
        # Regex to catch video ID from various YouTube URL formats
        youtube_regex = r'(?:v=|\/|embed\/|shorts\/)([0-9A-Za-z_-]{11})'
        match = re.search(youtube_regex, url)
        if match:
            video_id = match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
        
    return url # Return original if no match (fallback)
