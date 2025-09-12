# services/pdf_generator.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import black, darkblue
from typing import List, Dict
import tempfile
import os
from models.schemas import LayoutPlan
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Professional PDF generation service."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Professional header style
        self.styles.add(ParagraphStyle(
            name='CustomHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=darkblue,
            fontName='Helvetica-Bold',
            keepWithNext=True
        ))
        
        # Professional body style
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=12,
            spaceBefore=6,
            leftIndent=0,
            fontName='Helvetica',
            alignment=0,  # Left align
            leading=18  # Line spacing
        ))
    
    # def generate_pdf(self, sections: List[Dict[str, str]], layout_plan: LayoutPlan, filename: str) -> str:
    #     """
    #     Generate PDF from sections using layout plan.
        
    #     Args:
    #         sections: List of header-content dictionaries
    #         layout_plan: GPT-generated layout plan
    #         filename: Output filename
            
    #     Returns:
    #         Path to generated PDF file
    #     """
    #     try:
    #         # Create temporary file
    #         temp_dir = tempfile.gettempdir()
    #         pdf_path = os.path.join(temp_dir, filename)
            
    #         # Apply formatting rules from layout plan
    #         self._apply_formatting_rules(layout_plan.formatting_rules)
            
    #         # Create PDF document
    #         doc = SimpleDocTemplate(
    #             pdf_path,
    #             pagesize=A4,
    #             rightMargin=72,
    #             leftMargin=72,
    #             topMargin=72,
    #             bottomMargin=72
    #         )
            
    #         # Build content
    #         story = []
            
    #         for i, section in enumerate(sections):
    #             header, content = next(iter(section.items()))
                
    #             # Add section header
    #             header_para = Paragraph(header, self.styles['CustomHeader'])
    #             story.append(header_para)
                
    #             # Add section content
    #             # Handle long content by splitting into paragraphs
    #             content_paragraphs = self._split_content(content)
    #             for para_text in content_paragraphs:
    #                 if para_text.strip():
    #                     content_para = Paragraph(para_text, self.styles['CustomBody'])
    #                     story.append(content_para)
                
    #             # Add spacing between sections
    #             story.append(Spacer(1, 0.2*inch))
                
    #             # Force page break if specified in layout plan
    #             if i in layout_plan.section_breaks:
    #                 story.append(PageBreak())
            
    #         # Build PDF
    #         doc.build(story)
            
    #         logger.info(f"PDF generated successfully: {pdf_path}")
    #         return pdf_path
            
    #     except Exception as e:
    #         logger.error(f"PDF generation failed: {e}")
    #         raise Exception(f"PDF generation failed: {str(e)}")


    def generate_pdf(self, sections: List[Dict[str, str]], layout_plan: LayoutPlan, filename: str) -> bytes:
        """
        Generate PDF from sections using layout plan.
        
        Args:
            sections: List of header-content dictionaries
            layout_plan: GPT-generated layout plan
            filename: Output filename
            
        Returns:
            PDF file as bytes
        """
        try:
            # Create in-memory buffer
            from io import BytesIO
            buffer = BytesIO()
            
            # Apply formatting rules from layout plan
            self._apply_formatting_rules(layout_plan.formatting_rules)
            
            # Create PDF document
            doc = SimpleDocTemplate(
                buffer,
                pagesize=A4,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Build content
            story = []
            
            for i, section in enumerate(sections):
                header, content = next(iter(section.items()))
                
                # Add section header
                header_para = Paragraph(header, self.styles['CustomHeader'])
                story.append(header_para)
                
                # Add section content
                # Handle long content by splitting into paragraphs
                content_paragraphs = self._split_content(content)
                for para_text in content_paragraphs:
                    if para_text.strip():
                        content_para = Paragraph(para_text, self.styles['CustomBody'])
                        story.append(content_para)
                
                # Add spacing between sections
                story.append(Spacer(1, 0.2*inch))
                
                # Force page break if specified in layout plan
                if i in layout_plan.section_breaks:
                    story.append(PageBreak())
            
            # Build PDF
            doc.build(story)
            
            # Get bytes and return
            pdf_bytes = buffer.getvalue()
            buffer.close()
            
            logger.info(f"PDF generated successfully: {len(pdf_bytes)} bytes")
            return pdf_bytes
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            raise Exception(f"PDF generation failed: {str(e)}")
        
        
    def _apply_formatting_rules(self, rules: Dict[str, str]):
        """Apply GPT-suggested formatting rules."""
        try:
            # Update header style
            if 'header_size' in rules:
                self.styles['CustomHeader'].fontSize = int(rules['header_size'])
            
            # Update body style
            if 'body_size' in rules:
                self.styles['CustomBody'].fontSize = int(rules['body_size'])
            
            if 'line_spacing' in rules:
                spacing_multiplier = float(rules['line_spacing'])
                self.styles['CustomBody'].leading = int(self.styles['CustomBody'].fontSize * spacing_multiplier)
                
        except (ValueError, KeyError) as e:
            logger.warning(f"Could not apply formatting rule: {e}")
    
    def _split_content(self, content: str) -> List[str]:
        """Split long content into manageable paragraphs."""
        # Split by double newlines first (natural paragraph breaks)
        paragraphs = content.split('\n\n')
        
        result = []
        for para in paragraphs:
            # If paragraph is still too long, split by sentences
            if len(para) > 1000:
                sentences = para.split('. ')
                current_chunk = ""
                
                for sentence in sentences:
                    if len(current_chunk + sentence) > 1000 and current_chunk:
                        result.append(current_chunk.strip())
                        current_chunk = sentence + ". "
                    else:
                        current_chunk += sentence + ". "
                
                if current_chunk:
                    result.append(current_chunk.strip())
            else:
                result.append(para)
        
        return result


