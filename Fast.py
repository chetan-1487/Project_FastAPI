from fastapi import FastAPI, File, UploadFile, HTTPException
from moviepy import VideoFileClip
import os
from fastapi.responses import FileResponse
import tempfile

# Initialize FastAPI application
app = FastAPI()

# Root endpoint to welcome users
@app.get("/")
async def audio():
    return {"message": "Welcome to the audio extraction service."}

# Endpoint to handle audio extraction from uploaded video file
@app.post("/audio")
async def extract_audio(file: UploadFile = File(...)):
    # Validate that the uploaded file is a video
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video")

    try:
        # Save the uploaded video as a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video_file:
            video_filename = temp_video_file.name  # Temporary video filename
            temp_video_file.write(await file.read())  # Write the uploaded file to the temporary video file

        # Check if the video file was successfully saved
        if not os.path.exists(video_filename):
            raise HTTPException(status_code=500, detail="Error: Video file was not saved.")

        # Load the video file using MoviePy for audio extraction
        video_clip = VideoFileClip(video_filename)
        audio_filename = video_filename.replace(".mp4", ".mp3")  # Output audio filename (mp3 format)
        audio_clip = video_clip.audio  # Extract audio from the video clip
        audio_clip.write_audiofile(audio_filename)  # Save the audio to the output file

        # Check if the audio file was successfully generated
        if not os.path.exists(audio_filename):
            raise HTTPException(status_code=500, detail="Error: Audio file was not generated.")

        # Create the local folder to store the audio file if it doesn't exist
        local_folder = "audio_files"
        if not os.path.exists(local_folder):
            os.makedirs(local_folder)

        # Move the generated audio file into the local folder
        local_audio_path = os.path.join(local_folder, os.path.basename(audio_filename))
        os.rename(audio_filename, local_audio_path)

        # Return the audio file as a response to the client
        response = FileResponse(local_audio_path, media_type="audio/mpeg", filename=os.path.basename(local_audio_path))

        # Clean up: Remove the temporary video file after processing
        os.remove(video_filename)

        # Return the audio file to the client
        return response

    except Exception as e:
        # Handle any errors that occur during the process and return an error response
        raise HTTPException(status_code=500, detail=str(e))
