
"""
Voice Integration Router for MIND_ECHO API
Provides endpoints for converting speech to text and text to speech.
"""

from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from fastapi.responses import StreamingResponse
import speech_recognition as sr
import pyttsx3
import os
import io
import re
from gtts import gTTS
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/voice",
    tags=["Voice Integration"],
)

@router.post("/upload", summary="Convert Voice to Text")
async def voice_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print(f"🎙️ Listening (timeout: {timeout}s)...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            print("⌛ Listening timed out")
            return ""
        except Exception as e:
            print(f"⚠️ Voice input error: {e}")
            return ""



  # 👈 Add prefix

class TTSRequest(BaseModel):
    text: str
@router.post("/tts")
async def text_to_speech(text: str):
    try:
        # Initialize TTS engine
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)  # Adjust speech rate
        
        # Save speech to in-memory buffer
        with io.BytesIO() as buffer:
            # Pyttsx3 requires a file, so we use a temporary in-memory file
            engine.save_to_file(text, 'temp.wav')
            engine.runAndWait()
            
            # Read the generated file
            with open('temp.wav', 'rb') as f:
                audio_data = f.read()
            
            # Clean up
            import os
            os.remove('temp.wav')
            
            # Return as streaming response
            return StreamingResponse(
                io.BytesIO(audio_data),
                media_type="audio/wav",
                headers={"Content-Disposition": "attachment; filename=speech.wav"}
            )
            
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))