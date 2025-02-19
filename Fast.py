from fastapi import FastAPI, File, UploadFile, HTTPException
from moviepy import VideoFileClip
import uuid
from fastapi.responses import FileResponse
import os

app = FastAPI()

@app.post("/extract-audio/")
async def extract_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400,detail="File must be a video")
    video=f"temp_{uuid.uuid4()}.mp4"
    audio=f"temp_{uuid.uuid4()}.mp3"
    try:
        with open(video, "wb") as video_file:
            video_file.write(await file.read())

        video_clip = VideoFileClip(video)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio)

        video_clip.close()
        audio.close()

        return FileResponse(audio, media_type="audio/mpeg", filename=audio)
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"error procssing in video")
    
    finally:
        if os.path.exists(video):
            os.remove(video)
        if os.path.exists(audio):
            os.remove(audio)