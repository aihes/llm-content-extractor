"""Concrete implementation of content extraction strategies."""

import json
import re
from typing import Any, Dict, List, Union

try:
    from lxml import etree
    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False

from llm_content_extractor.base import ContentExtractor


class JSONExtractor(ContentExtractor):
    """Extract and parse JSON content from LLM output with fault tolerance."""

    def extract(self, raw_text: str) -> Union[Dict[Any, Any], List[Any]]:
        """
        Extract JSON from raw text with multiple fault-tolerance strategies.

        Args:
            raw_text: Raw string that may contain JSON

        Returns:
            Parsed JSON as dict or list

        Raises:
            ValueError: If valid JSON cannot be extracted
        """
        # Strategy 1: Remove markdown fences
        text = self._remove_markdown_fence(raw_text, "json")

        # Strategy 2: Try direct parsing
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        # Strategy 3: Extract JSON-like content between braces/brackets
        json_text = self._extract_json_content(text)
        if json_text:
            # Try parsing extracted content
            try:
                return json.loads(json_text)
            except json.JSONDecodeError:
                pass

            # Strategy 4: Fix common LLM errors (trailing commas)
            fixed_text = self._fix_trailing_commas(json_text)
            try:
                return json.loads(fixed_text)
            except json.JSONDecodeError:
                pass

        raise ValueError("Could not extract valid JSON from the provided text")

    def _extract_json_content(self, text: str) -> str:
        """
        Extract JSON content from text by finding balanced braces/brackets.

        Args:
            text: Text that may contain JSON

        Returns:
            Extracted JSON string or empty string if not found
        """
        text = text.strip()

        # Try to find JSON object
        if "{" in text:
            start_idx = text.find("{")
            json_str = self._extract_balanced(text[start_idx:], "{", "}")
            if json_str:
                return json_str

        # Try to find JSON array
        if "[" in text:
            start_idx = text.find("[")
            json_str = self._extract_balanced(text[start_idx:], "[", "]")
            if json_str:
                return json_str

        return ""

    def _extract_balanced(self, text: str, open_char: str, close_char: str) -> str:
        """
        Extract balanced content between opening and closing characters.

        Args:
            text: Text starting with open_char
            open_char: Opening character (e.g., '{')
            close_char: Closing character (e.g., '}')

        Returns:
            Balanced string or empty string if not found
        """
        if not text or text[0] != open_char:
            return ""

        count = 0
        in_string = False
        escape_next = False

        for i, char in enumerate(text):
            if escape_next:
                escape_next = False
                continue

            if char == "\\" and in_string:
                escape_next = True
                continue

            if char == '"' and not in_string:
                in_string = True
            elif char == '"' and in_string:
                in_string = False
            elif char == open_char and not in_string:
                count += 1
            elif char == close_char and not in_string:
                count -= 1
                if count == 0:
                    return text[: i + 1]

        return ""

    def _fix_trailing_commas(self, json_text: str) -> str:
        """
        Remove trailing commas which are common LLM errors.

        Args:
            json_text: JSON string that may have trailing commas

        Returns:
            JSON string with trailing commas removed
        """
        # Remove trailing commas before closing braces/brackets
        # This regex handles commas followed by optional whitespace and then } or ]
        fixed = re.sub(r",(\s*[}\]])", r"\1", json_text)
        return fixed


class XMLExtractor(ContentExtractor):
    """Extract and parse XML content from LLM output."""

    def extract(self, raw_text: str) -> Union[str, Any]:
        """
        Extract XML from raw text.

        Args:
            raw_text: Raw string that may contain XML

        Returns:
            Cleaned XML string or parsed ElementTree if lxml is available

        Raises:
            ValueError: If valid XML cannot be extracted
        """
        # Remove markdown fences
        text = self._remove_markdown_fence(raw_text, "xml")

        # Extract XML content
        xml_content = self._extract_xml_content(text)
        if not xml_content:
            raise ValueError("Could not extract valid XML from the provided text")

        # If lxml is available, validate by parsing
        if LXML_AVAILABLE:
            try:
                parsed = etree.fromstring(xml_content.encode("utf-8"))
                return xml_content  # Return string, but we've validated it
            except etree.XMLSyntaxError as e:
                raise ValueError(f"Invalid XML syntax: {e}")

        return xml_content

    def _extract_xml_content(self, text: str) -> str:
        """
        Extract XML content from text.

        Args:
            text: Text that may contain XML

        Returns:
            Extracted XML string or empty string if not found
        """
        text = text.strip()

        # Look for XML declaration or root element
        xml_pattern = r"<\?xml.*?\?>.*?(?=<\?xml|$)|<[^>]+>.*?</[^>]+>"
        matches = re.findall(xml_pattern, text, re.DOTALL)

        if matches:
            # Return the longest match (likely the complete XML)
            return max(matches, key=len).strip()

        # If no match, check if the entire text looks like XML
        if text.startswith("<") and text.endswith(">"):
            return text

        return ""


