"""Tests for XML, HTML, and Code extraction functionality."""

import pytest

from llm_content_extractor import extract, ContentType


class TestXMLExtractor:
    """Test cases for XMLExtractor."""

    def test_extract_simple_xml(self) -> None:
        """Test extracting simple XML."""
        raw_text = '<root><item>Hello</item></root>'
        result = extract(raw_text, ContentType.XML)
        assert result == '<root><item>Hello</item></root>'

    def test_extract_xml_with_markdown_fence(self) -> None:
        """Test extracting XML wrapped in markdown."""
        raw_text = '```xml\n<root><item>World</item></root>\n```'
        result = extract(raw_text, ContentType.XML)
        assert result == '<root><item>World</item></root>'

    def test_extract_xml_with_declaration(self) -> None:
        """Test extracting XML with declaration."""
        raw_text = '<?xml version="1.0"?>\n<root><item>Test</item></root>'
        result = extract(raw_text, ContentType.XML)
        assert '<?xml version="1.0"?>' in result
        assert '<root><item>Test</item></root>' in result

    def test_extract_xml_embedded_in_text(self) -> None:
        """Test extracting XML from surrounding text."""
        raw_text = 'Here is the XML: <root><data>value</data></root> - done!'
        result = extract(raw_text, ContentType.XML)
        assert '<root><data>value</data></root>' in result

    def test_invalid_xml_raises_error(self) -> None:
        """Test that text without XML raises ValueError."""
        raw_text = "This is not XML!"
        with pytest.raises(ValueError, match="Could not extract valid XML"):
            extract(raw_text, ContentType.XML)


class TestHTMLExtractor:
    """Test cases for HTMLExtractor."""

    def test_extract_simple_html(self) -> None:
        """Test extracting simple HTML."""
        raw_text = '<div>Hello World</div>'
        result = extract(raw_text, ContentType.HTML)
        assert result == '<div>Hello World</div>'

    def test_extract_html_with_markdown_fence(self) -> None:
        """Test extracting HTML wrapped in markdown."""
        raw_text = '```html\n<p>Test paragraph</p>\n```'
        result = extract(raw_text, ContentType.HTML)
        assert result == '<p>Test paragraph</p>'

    def test_extract_full_html_document(self) -> None:
        """Test extracting full HTML document."""
        raw_text = '''
        <!DOCTYPE html>
        <html>
        <head><title>Test</title></head>
        <body><p>Content</p></body>
        </html>
        '''
        result = extract(raw_text, ContentType.HTML)
        assert '<!DOCTYPE html>' in result
        assert '<html>' in result
        assert '<p>Content</p>' in result

    def test_extract_html_embedded_in_text(self) -> None:
        """Test extracting HTML from surrounding text."""
        raw_text = 'The HTML is: <div><span>text</span></div> - end'
        result = extract(raw_text, ContentType.HTML)
        assert '<div><span>text</span></div>' in result

    def test_invalid_html_raises_error(self) -> None:
        """Test that text without HTML raises ValueError."""
        raw_text = "This is plain text with no HTML tags!"
        with pytest.raises(ValueError, match="Could not extract valid HTML"):
            extract(raw_text, ContentType.HTML)


class TestCodeBlockExtractor:
    """Test cases for CodeBlockExtractor."""

    def test_extract_python_code(self) -> None:
        """Test extracting Python code."""
        raw_text = '''```python
def hello():
    print("Hello, World!")
```'''
        result = extract(raw_text, ContentType.CODE, language='python')
        assert 'def hello():' in result
        assert 'print("Hello, World!")' in result

    def test_extract_javascript_code(self) -> None:
        """Test extracting JavaScript code."""
        raw_text = '''```javascript
function add(a, b) {
    return a + b;
}
```'''
        result = extract(raw_text, ContentType.CODE, language='javascript')
        assert 'function add(a, b)' in result
        assert 'return a + b;' in result

    def test_extract_any_code_block(self) -> None:
        """Test extracting any code block without language specification."""
        raw_text = '''```
const x = 42;
console.log(x);
```'''
        result = extract(raw_text, ContentType.CODE)
        assert 'const x = 42;' in result
        assert 'console.log(x);' in result

    def test_extract_code_without_fence(self) -> None:
        """Test extracting code that looks like code but has no fence."""
        raw_text = '''def calculate(x, y):
    return x + y'''
        result = extract(raw_text, ContentType.CODE)
        assert 'def calculate(x, y):' in result
        assert 'return x + y' in result

    def test_extract_code_with_symbols(self) -> None:
        """Test extracting code with various symbols."""
        raw_text = '''```
const arr = [1, 2, 3];
const obj = {key: "value"};
```'''
        result = extract(raw_text, ContentType.CODE)
        assert 'const arr = [1, 2, 3];' in result
        assert 'const obj = {key: "value"};' in result

    def test_invalid_code_raises_error(self) -> None:
        """Test that plain text raises ValueError."""
        raw_text = "This is just plain English text without any code patterns."
        with pytest.raises(ValueError, match="Could not extract code block"):
            extract(raw_text, ContentType.CODE)


class TestExtractAPI:
    """Test cases for the main extract API."""

    def test_string_content_type(self) -> None:
        """Test using string for content_type parameter."""
        raw_text = '{"key": "value"}'
        result = extract(raw_text, "json")
        assert result == {"key": "value"}

    def test_invalid_content_type_string(self) -> None:
        """Test invalid string content_type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid content_type"):
            extract("test", "invalid_type")

    def test_invalid_extractor_type(self) -> None:
        """Test invalid extractor type raises TypeError."""
        with pytest.raises(TypeError, match="must be an instance of ContentExtractor"):
            extract("test", ContentType.JSON, extractor="not_an_extractor")  # type: ignore
