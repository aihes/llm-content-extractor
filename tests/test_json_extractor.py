"""Tests for JSON extraction functionality."""

import pytest

from llm_content_extractor import extract, ContentType, JSONExtractor


class TestJSONExtractor:
    """Test cases for JSONExtractor."""

    def test_extract_simple_json(self) -> None:
        """Test extracting simple JSON object."""
        raw_text = '{"name": "Alice", "age": 30}'
        result = extract(raw_text, ContentType.JSON)
        assert result == {"name": "Alice", "age": 30}

    def test_extract_json_with_markdown_fence(self) -> None:
        """Test extracting JSON wrapped in markdown code fence."""
        raw_text = '```json\n{"name": "Bob", "age": 25}\n```'
        result = extract(raw_text, ContentType.JSON)
        assert result == {"name": "Bob", "age": 25}

    def test_extract_json_with_uppercase_fence(self) -> None:
        """Test extracting JSON with uppercase language identifier."""
        raw_text = '```JSON\n{"name": "Charlie", "age": 35}\n```'
        result = extract(raw_text, ContentType.JSON)
        assert result == {"name": "Charlie", "age": 35}

    def test_extract_json_array(self) -> None:
        """Test extracting JSON array."""
        raw_text = '[1, 2, 3, 4, 5]'
        result = extract(raw_text, ContentType.JSON)
        assert result == [1, 2, 3, 4, 5]

    def test_extract_json_with_trailing_comma(self) -> None:
        """Test extracting JSON with trailing comma (common LLM error)."""
        raw_text = '{"name": "Dave", "items": [1, 2, 3,],}'
        result = extract(raw_text, ContentType.JSON)
        assert result == {"name": "Dave", "items": [1, 2, 3]}

    def test_extract_json_embedded_in_text(self) -> None:
        """Test extracting JSON embedded in surrounding text."""
        raw_text = 'Here is the data: {"status": "success", "count": 42} - that\'s all!'
        result = extract(raw_text, ContentType.JSON)
        assert result == {"status": "success", "count": 42}

    def test_extract_nested_json(self) -> None:
        """Test extracting nested JSON structure."""
        raw_text = '''
        ```json
        {
            "user": {
                "name": "Eve",
                "address": {
                    "city": "New York",
                    "zip": "10001"
                }
            },
            "active": true
        }
        ```
        '''
        result = extract(raw_text, ContentType.JSON)
        assert result == {
            "user": {
                "name": "Eve",
                "address": {
                    "city": "New York",
                    "zip": "10001"
                }
            },
            "active": True
        }

    def test_extract_json_with_special_characters(self) -> None:
        """Test extracting JSON with special characters in strings."""
        raw_text = r'{"message": "Hello \"world\"", "emoji": "😀"}'
        result = extract(raw_text, ContentType.JSON)
        assert result == {"message": 'Hello "world"', "emoji": "😀"}

    def test_extract_json_without_fence_in_text(self) -> None:
        """Test extracting JSON without fence from text with explanation."""
        raw_text = '''
        The configuration should be:
        {
            "enabled": true,
            "timeout": 30
        }
        This will set the timeout to 30 seconds.
        '''
        result = extract(raw_text, ContentType.JSON)
        assert result == {"enabled": True, "timeout": 30}

    def test_invalid_json_raises_error(self) -> None:
        """Test that invalid JSON raises ValueError."""
        raw_text = "This is not JSON at all!"
        with pytest.raises(ValueError, match="Could not extract valid JSON"):
            extract(raw_text, ContentType.JSON)

    def test_empty_string_raises_error(self) -> None:
        """Test that empty string raises ValueError."""
        with pytest.raises(ValueError, match="Could not extract valid JSON"):
            extract("", ContentType.JSON)

    def test_extract_json_array_with_trailing_comma(self) -> None:
        """Test extracting array with trailing comma."""
        raw_text = '[{"id": 1,}, {"id": 2,},]'
        result = extract(raw_text, ContentType.JSON)
        assert result == [{"id": 1}, {"id": 2}]

    def test_extract_json_with_generic_fence(self) -> None:
        """Test extracting JSON from generic code fence."""
        raw_text = '```\n{"key": "value"}\n```'
        result = extract(raw_text, ContentType.JSON)
        assert result == {"key": "value"}

    def test_direct_extractor_usage(self) -> None:
        """Test using JSONExtractor directly."""
        extractor = JSONExtractor()
        result = extractor.extract('{"direct": true}')
        assert result == {"direct": True}

    def test_extract_with_custom_extractor(self) -> None:
        """Test using custom extractor instance."""
        custom_extractor = JSONExtractor()
        result = extract('{"custom": true}', ContentType.JSON, extractor=custom_extractor)
        assert result == {"custom": True}
