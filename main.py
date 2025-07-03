from fastapi import FastAPI
from backend.routers import example, voice, sentiment
from backend.services import sentiment_engine
from mental_health_ai.companion import ask_ollama  # Import the ask_ollama function
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="MIND_ECHO API",
    description="Backend API for the Personalized Mental Health Companion Project.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React's default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CompanionRequest(BaseModel):
    user_input: str

@app.get("/")
def read_root():
    return {"message": "Welcome to MIND_ECHO API"}

@app.post("/companion")
async def companion_endpoint(request: CompanionRequest):
    response = ask_ollama(request.user_input)
    return {"reply": response}

# Include the routers
app.include_router(example.router)
app.include_router(voice.router)
app.include_router(sentiment.router)

def main():
    print("Welcome to MIND_ECHO 🌟")
    print("1. Start Mental Health Companion")
    print("2. Exit")

    choice = input("Choose an option: ")
    if choice == '1':
        start_mental_health_session()
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()