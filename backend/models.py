from pydantic import BaseModel
from typing import List, Dict, Any

class AnalyzeRequest(BaseModel):
    url: str

class AnalyzeResponse(BaseModel):
    status: str
    extraction: Dict[str, Any]
    hybrid_scoring: Dict[str, Any]
    pain_points: List[str]
    explainability: List[Dict[str, Any]]
    agentic_insight: str
