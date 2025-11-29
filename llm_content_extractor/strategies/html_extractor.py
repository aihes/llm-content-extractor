"""HTML content extraction strategy with robust error handling."""

import re
from typing import List, Optional

try:
    from lxml import etree, html as lxml_html

    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False

from llm_content_extractor.base import ContentExtractor


class HTMLExtractor(ContentExtractor):
    """
    Extract and parse HTML content from LLM output.

    This extractor can validate and clean HTML if lxml is available,
    otherwise it performs best-effort extraction.
    """

    def __init__(self, validate: bool = False, clean: bool = False) -> None:
        """
        Initialize HTMLExtractor.

        Args:
            validate: If True and lxml is available, validate HTML structure.
                     Default is False (HTML is more lenient than XML).
            clean: If True and lxml is available, clean and normalize HTML.
                  Default is False to preserve original formatting.
        """
        self.validate = validate
        self.clean = clean

    def extract(self, raw_text: str) -> str:
        """
        Extract HTML from raw text.

        Args:
            raw_text: Raw string that may contain HTML

        Returns:
            Cleaned HTML string

        Raises:
            ValueError: If valid HTML cannot be extracted
            TypeError: If input is not a string
        """
        # Input validation
        if not isinstance(raw_text, str):
            raise TypeError(f"Expected string input, got {type(raw_text).__name__}")

        if not raw_text or not raw_text.strip():
            raise ValueError("Cannot extract HTML from empty or whitespace-only string")

        # Remove markdown fences
        text = self._remove_markdown_fence(raw_text, "html")
        text = text.strip()

        if not text:
            raise ValueError("No content remaining after preprocessing")

        # Extract HTML content
        html_content = self._extract_html_content(text)
        if not html_content:
            raise ValueError(
                "Could not extract valid HTML from the provided text. "
                "The text may not contain HTML tags or the structure is malformed."
            )

        # Clean/validate if lxml is available and enabled
        if LXML_AVAILABLE:
            if self.clean:
                html_content = self._clean_html(html_content)
            elif self.validate:
                self._validate_html(html_content)

        return html_content

    def _validate_html(self, html_text: str) -> None:
        """
        Validate HTML structure.

        Args:
            html_text: HTML string to validate

        Raises:
            ValueError: If HTML is malformed
        """
        if not LXML_AVAILABLE:
            return

        try:
            # Parse HTML - lxml is lenient by default
            lxml_html.fromstring(html_text)
        except etree.ParserError as e:
            raise ValueError(f"Invalid HTML structure: {str(e)}")
        except Exception as e:
            raise ValueError(f"HTML validation failed: {str(e)}")

    def _clean_html(self, html_text: str) -> str:
        """
        Clean and normalize HTML.

        Args:
            html_text: HTML string to clean

        Returns:
            Cleaned HTML string
        """
        if not LXML_AVAILABLE:
            return html_text

        try:
            # Parse HTML
            tree = lxml_html.fromstring(html_text)

            # Serialize back to string
            cleaned = etree.tostring(
                tree,
                encoding="unicode",
                method="html",
                pretty_print=False,
            )

            return cleaned

        except Exception:
            # If cleaning fails, return original
            return html_text

    def _extract_html_content(self, text: str) -> str:
        """
        Extract HTML content from text using multiple strategies.

        Strategies:
        1. Complete HTML documents with DOCTYPE
        2. HTML documents with <html> tag
        3. HTML fragments with common root elements
        4. Any content with HTML tags

        Args:
            text: Text that may contain HTML

        Returns:
            Extracted HTML string or empty string if not found
        """
        if not text:
            return ""

        # Strategy 1: Complete HTML document with DOCTYPE
        doctype_html = self._extract_doctype_html(text)
        if doctype_html:
            return doctype_html

        # Strategy 2: HTML with <html> root
        html_with_root = self._extract_html_with_root(text)
        if html_with_root:
            return html_with_root

        # Strategy 3: HTML fragments with common structures
        html_fragment = self._extract_html_fragment(text)
        if html_fragment:
            return html_fragment

        # Strategy 4: Check if entire text looks like HTML
        if self._looks_like_html(text):
            return text

        return ""

    def _extract_doctype_html(self, text: str) -> str:
        """
        Extract complete HTML document with DOCTYPE.

        Args:
            text: Text that may contain HTML document

        Returns:
            Extracted HTML or empty string
        """
        # Pattern for DOCTYPE followed by HTML
        pattern = r'<!DOCTYPE\s+html.*?</html>'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        if matches:
            return max(matches, key=len).strip()

        return ""

    def _extract_html_with_root(self, text: str) -> str:
        """
        Extract HTML with <html> root element.

        Args:
            text: Text that may contain HTML with root

        Returns:
            Extracted HTML or empty string
        """
        # Pattern for <html> to </html>
        pattern = r'<html[^>]*>.*?</html>'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        if matches:
            return max(matches, key=len).strip()

        return ""

    def _extract_html_fragment(self, text: str) -> str:
        """
        Extract HTML fragment with common root elements.

        Args:
            text: Text that may contain HTML fragment

        Returns:
            Extracted HTML or empty string
        """
        # Common HTML container elements
        container_tags = [
            "body",
            "div",
            "section",
            "article",
            "main",
            "header",
            "footer",
            "nav",
            "aside",
        ]

        best_match = ""
        max_length = 0

        for tag in container_tags:
            pattern = rf'<{tag}[^>]*>.*?</{tag}>'
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

            for match in matches:
                if len(match) > max_length:
                    max_length = len(match)
                    best_match = match

        if best_match:
            return best_match.strip()

        # Try any paired tags
        pattern = r'<([a-zA-Z][\w\-]*)[^>]*>.*?</\1>'
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            # Reconstruct the full match
            first_tag = matches[0]
            tag_pattern = rf'<{re.escape(first_tag)}[^>]*>.*?</{re.escape(first_tag)}>'
            match = re.search(tag_pattern, text, re.DOTALL)
            if match:
                return match.group(0).strip()

        return ""

    def _looks_like_html(self, text: str) -> bool:
        """
        Heuristic check if text looks like HTML.

        Args:
            text: Text to check

        Returns:
            True if text appears to be HTML
        """
        if not text:
            return False

        text = text.strip()

        # Check for DOCTYPE
        if text.lower().startswith("<!doctype html"):
            return True

        # Must start with < and contain closing >
        if not (text.startswith("<") and ">" in text):
            return False

        # Check for common HTML patterns
        html_patterns = [
            r'<html[^>]*>',
            r'<head[^>]*>',
            r'<body[^>]*>',
            r'<div[^>]*>',
            r'<p[^>]*>',
            r'<span[^>]*>',
            r'<a[^>]*>',
            r'<img[^>]*>',
            r'</[a-zA-Z][\w\-]*>',  # Closing tag
        ]

        match_count = sum(
            1 for pattern in html_patterns if re.search(pattern, text, re.IGNORECASE)
        )

        # If we find multiple HTML patterns, it's likely HTML
        return match_count >= 2

    def is_valid_html(self, html_text: str) -> bool:
        """
        Check if HTML string is valid without raising an exception.

        Args:
            html_text: HTML string to check

        Returns:
            True if HTML is valid, False otherwise
        """
        if not LXML_AVAILABLE:
            # Without lxml, use heuristic
            return self._looks_like_html(html_text)

        try:
            lxml_html.fromstring(html_text)
            return True
        except (etree.ParserError, ValueError, TypeError):
            return False

    def extract_all_fragments(self, raw_text: str) -> List[str]:
        """
        Extract all HTML fragments from text.

        This is useful when LLM output contains multiple HTML snippets.

        Args:
            raw_text: Raw text that may contain multiple HTML fragments

        Returns:
            List of extracted HTML fragments

        Raises:
            TypeError: If input is not a string
        """
        if not isinstance(raw_text, str):
            raise TypeError(f"Expected string input, got {type(raw_text).__name__}")

        fragments = []
        text = self._remove_markdown_fence(raw_text, "html")

        # Find all paired tags
        pattern = r'<([a-zA-Z][\w\-]*)[^>]*>.*?</\1>'
        matches = re.finditer(pattern, text, re.DOTALL)

        for match in matches:
            fragment = match.group(0).strip()
            if fragment and self._looks_like_html(fragment):
                fragments.append(fragment)

        return fragments