class HTMLExtractor(ContentExtractor):
    """Extract and parse HTML content from LLM output."""

    def extract(self, raw_text: str) -> str:
        """
        Extract HTML from raw text.

        Args:
            raw_text: Raw string that may contain HTML

        Returns:
            Cleaned HTML string

        Raises:
            ValueError: If valid HTML cannot be extracted
        """
        # Remove markdown fences
        text = self._remove_markdown_fence(raw_text, "html")

        # Extract HTML content
        html_content = self._extract_html_content(text)
        if not html_content:
            raise ValueError("Could not extract valid HTML from the provided text")

        return html_content

    def _extract_html_content(self, text: str) -> str:
        """
        Extract HTML content from text.

        Args:
            text: Text that may contain HTML

        Returns:
            Extracted HTML string or empty string if not found
        """
        text = text.strip()

        # Look for common HTML structures
        html_patterns = [
            r"<!DOCTYPE html>.*?</html>",
            r"<html.*?</html>",
            r"<div.*?</div>",
            r"<body.*?</body>",
            r"<[^>]+>.*?</[^>]+>",
        ]

        for pattern in html_patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches:
                # Return the longest match
                return max(matches, key=len).strip()

        # If text starts and ends with HTML tags, assume it's HTML
        if re.match(r"^\s*<[^>]+>", text) and re.search(r"</[^>]+>\s*$", text):
            return text

        return ""


class CodeBlockExtractor(ContentExtractor):
    """Extract code blocks from LLM output."""

    def __init__(self, language: str = ""):
        """
        Initialize CodeBlockExtractor.

        Args:
            language: Specific language to extract (e.g., 'python', 'javascript')
                     Empty string means extract any code block
        """
        self.language = language

    def extract(self, raw_text: str) -> str:
        """
        Extract code block from raw text.

        Args:
            raw_text: Raw string that may contain code blocks

        Returns:
            Extracted code as string

        Raises:
            ValueError: If code block cannot be extracted
        """
        text = raw_text.strip()

        # Try to extract markdown code fence
        code = self._extract_fenced_code(text)
        if code:
            return code

        # If no fenced code found, return the text as-is if it looks like code
        # (This is a fallback for when LLM returns code without fences)
        if self._looks_like_code(text):
            return text

        raise ValueError("Could not extract code block from the provided text")

    def _extract_fenced_code(self, text: str) -> str:
        """
        Extract code from markdown fences.

        Args:
            text: Text that may contain fenced code blocks

        Returns:
            Extracted code or empty string if not found
        """
        # Pattern for fenced code blocks with optional language
        if self.language:
            pattern = rf"```{re.escape(self.language)}\s*\n(.*?)```"
        else:
            pattern = r"```(?:\w+)?\s*\n(.*?)```"

        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
        if matches:
            # Return the first match
            return matches[0].strip()

        # Try without language specifier
        pattern = r"```(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)
        if matches:
            return matches[0].strip()

        return ""

    def _looks_like_code(self, text: str) -> bool:
        """
        Heuristic to determine if text looks like code.

        Args:
            text: Text to check

        Returns:
            True if text looks like code
        """
        # Check for common code patterns
        code_indicators = [
            r"^\s*(?:def|class|function|const|let|var|import|from)\s+",  # Keywords
            r"[{}\[\]();]",  # Common code symbols
            r"^\s*#.*$",  # Comments
            r"^\s*//.*$",  # Comments
            r"=\s*[^=]",  # Assignment
        ]

        for pattern in code_indicators:
            if re.search(pattern, text, re.MULTILINE):
                return True

        return False
