"""Main API interface for content extraction."""

from enum import Enum
from typing import Any, Union

from llm_content_extractor.base import ContentExtractor
from llm_content_extractor.strategies import (
    JSONExtractor,
    XMLExtractor,
    HTMLExtractor,
    CodeBlockExtractor,
)


class ContentType(Enum):
    """Supported content types for extraction."""

    JSON = "json"
    XML = "xml"
    HTML = "html"
    CODE = "code"


# Registry of extractors
_EXTRACTORS = {
    ContentType.JSON: JSONExtractor,
    ContentType.XML: XMLExtractor,
    ContentType.HTML: HTMLExtractor,
    ContentType.CODE: CodeBlockExtractor,
}


def extract(
    raw_text: str,
    content_type: Union[ContentType, str],
    language: str = "",
    extractor: ContentExtractor = None,
) -> Union[str, Any]:
    """
    Extract and parse content from LLM output.

    This is the main entry point for the library. It provides a simple
    functional interface to extract various types of content from LLM outputs.

    Args:
        raw_text: Raw string output from LLM
        content_type: Type of content to extract (JSON, XML, HTML, CODE)
        language: For CODE type, specify the language (e.g., 'python', 'javascript')
        extractor: Optional custom extractor instance. If provided, content_type is ignored.

    Returns:
        - For JSON: Parsed dict or list
        - For XML/HTML/CODE: Cleaned string
        - For custom extractor: Whatever the extractor returns

    Raises:
        ValueError: If content cannot be extracted or invalid content_type
        TypeError: If invalid extractor provided

    Examples:
        >>> # Extract JSON
        >>> result = extract('```json\\n{"key": "value"}\\n```', ContentType.JSON)
        >>> print(result)  # {'key': 'value'}

        >>> # Extract Python code
        >>> code = extract('```python\\nprint("hello")\\n```', ContentType.CODE, language='python')
        >>> print(code)  # print("hello")

        >>> # Use custom extractor
        >>> custom = JSONExtractor()
        >>> result = extract(raw_text, ContentType.JSON, extractor=custom)
    """
    # If custom extractor provided, use it directly
    if extractor is not None:
        if not isinstance(extractor, ContentExtractor):
            raise TypeError("extractor must be an instance of ContentExtractor")
        return extractor.extract(raw_text)

    # Convert string to enum if needed
    if isinstance(content_type, str):
        try:
            content_type = ContentType(content_type.lower())
        except ValueError:
            valid_types = ", ".join([ct.value for ct in ContentType])
            raise ValueError(
                f"Invalid content_type: {content_type}. Valid types: {valid_types}"
            )

    # Get the appropriate extractor class
    extractor_class = _EXTRACTORS.get(content_type)
    if extractor_class is None:
        raise ValueError(f"No extractor available for content_type: {content_type}")

    # Create extractor instance
    if content_type == ContentType.CODE and language:
        extractor_instance = extractor_class(language=language)
    else:
        extractor_instance = extractor_class()

    # Extract content
    return extractor_instance.extract(raw_text)


def register_extractor(content_type: ContentType, extractor_class: type) -> None:
    """
    Register a custom extractor for a content type.

    This allows users to override default extractors or add support for new types.

    Args:
        content_type: The content type this extractor handles
        extractor_class: The extractor class (must inherit from ContentExtractor)

    Raises:
        TypeError: If extractor_class is not a subclass of ContentExtractor

    Example:
        >>> class MyJSONExtractor(ContentExtractor):
        ...     def extract(self, raw_text: str):
        ...         # Custom implementation
        ...         pass
        >>> register_extractor(ContentType.JSON, MyJSONExtractor)
    """
    if not issubclass(extractor_class, ContentExtractor):
        raise TypeError("extractor_class must be a subclass of ContentExtractor")

    _EXTRACTORS[content_type] = extractor_class
