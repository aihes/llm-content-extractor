"""JSON content extraction strategy with robust error handling."""

import json
import re
from typing import Any, Dict, List, Optional, Union

from llm_content_extractor.base import ContentExtractor


class JSONExtractor(ContentExtractor):
    """
    Extract and parse JSON content from LLM output with fault tolerance.

    This extractor implements multiple strategies to handle various formats
    and common errors in LLM-generated JSON content.
    """

    def __init__(self, strict: bool = False) -> None:
        """
        Initialize JSONExtractor.

        Args:
            strict: If True, disable auto-fixing of common errors like trailing commas.
                   Default is False for better fault tolerance.
        """
        self.strict = strict

    def extract(self, raw_text: str) -> Union[Dict[Any, Any], List[Any]]:
        """
        Extract JSON from raw text with multiple fault-tolerance strategies.

        Strategies applied in order:
        1. Remove markdown code fences
        2. Direct JSON parsing
        3. Extract JSON-like content between braces/brackets
        4. Fix common LLM errors (trailing commas, etc.)
        5. Attempt lenient parsing with whitespace normalization

        Args:
            raw_text: Raw string that may contain JSON

        Returns:
            Parsed JSON as dict or list

        Raises:
            ValueError: If valid JSON cannot be extracted after all strategies
            TypeError: If input is not a string
        """
        # Input validation
        if not isinstance(raw_text, str):
            raise TypeError(f"Expected string input, got {type(raw_text).__name__}")

        if not raw_text or not raw_text.strip():
            raise ValueError("Cannot extract JSON from empty or whitespace-only string")

        # Strategy 1: Remove markdown fences and normalize whitespace
        text = self._remove_markdown_fence(raw_text, "json")
        text = self._normalize_whitespace(text)

        if not text:
            raise ValueError("No content remaining after preprocessing")

        # Strategy 2: Try direct parsing (fastest path for clean JSON)
        try:
            return self._parse_json(text)
        except (json.JSONDecodeError, ValueError):
            pass

        # Strategy 3: Extract JSON-like content between braces/brackets
        json_text = self._extract_json_content(text)
        if json_text:
            # Try parsing extracted content
            try:
                return self._parse_json(json_text)
            except (json.JSONDecodeError, ValueError):
                pass

            # Strategy 4: Fix common LLM errors if not in strict mode
            if not self.strict:
                fixed_text = self._fix_common_errors(json_text)
                if fixed_text != json_text:  # Only try if changes were made
                    try:
                        return self._parse_json(fixed_text)
                    except (json.JSONDecodeError, ValueError):
                        pass

        # All strategies failed
        raise ValueError(
            "Could not extract valid JSON from the provided text. "
            "The text may not contain valid JSON, or the JSON structure is too malformed to recover."
        )

    def _parse_json(self, text: str) -> Union[Dict[Any, Any], List[Any]]:
        """
        Parse JSON string with validation.

        Args:
            text: JSON string to parse

        Returns:
            Parsed JSON object

        Raises:
            ValueError: If parsing fails or result is not dict/list
        """
        try:
            result = json.loads(text)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON parsing failed: {e.msg} at position {e.pos}")

        # Validate result type
        if not isinstance(result, (dict, list)):
            raise ValueError(
                f"Expected JSON object or array, got {type(result).__name__}"
            )

        return result

    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace while preserving JSON structure.

        Args:
            text: Text to normalize

        Returns:
            Text with normalized whitespace
        """
        # Only strip leading/trailing whitespace, preserve internal structure
        return text.strip()

    def _extract_json_content(self, text: str) -> str:
        """
        Extract JSON content from text by finding balanced braces/brackets.

        This method attempts to extract the largest valid JSON structure
        from the input text.

        Args:
            text: Text that may contain JSON

        Returns:
            Extracted JSON string or empty string if not found
        """
        if not text:
            return ""

        # Determine what to extract based on which character appears first
        brace_idx = text.find("{")
        bracket_idx = text.find("[")

        # Neither found
        if brace_idx == -1 and bracket_idx == -1:
            return ""

        # Only array found, or array comes first
        if brace_idx == -1 or (bracket_idx != -1 and bracket_idx < brace_idx):
            json_str = self._extract_balanced(text[bracket_idx:], "[", "]")
            if json_str and self._looks_like_json(json_str):
                return json_str

        # Only object found, or object comes first
        if bracket_idx == -1 or (brace_idx != -1 and brace_idx < bracket_idx):
            json_str = self._extract_balanced(text[brace_idx:], "{", "}")
            if json_str and self._looks_like_json(json_str):
                return json_str

        return ""

    def _extract_balanced(self, text: str, open_char: str, close_char: str) -> str:
        """
        Extract balanced content between opening and closing characters.

        Properly handles:
        - String literals with escaped quotes
        - Nested structures
        - Unicode escape sequences

        Args:
            text: Text starting with open_char
            open_char: Opening character ('{' or '[')
            close_char: Closing character ('}' or ']')

        Returns:
            Balanced string or empty string if not found
        """
        if not text or text[0] != open_char:
            return ""

        depth = 0
        in_string = False
        escape_next = False
        i = 0

        try:
            while i < len(text):
                char = text[i]

                if escape_next:
                    escape_next = False
                    i += 1
                    continue

                if char == "\\" and in_string:
                    escape_next = True
                    i += 1
                    continue

                if char == '"' and not in_string:
                    in_string = True
                elif char == '"' and in_string:
                    in_string = False
                elif char == open_char and not in_string:
                    depth += 1
                elif char == close_char and not in_string:
                    depth -= 1
                    if depth == 0:
                        return text[: i + 1]

                i += 1

        except IndexError:
            # Malformed input, return empty string
            return ""

        # No balanced structure found
        return ""

    def _looks_like_json(self, text: str) -> bool:
        """
        Heuristic check if text looks like JSON.

        Args:
            text: Text to check

        Returns:
            True if text appears to be JSON
        """
        if not text:
            return False

        text = text.strip()

        # Must start with { or [
        if not (text.startswith("{") or text.startswith("[")):
            return False

        # Must end with } or ]
        if not (text.endswith("}") or text.endswith("]")):
            return False

        # Should have some JSON-like patterns
        json_patterns = [
            r'"[^"]*"\s*:',  # Key-value pairs
            r':\s*"[^"]*"',  # String values
            r':\s*[\d\-]',  # Numeric values
            r':\s*(?:true|false|null)',  # Boolean/null values
            r'\[.*\]',  # Arrays
        ]

        return any(re.search(pattern, text) for pattern in json_patterns)

    def _fix_common_errors(self, json_text: str) -> str:
        """
        Fix common LLM errors in JSON.

        Fixes:
        - Trailing commas before closing braces/brackets
        - Multiple consecutive commas
        - Commas after the last element
        - Extra whitespace around structural characters

        Args:
            json_text: JSON string that may have errors

        Returns:
            JSON string with common errors fixed
        """
        if not json_text:
            return json_text

        # Fix trailing commas before closing braces/brackets
        # This handles cases like: {"key": "value",} or [1, 2, 3,]
        fixed = re.sub(r',(\s*[}\]])', r'\1', json_text)

        # Fix multiple consecutive commas
        fixed = re.sub(r',(\s*,)+', r',', fixed)

        # Fix comma at the start of object/array (rare but possible)
        fixed = re.sub(r'([{\[])\s*,', r'\1', fixed)

        return fixed

    def _extract_from_code_fence(
        self, text: str, language: Optional[str] = None
    ) -> Optional[str]:
        """
        Extract content from markdown code fence.

        Args:
            text: Text that may contain code fence
            language: Expected language (e.g., 'json')

        Returns:
            Extracted content or None if no fence found
        """
        if not text:
            return None

        # Pattern for code fences with optional language
        if language:
            patterns = [
                rf"```{language}\s*\n(.*?)```",
                rf"```{language.upper()}\s*\n(.*?)```",
            ]
        else:
            patterns = [r"```(?:\w+)?\s*\n(.*?)```"]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches:
                return matches[0].strip()

        return None
