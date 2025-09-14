# services/gpt_planner.py
import openai
import json
import os
from typing import List, Dict
from models.schemas import LayoutPlan
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class GPTPlanner:
    """GPT-5 powered layout planning agent."""
    
    def __init__(self):
        load_dotenv
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4"  # Using GPT-4 as GPT-5 isn't available yet
        
    async def plan_layout(self, sections: List[Dict[str, str]]) -> LayoutPlan:
        """
        Use GPT to plan optimal PDF layout and formatting.
        
        Args:
            sections: List of header-content dictionaries
            
        Returns:
            LayoutPlan with formatting strategy
        """
        try:
            # Prepare content analysis prompt
            content_summary = self._analyze_content(sections)
            
            # prompt = f"""
            # Analyze the following document sections and create an optimal PDF layout plan:

            # Document Sections ({len(sections)} total):
            # {content_summary}

            # Provide a JSON response with:
            # 1. strategy: Overall formatting approach
            # 2. section_breaks: Indices where page breaks should be forced
            # 3. formatting_rules: CSS-like rules for styling
            # 4. estimated_pages: Expected page count

            # Consider:
            # - Professional document standards
            # - Preventing mid-section page breaks
            # - Consistent typography hierarchy
            # - Optimal spacing and readability
            # """

            prompt = f"""
                You are tasked with analyzing the following structured document input and generating an optimal PDF layout plan.

                Input Format:
                [{{
                "header": "Section Title",
                "content": "Corresponding section content"
                }}, ...]

                Document Content:
                {content_summary}

                Your goal is to produce a comprehensive JSON response that guides the PDF generation pipeline. The response must include:

                1. strategy: A high-level description of the overall formatting and layout approach
                2. section_breaks: List of indices where page breaks should be explicitly applied (avoid mid-section breaks)
                3. formatting_rules: CSS-like styling rules for headers, subheaders, body text, tables, and visuals, single column preferable for professionalism
                4. estimated_pages: Approximate number of pages based on content density and layout 
                5. toc_structure: A clickable content index structure with anchor mappings
                6. visual_elements: Suggestions for tables or visualizations where applicable
                7. appendix_plan: Placement and formatting strategy for supplementary content
                8. color_palette: Formal, subtle, and complementary color scheme for the document keeping readiblity on priority keeping good contrast in background color and text
                9. alignment_strategy: Rules for full-width alignment to ensure balanced page layout
                10. aesthetic_notes: Guidelines to enhance the document’s professional appearance and user experience

                Design Considerations:
                - Follow professional document standards and ensure consistent typography hierarchy
                - Prevent blank space at the end of pages; avoid starting new sections on fresh pages unless necessary
                - Apply bold, italics, and underlining where semantically appropriate to enhance clarity
                - Ensure the document feels informative, formal, and positively engaging to the reader
                - Include tables and visualizations where analytics insights are present
                - Maintain a cohesive and elegant aesthetic throughout the document

                Return the output strictly as a structured JSON object with all fields populated.
            """
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional document layout expert. Respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                # temperature=0.3,
                # max_tokens=1000
            )
            
            # Parse GPT response
            plan_data = json.loads(response.choices[0].message.content)
            logger.info(f"GPT layout plan: {plan_data}")
            
            return LayoutPlan(
                strategy=plan_data.get("strategy", "standard_professional"),
                section_breaks=plan_data.get("section_breaks", []),
                formatting_rules=plan_data.get("formatting_rules", self._default_formatting()),
                estimated_pages=plan_data.get("estimated_pages", self._estimate_pages(sections))
            )
            
        except Exception as e:
            logger.warning(f"GPT planning failed, using defaults: {e}")
            return self._default_layout_plan(sections)
    
    def _analyze_content(self, sections: List[Dict[str, str]]) -> str:
        """Analyze content structure for GPT planning."""
        analysis = []
        for i, section in enumerate(sections):
            header, content = next(iter(section.items()))
            content_length = len(content)
            analysis.append(f"Section {i+1}: '{header}' ({content_length} chars)")
        
        return "\n".join(analysis)
    
    def _estimate_pages(self, sections: List[Dict[str, str]]) -> int:
        """Rough page estimation based on content length."""
        total_chars = sum(len(list(section.values())[0]) for section in sections)
        # Assuming ~2500 chars per page with formatting
        return max(1, (total_chars // 2500) + 1)
    
    def _default_formatting(self) -> Dict[str, str]:
        """Default CSS-like formatting rules."""
        return {
            "header_font": "Arial-Bold",
            "header_size": "16",
            "body_font": "Arial",
            "body_size": "12",
            "line_spacing": "1.5",
            "margin_top": "72",
            "margin_bottom": "72",
            "margin_left": "72",
            "margin_right": "72"
        }
    
    def _default_layout_plan(self, sections: List[Dict[str, str]]) -> LayoutPlan:
        """Fallback layout plan when GPT fails."""
        return LayoutPlan(
            strategy="standard_professional_fallback",
            section_breaks=[],
            formatting_rules=self._default_formatting(),
            estimated_pages=self._estimate_pages(sections)
        )


