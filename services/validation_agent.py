# services/validation_agent.py
import os
import pymupdf4llm
from typing import List, Dict
from models.schemas import ValidationResult
import logging

logger = logging.getLogger(__name__)

class ValidationAgent:
    """Input and output validation agent."""
    
    def validate_input(self, sections: List[Dict[str, str]]) -> ValidationResult:
        """
        Validate input structure and content.
        
        Args:
            sections: Input sections to validate
            
        Returns:
            ValidationResult with validation status
        """
        try:
            # Check basic structure
            if not sections:
                return ValidationResult(
                    is_valid=False,
                    error_message="No sections provided"
                )
            
            warnings = []
            
            # Validate each section
            for i, section in enumerate(sections):
                if not isinstance(section, dict):
                    return ValidationResult(
                        is_valid=False,
                        error_message=f"Section {i+1} is not a dictionary"
                    )
                
                if len(section) != 1:
                    return ValidationResult(
                        is_valid=False,
                        error_message=f"Section {i+1} must have exactly one key-value pair"
                    )
                
                header, content = next(iter(section.items()))
                
                # Content length warnings
                if len(content) > 10000:
                    warnings.append(f"Section '{header}' has very long content ({len(content)} chars)")
                
                if len(header) > 100:
                    warnings.append(f"Header '{header[:50]}...' is very long")
            
            return ValidationResult(
                is_valid=True,
                warnings=warnings
            )
            
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"Validation error: {str(e)}"
            )
    
    def validate_pdf_structure(self, pdf_path: str) -> ValidationResult:
        """
        Validate generated PDF structure.
        
        Args:
            pdf_path: Path to generated PDF
            
        Returns:
            ValidationResult with PDF validation status
        """
        try:
            if not os.path.exists(pdf_path):
                return ValidationResult(
                    is_valid=False,
                    error_message="PDF file not found"
                )
            
            # Basic file size check
            file_size = os.path.getsize(pdf_path)
            if file_size < 1024:  # Less than 1KB
                return ValidationResult(
                    is_valid=False,
                    error_message="PDF file appears to be empty or corrupted"
                )
            
            warnings = []
            
            # Large file warning
            if file_size > 50 * 1024 * 1024:  # 50MB
                warnings.append("PDF file is very large (>50MB)")
            
            return ValidationResult(
                is_valid=True,
                warnings=warnings
            )
            
        except Exception as e:
            logger.error(f"PDF validation error: {e}")
            return ValidationResult(
                is_valid=True,  # Don't fail generation for validation errors
                warnings=[f"Could not validate PDF structure: {str(e)}"]
            )


