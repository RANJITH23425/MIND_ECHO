from fastapi import APIRouter
#from backend.services import sentiment_engine
from ..services import sentiment_engine
#from backend.models.schemas import SentimentRequest
from ..models.schemas import SentimentRequest



router = APIRouter(prefix="/analyze", tags=["Sentiment Analysis"])

@router.post("/")
async def analyze_sentiment(request: SentimentRequest):
    return sentiment_engine.process_sentiment(request.text)
