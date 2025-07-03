import speech_recognition as sr
import pyttsx3

def handle_real_time_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    engine = pyttsx3.init()

    with mic as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)

        # (Optional) Get empathetic response
        response = "It's okay to feel this way."
        engine.say(response)
        engine.runAndWait()

        return {"text": text, "response": response}
    except Exception as e:
        return {"error": str(e)}
