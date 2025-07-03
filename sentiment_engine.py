from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def process_sentiment(text: str):
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(text)
    label = (
        "Positive" if scores["compound"] > 0.05 else
        "Negative" if scores["compound"] < -0.05 else
        "Neutral"
    )
    return {
        "sentiment": {
            "scores": scores,
            "label": label
        }
    }
