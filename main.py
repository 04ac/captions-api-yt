from youtube_transcript_api import YouTubeTranscriptApi
from fastapi import FastAPI
from dotenv import load_dotenv
import os


load_dotenv()
app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Use endpoint /transcript/{video_id}",
        "docs": "To access docs, use endpoint /docs",
    }


@app.get("/transcript/{video_id}")
def get_transcript_from_video_id(video_id: str):
    # video_id = "Z6nkEZyS9nA"
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, proxies={"http": os.getenv("PROXY_URL")})
        complete_transcript = ""
        for transcript in transcript_list:
            text = transcript["text"]
            complete_transcript += text + " "

            # Uncomment this if you want the transcript in a file
            # with open(f"transcript_{video_id}.txt", "a") as opf:
            #     opf.write(text + "\n")

    # Ensure transcript only contains utf-8 chars
        complete_transcript = complete_transcript.encode("utf-8", errors="ignore").decode(
            "utf-8"
        )
        return {"transcript": complete_transcript}
    except Exception as e:
        return {"error": str(e), "url": os.getenv("PROXY_URL")}

# To run
# ```uvicorn app:app --reload```
# also rename main.py to app.py for localhost running
