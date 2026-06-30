from textblob import TextBlob

def get_sentiment(text):
    if not text:
        return 0.0
    try:
        return TextBlob(text).sentiment.polarity
    except Exception:
        return 0.0