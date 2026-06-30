from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

_analyzer = None

def get_analyzer():
    global _analyzer
    if _analyzer is None:
        _analyzer = SentimentIntensityAnalyzer()
    return _analyzer

def predict_sentiment(text: str) -> str:
    scores = get_analyzer().polarity_scores(text)
    compound = scores["compound"]
    if compound >= 0.05:
        return "positive"
    if compound <= -0.05:
        return "negative"
    return "neutral"
