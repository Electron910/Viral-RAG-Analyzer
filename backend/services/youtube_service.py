import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from typing import Dict, Any, Tuple

def get_youtube_video_id(url: str) -> str:
    if "v=" in url:
        return url.split("v=")[1].split("&")[0]
    elif "youtu.be/" in url:
        return url.split("youtu.be/")[1].split("?")[0]
    return url

def fetch_youtube_data(url: str) -> Tuple[str, Dict[str, Any]]:
    video_id = get_youtube_video_id(url)
    
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item["text"] for item in transcript_list])
    except Exception as e:
        transcript_text = "Transcript unavailable."
        try:
            import tempfile
            import subprocess
            import os
            
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
        except Exception as fallback_e:
            import traceback
            print(f"Whisper Fallback Failed: {fallback_e}")
            if "ffmpeg" in str(fallback_e).lower() or isinstance(fallback_e, FileNotFoundError):
                print("WARNING: FFmpeg is likely missing on your system. yt-dlp requires FFmpeg to extract audio for transcription.")

    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key or api_key == "your_google_cloud_api_key":
        return transcript_text, {
            "title": "YouTube Video",
            "creator": "Unknown",
            "follower_count": 0,
            "views": 1000,
            "likes": 100,
            "comments": 10,
            "hashtags": [],
            "upload_date": "2024-01-01T00:00:00Z",
            "duration": "PT5M",
            "engagement_rate": 11.0,
            "thumbnail_url": ""
        }
        
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
    response = request.execute()
    
    if not response.get("items"):
        raise ValueError("Video not found")
        
    video = response["items"][0]
    snippet = video["snippet"]
    statistics = video.get("statistics", {})
    
    channel_id = snippet["channelId"]
    channel_req = youtube.channels().list(part="statistics", id=channel_id)
    channel_res = channel_req.execute()
    subscriber_count = 0
    if channel_res.get("items"):
        subscriber_count = int(channel_res["items"][0]["statistics"].get("subscriberCount", 0))
        
    views = int(statistics.get("viewCount", 0))
    likes = int(statistics.get("likeCount", 0))
    comments = int(statistics.get("commentCount", 0))
    engagement_rate = ((likes + comments) / views * 100) if views > 0 else 0
    
    metadata = {
        "title": snippet.get("title", ""),
        "creator": snippet.get("channelTitle", ""),
        "follower_count": subscriber_count,
        "views": views,
        "likes": likes,
        "comments": comments,
        "hashtags": snippet.get("tags", []),
        "upload_date": snippet.get("publishedAt", ""),
        "duration": video["contentDetails"].get("duration", ""),
        "engagement_rate": round(engagement_rate, 2),
        "thumbnail_url": snippet.get("thumbnails", {}).get("high", {}).get("url", "")
    }
    
    return transcript_text, metadata
