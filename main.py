# main.py
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import tempfile
import os
import logging
from datetime import datetime

from services.pdf_generator import PDFGenerator
from services.gpt_planner import GPTPlanner
from services.validation_agent import ValidationAgent
from models.schemas import PDFRequest, PDFResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="PDF Generation Service",
    description="AI-powered PDF generation with GPT-5 planning",
    version="1.0.0"
)

# Initialize services
pdf_generator = PDFGenerator()
gpt_planner = GPTPlanner()
validator = ValidationAgent()

@app.post("/generate-pdf", response_model=PDFResponse)
async def generate_pdf(request: PDFRequest):
    """
    Generate a professionally formatted PDF from structured input.
    
    Args:
        request: PDFRequest containing list of {"Header": "Content"} dictionaries
        
    Returns:
        PDFResponse with download URL and metadata
    """
    try:
        # Validate input structure
        validation_result = validator.validate_input(request.sections)
        if not validation_result.is_valid:
            raise HTTPException(status_code=400, detail=validation_result.error_message)
        
        # Plan layout with GPT-5
        layout_plan = await gpt_planner.plan_layout(request.sections)
        logger.info(f"Generated layout plan: {layout_plan.strategy}")
        
        # Generate PDF
        pdf_path = pdf_generator.generate_pdf(
            sections=request.sections,
            layout_plan=layout_plan,
            filename=request.filename or f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        # Final validation
        final_validation = validator.validate_pdf_structure(pdf_path)
        if not final_validation.is_valid:
            logger.warning(f"PDF validation warning: {final_validation.error_message}")
        
        return PDFResponse(
            success=True,
            filename=os.path.basename(pdf_path),
            download_url=f"/download/{os.path.basename(pdf_path)}",
            metadata={
                "sections_count": len(request.sections),
                "layout_strategy": layout_plan.strategy,
                "generated_at": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"PDF generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/download/{filename}")
async def download_pdf(filename: str):
    """Download generated PDF file."""
    file_path = os.path.join(tempfile.gettempdir(), filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8734)