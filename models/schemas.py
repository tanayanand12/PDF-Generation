# models/schemas.py
from pydantic import BaseModel, validator
from typing import List, Dict, Optional, Any

class PDFRequest(BaseModel):
    """Request model for PDF generation."""
    sections: List[Dict[str, str]]
    filename: Optional[str] = None
    
    @validator('sections')
    def validate_sections(cls, v):
        if not v:
            raise ValueError("Sections cannot be empty")
        
        for section in v:
            if not isinstance(section, dict):
                raise ValueError("Each section must be a dictionary")
            if len(section) != 1:
                raise ValueError("Each section must have exactly one key-value pair")
            
            key, value = next(iter(section.items()))
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValueError("Both header and content must be strings")
                
        return v

class PDFResponse(BaseModel):
    """Response model for PDF generation."""
    success: bool
    filename: str
    download_url: str
    metadata: Dict[str, Any]

class LayoutPlan(BaseModel):
    """Layout planning result from GPT-5."""
    strategy: str
    section_breaks: List[int]
    formatting_rules: Dict[str, Any]
    estimated_pages: int

class ValidationResult(BaseModel):
    """Validation result model."""
    is_valid: bool
    error_message: Optional[str] = None
    warnings: List[str] = []


