"""
Example Router for MIND_ECHO API
This router defines an endpoint to analyze sentiment from user-provided text
and return an empathetic response.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure that the VADER lexicon is available.
nltk.download("vader_lexicon", quiet=True)

# Instantiate the router for endpoints that we will mount.
router = APIRouter(
    tags=["Sentiment Analysis"]
)

# Define the request model for sentiment analysis
class SentimentRequest(BaseModel):
    text: str  # The user-provided text input

def analyze_sentiment(text: str) -> dict:
    """
    Analyze the sentiment of the provided text using NLTK's VADER sentiment analysis.
    
    Parameters:
        text (str): The input text from the user.
    
    Returns:
        dict: A dictionary with detailed sentiment scores and an overall sentiment label.
    
    Raises:
        ValueError: If the input text is empty.
    """
    if not text.strip():
        raise ValueError("Input text cannot be empty.")
    
    # Initialize the sentiment analyzer
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    
    # Determine the overall sentiment label based on compound score thresholds.
    compound = scores.get("compound", 0)
    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"
    
    return {"scores": scores, "label": label}

@router.post("/analyze", summary="Analyze Sentiment and Provide Empathetic Response")
def sentiment_endpoint(request: SentimentRequest):
    """
    Endpoint to perform sentiment analysis on user-provided text and return both detailed sentiment 
    scores and a curated empathetic response.
    
    Request Body:
        - text: The text input from the user.
    
    Returns:
        dict: A JSON response containing:
            - sentiment: Dictionary with sentiment scores and overall label.
            - empathetic_response: A supportive message based on the sentiment.
    
    Raises:
        HTTPException with status code 400 if sentiment analysis fails.
    """
    try:
        # Perform sentiment analysis
        result = analyze_sentiment(request.text)
        
        # Generate an empathetic response based on the sentiment.
        # (In a more advanced version, you'd integrate an LLM or contextual generator.)
        if result["label"] == "Positive":
            empathetic_message = (
                "It's great to see positivity! Keep nurturing your happy moments, and consider "
                "sharing more if you'd like."
            )
        elif result["label"] == "Negative":
            empathetic_message = (
                "I understand you're going through a tough time. Remember, it's okay to feel this way. "
                "It might help to talk to someone or take some time for self-care."
            )
        else:
            empathetic_message = (
                "It seems you're in a balanced state. Keep an eye on your feelings and take care of yourself. "
                "We're here if you need support."
            )
        
        return {
            "sentiment": result,
            "empathetic_response": empathetic_message
        }
    except Exception as e:
        # Handle any errors by returning a 400 error with the exception message.
        raise HTTPException(status_code=400, detail=str(e))
