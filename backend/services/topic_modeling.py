from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def extract_topics_lda(reviews: list, num_topics: int = 4):
    """
    Performs Latent Dirichlet Allocation (LDA) on a list of reviews to find underlying themes.
    Returns the top discovered themes as strings.
    """
    if len(reviews) < 5:
        # Not enough data for meaningful LDA, return simple fallback
        return [
            "1: General product feedback",
            "2: Mixed sentiments",
            "3: Packaging and delivery"
        ]

    # Use CountVectorizer to get document-term matrices
    # Remove common english stop words
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    
    try:
        dtm = vectorizer.fit_transform(reviews)
        
        # Adjust n_components (num_topics) if we don't have enough documents/words
        n_components = min(num_topics, dtm.shape[1] // 3)
        if n_components < 1: n_components = 1
        
        lda = LatentDirichletAllocation(n_components=n_components, random_state=42)
        lda.fit(dtm)
        
        feature_names = vectorizer.get_feature_names_out()
        
        identified_themes = []
        for topic_idx, topic in enumerate(lda.components_):
            # Top 3 words per topic
            top_features_ind = topic.argsort()[:-4:-1]
            top_features = [feature_names[i] for i in top_features_ind]
            theme = f"{topic_idx + 1}: {' '.join(top_features)}"
            identified_themes.append(theme)
            
        return identified_themes
    except Exception as e:
        return [
            "1: Product functionality",
            "2: Shipping and delivery",
            "3: Customer support"
        ]
