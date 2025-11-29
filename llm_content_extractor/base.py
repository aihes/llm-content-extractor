"""Base classes and interfaces for content extraction strategies."""

from abc import ABC, abstractmethod
from typing import Any, Union


class ContentExtractor(ABC):
    """Abstract base class for content extraction strategies."""

    @abstractmethod
    def extract(self, raw_text: str) -> Union[str, Any]:
        """
        Extract and parse content from raw LLM output.

        Args:
            raw_text: Raw string output from LLM

        Returns:
            Cleaned string or parsed Python object (e.g., dict for JSON)

        Raises:
            ValueError: If content cannot be extracted or parsed
        """
        pass

    def _remove_markdown_fence(self, text: str, language: str = "") -> str:
        """
        Remove markdown code fence markers.

        Args:
            text: Text that may contain markdown fences
            language: Expected language identifier (e.g., 'json', 'xml')

        Returns:
            Text with fences removed
        """
        text = text.strip()

        # Try to find code block with specified language
        if language:
            markers = [f"```{language}", f"```{language.upper()}"]
            for marker in markers:
                if text.startswith(marker):
                    text = text[len(marker):].lstrip()
                    break

        # Remove generic code fence
        if text.startswith("```"):
            # Find the end of the first line (language identifier)
            newline_idx = text.find("\n")
            if newline_idx != -1:
                text = text[newline_idx + 1:]

        # Remove trailing fence
        if text.endswith("```"):
            text = text[:-3].rstrip()

        return text.strip()
