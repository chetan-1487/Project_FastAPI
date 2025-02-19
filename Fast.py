from fastapi import FastAPI, File, UploadFile, HTTPException
from moviepy import VideoFileClip
import os
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/audio")
async def extract_audio(file: UploadFile = File(...)):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")

    video_filename ="video_filename.mp4"
    audio_filename = "audio_filename.mp3"

    try:
        with open(video_filename, "wb") as video_file:
            video_file.write(await file.read())

        if not os.path.exists(video_filename):
            raise HTTPException(status_code=500, detail="Error: Video file was not saved.")
        video_clip = VideoFileClip(video_filename)
        audio_clip = video_clip.audio
        audio_clip.write_audiofile(audio_filename)

        if not os.path.exists(audio_filename):
            raise HTTPException(status_code=500, detail="Error: Audio file was not generated.")

        response = FileResponse(audio_filename, media_type="audio/mpeg", filename=audio_filename)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail="error")
