from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import AnalyzeRequest, AnalyzeResponse
from services.scraper import extract_amazon_reviews
from services.ml_inference import run_hybrid_inference
from services.topic_modeling import extract_topics_lda
from services.explainability import extract_shap_values
from services.agent import generate_executive_summary

app = FastAPI(title="SentiInsight AI API")

# Add CORS Middleware to allow React to communicate with the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "*"], # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"msg": "Welcome to SentiInsight AI Backend API"}

@app.post("/analyze-url", response_model=AnalyzeResponse)
def analyze_url(req: AnalyzeRequest):
    # 1. Extraction Layer
    extracted_data = extract_amazon_reviews(req.url)
    reviews = extracted_data.get('reviews', [])
    metadata = extracted_data.get('metadata', {})
    
    # 2. ML Inference Layer (Dual-engine)
    ml_scores = run_hybrid_inference(reviews)
    
    # 3. Topic Modeling Layer (LDA)
    topics = extract_topics_lda(reviews)
    
    # 4. Explainability Layer (SHAP mock/VADER tokens)
    explainability = extract_shap_values(reviews)
    
    # 5. Agentic Layer (LangChain summary)
    agent_insight = generate_executive_summary(metadata, ml_scores, topics)
    
    return AnalyzeResponse(
        status="success",
        extraction=metadata,
        hybrid_scoring=ml_scores,
        pain_points=topics,
        explainability=explainability,
        agentic_insight=agent_insight
    )
