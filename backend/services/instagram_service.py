import os
import subprocess
from instaloader import Instaloader, Post

from typing import Dict, Any, Tuple
import tempfile

import re

def fetch_instagram_data(url: str) -> Tuple[str, Dict[str, Any]]:
    match = re.search(r'(?:reel|p)/([a-zA-Z0-9_-]+)', url)
    shortcode = match.group(1) if match else url.rstrip("/").split("/")[-1].split("?")[0]

    
    try:
        L = Instaloader()
        post = Post.from_shortcode(L.context, shortcode)
        
        views = post.video_view_count if post.is_video and post.video_view_count else 1000
        likes = post.likes
        comments = post.comments
        engagement_rate = ((likes + comments) / views * 100) if views > 0 else 0
        
        metadata = {
            "title": post.caption[:80] if post.caption else "Instagram Reel",
            "creator": post.owner_profile.username,
            "follower_count": post.owner_profile.followers,
            "views": views,
            "likes": likes,
            "comments": comments,
            "hashtags": post.caption_hashtags,
            "upload_date": post.date_utc.isoformat(),
            "duration": post.video_duration if post.is_video else 0,
            "engagement_rate": round(engagement_rate, 2),
            "thumbnail_url": post.url
        }
    except Exception:
        metadata = {
            "title": "Instagram Reel (Anti-Scraping Blocked)",
            "creator": "Private/Blocked Account",
            "follower_count": 0,
            "views": 0,
            "likes": 0,
            "comments": 0,
            "hashtags": ["blocked", "private"],
            "upload_date": "2024-01-01T00:00:00Z",
            "duration": 60,
            "engagement_rate": 0.0,
            "thumbnail_url": "https://via.placeholder.com/300x450/111111/ffffff?text=Instagram+Reel"
        }

    transcript_text = "Transcript unavailable."
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = os.path.join(tmpdir, "audio.mp3")
            subprocess.run([
                "yt-dlp", "-x", "--audio-format", "mp3",
                "-o", audio_path, url
            ], check=True, capture_output=True)
            
            if os.path.exists(audio_path):
                from faster_whisper import WhisperModel
                model = WhisperModel("tiny", device="cpu", compute_type="int8")
                segments, _ = model.transcribe(audio_path)
                transcript_text = " ".join([segment.text for segment in segments])
    except Exception as e:
        pass
        
    return transcript_text, metadata
