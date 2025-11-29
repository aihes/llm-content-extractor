"""XML content extraction strategy with robust error handling."""

import re
from typing import Any, Optional, Union

try:
    from lxml import etree

    LXML_AVAILABLE = True
except ImportError:
    LXML_AVAILABLE = False

from llm_content_extractor.base import ContentExtractor


class XMLExtractor(ContentExtractor):
    """
    Extract and parse XML content from LLM output.

    This extractor can validate XML syntax if lxml is available,
    otherwise it performs best-effort extraction.
    """

    def __init__(self, validate: bool = True, recover: bool = True) -> None:
        """
        Initialize XMLExtractor.

        Args:
            validate: If True and lxml is available, validate XML syntax.
                     Default is True.
            recover: If True and lxml is available, attempt to recover from
                    malformed XML. Default is True.
        """
        self.validate = validate
        self.recover = recover

    def extract(self, raw_text: str) -> str:
        """
        Extract XML from raw text.

        Args:
            raw_text: Raw string that may contain XML

        Returns:
            Cleaned XML string (validated if lxml is available)

        Raises:
            ValueError: If valid XML cannot be extracted
            TypeError: If input is not a string
        """
        # Input validation
        if not isinstance(raw_text, str):
            raise TypeError(f"Expected string input, got {type(raw_text).__name__}")

        if not raw_text or not raw_text.strip():
            raise ValueError("Cannot extract XML from empty or whitespace-only string")

        # Remove markdown fences
        text = self._remove_markdown_fence(raw_text, "xml")
        text = text.strip()

        if not text:
            raise ValueError("No content remaining after preprocessing")

        # Extract XML content
        xml_content = self._extract_xml_content(text)
        if not xml_content:
            raise ValueError(
                "Could not extract valid XML from the provided text. "
                "The text may not contain XML tags or the structure is malformed."
            )

        # Validate if lxml is available and validation is enabled
        if LXML_AVAILABLE and self.validate:
            xml_content = self._validate_and_clean_xml(xml_content)

        return xml_content

    def _validate_and_clean_xml(self, xml_text: str) -> str:
        """
        Validate XML syntax and optionally recover from errors.

        Args:
            xml_text: XML string to validate

        Returns:
            Validated (and possibly recovered) XML string

        Raises:
            ValueError: If XML is invalid and recovery is disabled
        """
        if not LXML_AVAILABLE:
            return xml_text

        try:
            # Try strict parsing first
            parser = etree.XMLParser(
                recover=False,
                remove_blank_text=False,
                resolve_entities=False,  # Security: disable entity expansion
                no_network=True,  # Security: disable network access
            )
            etree.fromstring(xml_text.encode("utf-8"), parser=parser)
            return xml_text

        except etree.XMLSyntaxError as e:
            if not self.recover:
                raise ValueError(
                    f"Invalid XML syntax: {e.msg} at line {e.lineno}, column {e.offset}"
                )

            # Try recovery mode
            try:
                parser = etree.XMLParser(
                    recover=True,
                    remove_blank_text=False,
                    resolve_entities=False,
                    no_network=True,
                )
                tree = etree.fromstring(xml_text.encode("utf-8"), parser=parser)

                # Re-serialize the recovered tree
                recovered = etree.tostring(
                    tree, encoding="unicode", method="xml", pretty_print=False
                )
                return recovered

            except Exception as recover_error:
                raise ValueError(
                    f"XML validation failed and recovery unsuccessful: {str(recover_error)}"
                )

    def _extract_xml_content(self, text: str) -> str:
        """
        Extract XML content from text using multiple strategies.

        Args:
            text: Text that may contain XML

        Returns:
            Extracted XML string or empty string if not found
        """
        if not text:
            return ""

        # Strategy 1: Look for XML declaration
        xml_with_declaration = self._extract_with_declaration(text)
        if xml_with_declaration:
            return xml_with_declaration

        # Strategy 2: Look for complete XML documents/fragments
        xml_fragment = self._extract_xml_fragment(text)
        if xml_fragment:
            return xml_fragment

        # Strategy 3: Check if entire text is XML
        if self._looks_like_xml(text):
            return text

        return ""

    def _extract_with_declaration(self, text: str) -> str:
        """
        Extract XML that starts with a declaration.

        Args:
            text: Text that may contain XML with declaration

        Returns:
            Extracted XML or empty string
        """
        # Pattern for XML declaration followed by content
        pattern = r'<\?xml[^>]*\?>.*?(?=<\?xml|$)'
        matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)

        if matches:
            # Return the longest match (most complete)
            return max(matches, key=len).strip()

        return ""

    def _extract_xml_fragment(self, text: str) -> str:
        """
        Extract XML fragment without declaration.

        Args:
            text: Text that may contain XML fragment

        Returns:
            Extracted XML or empty string
        """
        # Find all potential XML root elements
        # Pattern: opening tag with possible attributes, content, closing tag
        pattern = r'<([a-zA-Z_][\w\-\.]*)[^>]*>.*?</\1>'
        matches = re.findall(pattern, text, re.DOTALL)

        if not matches:
            # Try self-closing tags
            pattern = r'<[a-zA-Z_][\w\-\.]*[^>]*/>'
            if re.search(pattern, text):
                match = re.search(pattern, text)
                return match.group(0) if match else ""
            return ""

        # Find the complete XML for the first root element
        # This is a simplified approach; for complex cases, use proper parsing
        first_tag = matches[0]
        tag_pattern = rf'<{re.escape(first_tag)}[^>]*>.*?</{re.escape(first_tag)}>'
        match = re.search(tag_pattern, text, re.DOTALL)

        if match:
            return match.group(0).strip()

        return ""

    def _looks_like_xml(self, text: str) -> bool:
        """
        Heuristic check if text looks like XML.

        Args:
            text: Text to check

        Returns:
            True if text appears to be XML
        """
        if not text:
            return False

        text = text.strip()

        # Check for XML declaration
        if text.startswith("<?xml"):
            return True

        # Check for opening and closing tags
        if not (text.startswith("<") and text.endswith(">")):
            return False

        # Check for at least one complete tag
        tag_pattern = r'<([a-zA-Z_][\w\-\.]*)[^>]*>.*?</\1>|<[a-zA-Z_][\w\-\.]*[^>]*/>'
        if re.search(tag_pattern, text, re.DOTALL):
            return True

        return False

    def is_valid_xml(self, xml_text: str) -> bool:
        """
        Check if XML string is valid without raising an exception.

        Args:
            xml_text: XML string to check

        Returns:
            True if XML is valid, False otherwise
        """
        if not LXML_AVAILABLE:
            # Without lxml, use heuristic
            return self._looks_like_xml(xml_text)

        try:
            parser = etree.XMLParser(
                recover=False,
                resolve_entities=False,
                no_network=True,
            )
            etree.fromstring(xml_text.encode("utf-8"), parser=parser)
            return True
        except (etree.XMLSyntaxError, ValueError, TypeError):
            return False
