from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from fastapi import FastAPI
from dotenv import load_dotenv
import requests
import os


load_dotenv()
app = FastAPI()


username = os.getenv("USER")
password = os.getenv("PASS")

# List of proxies with IP and port
raw_proxies = [
    "198.23.239.134:6540",
    "207.244.217.165:6712",
    "107.172.163.27:6543",
    "64.137.42.112:5157",
    "173.211.0.148:6641",
    "161.123.152.115:6360",
    "167.160.180.203:6754",
    "154.36.110.199:6853",
    "173.0.9.70:5653",
    "173.0.9.209:5792",
]

# Generate formatted proxies
proxies = [f"http://{username}:{password}@{ip}" for ip in raw_proxies]

@app.get("/")
def root():
    return {
        "message": "Use endpoint /transcript/{video_id}",
        "docs": "To access docs, use endpoint /docs",
    }


@app.get("/transcript/{video_id}")
def get_transcript_from_video_id(video_id: str):
    try:
        transcript_list = None
        complete_transcript = ""
        i = 0

        while i < len(proxies):
            current_proxy = proxies[i]
            proxy_dict = {"http": current_proxy, "https": current_proxy}
            try:
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxy_dict)
                break  # Exit the loop if successful
            except TranscriptsDisabled:
                print(f"Transcripts are disabled for the video. Proxy: {current_proxy}")
                # return {"error": "Transcripts are disabled for this video."}
            except requests.exceptions.ProxyError:
                print(f"Proxy is unavailable; switching to next: {current_proxy}")
            except Exception as e:
                print(f"An error occurred with proxy {current_proxy}: {e}")
            i += 1

        # If no proxies were successful
        if transcript_list is None:
            return {"error": "Unable to fetch transcript. All proxies failed."}

        # Process the transcript
        for transcript in transcript_list:
            text = transcript["text"]
            complete_transcript += text + " "

        # Ensure transcript only contains UTF-8 characters
        complete_transcript = complete_transcript.encode("utf-8", errors="ignore").decode("utf-8")

        return {"transcript": complete_transcript}
    except Exception as e:
        return {"error": str(e)}

# To run
# ```uvicorn app:app --reload```
# also rename main.py to app.py for localhost running
