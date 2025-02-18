from fastapi import FastAPI, File, UploadFile, HTTPException
from moviepy import VideoFileClip
import tempfile
from fastapi.responses import FileResponse

app = FastAPI()

@app.post("/extract-audio/")
async def extract_audio(file: UploadFile = File(...)):
    try:
        temp_video_path = tempfile.mktemp(suffix=".mp4")

        with open(temp_video_path, "wb") as video_file:
            video_file.write(await file.read())

        video_clip = VideoFileClip(temp_video_path)

        audio = video_clip.audio

        temp_audio_path = tempfile.mktemp(suffix=".mp3")
        audio.write_audiofile(temp_audio_path)

        video_clip.close()
        audio.close()

        return FileResponse(temp_audio_path, media_type="audio/mp3", filename="extracted_audio.mp3")
    
    except Exception as e:
        raise HTTPException()