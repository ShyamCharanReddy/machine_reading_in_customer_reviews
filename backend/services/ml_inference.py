import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Download VADER lexicon if not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

# Initialize VADER analyzer
sia = SentimentIntensityAnalyzer()

# Initialize HuggingFace pipeline (roberta-base). 
# We use a known sentiment analysis model.
sentiment_pipeline = pipeline(
    "sentiment-analysis", 
    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest",
    truncation=True,
    max_length=512
)

def run_hybrid_inference(reviews: list):
    """
    Runs VADER and RoBERTa on a list of reviews.
    Aggregates the scores and returns a combined hybrid profile.
    """
    if not reviews:
        return {
            "vader_compound": 0,
            "roberta_distribution": {"positive": 0.33, "neutral": 0.34, "negative": 0.33},
            "final_prediction": "Neutral"
        }
        
    total_compound = 0
    roberta_counts = {"positive": 0, "neutral": 0, "negative": 0}
    
    # RoBERTa returns labels like 'positive', 'neutral', 'negative'
    for review in reviews:
        # VADER inference
        vader_scores = sia.polarity_scores(review)
        total_compound += vader_scores['compound']
        
        # RoBERTa inference
        # The pipeline can crash on extremely long inputs even with truncation if not careful, but truncation=True protects us.
        try:
            roberta_result = sentiment_pipeline(review)[0]
            label = roberta_result['label'].lower()
            if label in roberta_counts:
                roberta_counts[label] += 1
            else:
                roberta_counts['neutral'] += 1
        except Exception:
            roberta_counts['neutral'] += 1
            
    # Aggregate VADER
    avg_compound = total_compound / len(reviews)
    
    # Aggregate RoBERTa
    total_roberta = sum(roberta_counts.values())
    roberta_dist = {
        "positive": round((roberta_counts['positive'] / total_roberta) * 100) if total_roberta else 33,
        "neutral": round((roberta_counts['neutral'] / total_roberta) * 100) if total_roberta else 34,
        "negative": round((roberta_counts['negative'] / total_roberta) * 100) if total_roberta else 33,
    }
    
    # Simple Logistic Regression heuristic wrapper
    # Emphasizes negative if roberta_negative is high or vader is < -0.1
    if roberta_dist['negative'] >= 40 or avg_compound < -0.1:
        final_verdict = "Negative"
    elif roberta_dist['positive'] >= 50 or avg_compound > 0.3:
        final_verdict = "Positive"
    else:
        final_verdict = "Neutral"

    return {
        "vader_compound": round(avg_compound, 2),
        "roberta_distribution": roberta_dist,
        "final_prediction": final_verdict
    }
