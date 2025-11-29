"""Code block extraction strategy with robust error handling."""

import re
from typing import Dict, List, Optional, Set

from llm_content_extractor.base import ContentExtractor


class CodeBlockExtractor(ContentExtractor):
    """
    Extract code blocks from LLM output.

    Supports:
    - Markdown fenced code blocks with language specifiers
    - Generic code blocks without language
    - Unfenced code detection using heuristics
    """

    # Common programming language keywords for detection
    LANGUAGE_KEYWORDS = {
        "python": {
            "def",
            "class",
            "import",
            "from",
            "return",
            "if",
            "elif",
            "else",
            "for",
            "while",
            "try",
            "except",
            "with",
            "lambda",
            "yield",
            "async",
            "await",
        },
        "javascript": {
            "function",
            "const",
            "let",
            "var",
            "return",
            "if",
            "else",
            "for",
            "while",
            "class",
            "import",
            "export",
            "async",
            "await",
            "=>",
        },
        "java": {
            "public",
            "private",
            "protected",
            "class",
            "interface",
            "void",
            "int",
            "String",
            "return",
            "if",
            "else",
            "for",
            "while",
            "try",
            "catch",
        },
        "go": {
            "func",
            "package",
            "import",
            "var",
            "const",
            "type",
            "struct",
            "interface",
            "return",
            "if",
            "else",
            "for",
            "range",
            "defer",
            "go",
        },
        "rust": {
            "fn",
            "let",
            "mut",
            "pub",
            "struct",
            "enum",
            "impl",
            "trait",
            "use",
            "mod",
            "return",
            "if",
            "else",
            "for",
            "while",
            "match",
        },
        "typescript": {
            "function",
            "const",
            "let",
            "var",
            "interface",
            "type",
            "class",
            "return",
            "if",
            "else",
            "for",
            "while",
            "import",
            "export",
            "async",
            "await",
        },
    }

    def __init__(self, language: str = "", strict: bool = False) -> None:
        """
        Initialize CodeBlockExtractor.

        Args:
            language: Specific language to extract (e.g., 'python', 'javascript').
                     Empty string means extract any code block.
            strict: If True, only extract fenced code blocks.
                   If False, attempt to detect unfenced code. Default is False.
        """
        self.language = language.lower() if language else ""
        self.strict = strict

    def extract(self, raw_text: str) -> str:
        """
        Extract code block from raw text.

        Strategies:
        1. Extract from markdown fenced code blocks (```language...```)
        2. If not strict mode, detect unfenced code using heuristics

        Args:
            raw_text: Raw string that may contain code blocks

        Returns:
            Extracted code as string

        Raises:
            ValueError: If code block cannot be extracted
            TypeError: If input is not a string
        """
        # Input validation
        if not isinstance(raw_text, str):
            raise TypeError(f"Expected string input, got {type(raw_text).__name__}")

        if not raw_text or not raw_text.strip():
            raise ValueError("Cannot extract code from empty or whitespace-only string")

        text = raw_text.strip()

        # Strategy 1: Try to extract fenced code
        code = self._extract_fenced_code(text)
        if code:
            return code

        # Strategy 2: If not strict mode, try to detect unfenced code
        if not self.strict:
            if self._looks_like_code(text):
                # The entire text might be code
                return text

        raise ValueError(
            "Could not extract code block from the provided text. "
            "The text may not contain a code block, or you may need to disable strict mode."
        )

    def _extract_fenced_code(self, text: str) -> str:
        """
        Extract code from markdown fences.

        Args:
            text: Text that may contain fenced code blocks

        Returns:
            Extracted code or empty string if not found
        """
        # If language is specified, try to find blocks with that language
        if self.language:
            code = self._extract_by_language(text, self.language)
            if code:
                return code

        # Try generic code fence extraction
        code = self._extract_generic_fence(text)
        if code:
            return code

        return ""

    def _extract_by_language(self, text: str, language: str) -> str:
        """
        Extract code block with specific language identifier.

        Args:
            text: Text to search
            language: Language identifier

        Returns:
            Extracted code or empty string
        """
        # Try exact match (case-insensitive)
        patterns = [
            rf"```{re.escape(language)}\s*\n(.*?)```",
            rf"```{re.escape(language.upper())}\s*\n(.*?)```",
            rf"```{re.escape(language.capitalize())}\s*\n(.*?)```",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.IGNORECASE)
            if matches:
                # Return the first match
                return matches[0].strip()

        return ""

    def _extract_generic_fence(self, text: str) -> str:
        """
        Extract code from generic fenced blocks.

        Args:
            text: Text to search

        Returns:
            Extracted code or empty string
        """
        # Pattern for any fenced code block
        pattern = r"```(?:\w+)?\s*\n(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            # Return the first match
            return matches[0].strip()

        # Try without newline after opening fence
        pattern = r"```(?:\w+)?(.*?)```"
        matches = re.findall(pattern, text, re.DOTALL)

        if matches:
            return matches[0].strip()

        return ""

    def _looks_like_code(self, text: str) -> bool:
        """
        Heuristic to determine if text looks like code.

        Checks for:
        - Programming language keywords
        - Common code symbols and patterns
        - Indentation patterns
        - Comment patterns

        Args:
            text: Text to check

        Returns:
            True if text looks like code
        """
        if not text:
            return False

        # If language is specified, check for language-specific patterns
        if self.language and self.language in self.LANGUAGE_KEYWORDS:
            if self._contains_language_keywords(text, self.language):
                return True

        # General code indicators
        code_score = 0

        # Check for common code symbols (weight: 1 point each)
        code_symbols = [
            r"[{}\[\]();]",  # Braces, brackets, parentheses
            r"[=<>!]=",  # Comparison operators
            r"[+\-*/]=",  # Compound assignment
            r"=>",  # Arrow function
            r"->",  # Pointer/arrow
            r"::",  # Scope resolution
        ]

        for pattern in code_symbols:
            if re.search(pattern, text):
                code_score += 1

        # Check for keywords (weight: 2 points)
        keyword_patterns = [
            r"\b(?:def|class|function|const|let|var)\s+\w+",
            r"\b(?:import|from|export|require)\s+",
            r"\b(?:if|else|elif|for|while|switch|case)\s*\(",
            r"\b(?:return|yield|await|async)\s+",
        ]

        for pattern in keyword_patterns:
            if re.search(pattern, text):
                code_score += 2

        # Check for comments (weight: 1 point)
        comment_patterns = [
            r"^\s*#.*$",  # Python, Ruby, etc.
            r"^\s*//.*$",  # C-style
            r"/\*.*?\*/",  # Multi-line C-style
        ]

        for pattern in comment_patterns:
            if re.search(pattern, text, re.MULTILINE):
                code_score += 1

        # Check for indentation (weight: 1 point)
        lines = text.split("\n")
        indented_lines = sum(1 for line in lines if line.startswith(("    ", "\t")))
        if indented_lines >= len(lines) * 0.3:  # 30% of lines are indented
            code_score += 1

        # Threshold: score >= 3 suggests code
        return code_score >= 3

    def _contains_language_keywords(self, text: str, language: str) -> bool:
        """
        Check if text contains keywords from specific language.

        Args:
            text: Text to check
            language: Programming language

        Returns:
            True if language keywords are found
        """
        if language not in self.LANGUAGE_KEYWORDS:
            return False

        keywords = self.LANGUAGE_KEYWORDS[language]
        keyword_count = 0

        for keyword in keywords:
            # Use word boundary for exact matches
            pattern = rf"\b{re.escape(keyword)}\b"
            if re.search(pattern, text):
                keyword_count += 1
                if keyword_count >= 2:  # At least 2 keywords
                    return True

        return False

    def extract_all_blocks(self, raw_text: str) -> List[Dict[str, str]]:
        """
        Extract all code blocks from text.

        Returns metadata for each block including language and content.

        Args:
            raw_text: Raw text that may contain multiple code blocks

        Returns:
            List of dictionaries with 'language' and 'code' keys

        Raises:
            TypeError: If input is not a string
        """
        if not isinstance(raw_text, str):
            raise TypeError(f"Expected string input, got {type(raw_text).__name__}")

        blocks = []

        # Pattern to find all fenced code blocks with language
        pattern = r"```([\w+-]*)\s*\n(.*?)```"
        matches = re.finditer(pattern, raw_text, re.DOTALL)

        for match in matches:
            language = match.group(1).strip() or "unknown"
            code = match.group(2).strip()
            if code:
                blocks.append({"language": language, "code": code})

        return blocks

    def get_supported_languages(self) -> Set[str]:
        """
        Get set of languages with keyword detection support.

        Returns:
            Set of supported language names
        """
        return set(self.LANGUAGE_KEYWORDS.keys())

    def detect_language(self, code: str) -> Optional[str]:
        """
        Attempt to detect the programming language of code.

        Args:
            code: Code string to analyze

        Returns:
            Detected language name or None if uncertain
        """
        if not code:
            return None

        # Count keyword matches for each language
        language_scores = {}

        for language, keywords in self.LANGUAGE_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                pattern = rf"\b{re.escape(keyword)}\b"
                matches = re.findall(pattern, code)
                score += len(matches)

            if score > 0:
                language_scores[language] = score

        if not language_scores:
            return None

        # Return language with highest score
        detected = max(language_scores.items(), key=lambda x: x[1])

        # Only return if score is meaningful (at least 2 keywords)
        return detected[0] if detected[1] >= 2 else None
