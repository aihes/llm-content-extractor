"""Advanced usage examples demonstrating robustness features."""

from llm_content_extractor import extract, ContentType
from llm_content_extractor.strategies import (
    JSONExtractor,
    XMLExtractor,
    HTMLExtractor,
    CodeBlockExtractor,
)


def json_robustness_examples() -> None:
    """Demonstrate JSON extractor robustness features."""
    print("=" * 60)
    print("JSON Extractor - Robustness Features")
    print("=" * 60)

    # Example 1: Strict mode (disable auto-fixing)
    print("\n1. Strict vs Non-strict Mode:")
    malformed_json = '{"key": "value",}'  # Trailing comma

    # Non-strict mode (default) - auto-fixes the error
    extractor_lenient = JSONExtractor(strict=False)
    try:
        result = extractor_lenient.extract(malformed_json)
        print(f"   Lenient mode: {result}")  # Success
    except ValueError as e:
        print(f"   Lenient mode failed: {e}")

    # Strict mode - raises error
    extractor_strict = JSONExtractor(strict=True)
    try:
        result = extractor_strict.extract(malformed_json)
        print(f"   Strict mode: {result}")
    except ValueError as e:
        print(f"   Strict mode error: {e}")

    # Example 2: Detailed error messages
    print("\n2. Detailed Error Messages:")
    invalid_json = '{"key": invalid}'
    try:
        extract(invalid_json, ContentType.JSON)
    except ValueError as e:
        print(f"   Error: {e}")

    # Example 3: Array vs Object priority based on order
    print("\n3. Extraction Priority (first occurrence):")
    text_array_first = '[1, 2, 3] and {"key": "value"}'
    text_object_first = '{"key": "value"} and [1, 2, 3]'

    result1 = extract(text_array_first, ContentType.JSON)
    result2 = extract(text_object_first, ContentType.JSON)

    print(f"   Array first: {result1}")
    print(f"   Object first: {result2}")


def xml_robustness_examples() -> None:
    """Demonstrate XML extractor robustness features."""
    print("\n" + "=" * 60)
    print("XML Extractor - Robustness Features")
    print("=" * 60)

    # Example 1: Validation and recovery
    print("\n1. XML Validation and Recovery:")
    malformed_xml = "<root><item>Unclosed tag"

    # With recovery enabled (default)
    extractor_recover = XMLExtractor(validate=True, recover=True)
    try:
        result = extractor_recover.extract(malformed_xml)
        print(f"   With recovery: Success (might auto-close tags)")
    except ValueError as e:
        print(f"   With recovery failed: {e}")

    # Without recovery
    extractor_strict = XMLExtractor(validate=True, recover=False)
    try:
        result = extractor_strict.extract(malformed_xml)
        print(f"   Without recovery: {result}")
    except ValueError as e:
        print(f"   Strict validation error: {e}")

    # Example 2: Valid XML check
    print("\n2. XML Validation Helper:")
    valid_xml = "<root><item>Valid</item></root>"
    invalid_xml = "<root><item>Invalid"

    extractor = XMLExtractor()
    print(f"   Is valid (good XML): {extractor.is_valid_xml(valid_xml)}")
    print(f"   Is valid (bad XML): {extractor.is_valid_xml(invalid_xml)}")


def html_robustness_examples() -> None:
    """Demonstrate HTML extractor robustness features."""
    print("\n" + "=" * 60)
    print("HTML Extractor - Robustness Features")
    print("=" * 60)

    # Example 1: Clean HTML
    print("\n1. HTML Cleaning:")
    messy_html = '<div  class="test"  >  <p>Content</p>  </div>'

    # Without cleaning
    extractor_normal = HTMLExtractor(clean=False)
    result1 = extractor_normal.extract(messy_html)
    print(f"   Without cleaning: {result1}")

    # With cleaning (normalizes structure)
    extractor_clean = HTMLExtractor(clean=True)
    result2 = extractor_clean.extract(messy_html)
    print(f"   With cleaning: {result2}")

    # Example 2: Extract multiple fragments
    print("\n2. Extract All HTML Fragments:")
    multi_html = """
    First fragment: <div>First</div>
    Second fragment: <span>Second</span>
    Third fragment: <p>Third</p>
    """

    extractor = HTMLExtractor()
    fragments = extractor.extract_all_fragments(multi_html)
    print(f"   Found {len(fragments)} fragments:")
    for i, fragment in enumerate(fragments, 1):
        print(f"     {i}. {fragment}")


def code_robustness_examples() -> None:
    """Demonstrate code extractor robustness features."""
    print("\n" + "=" * 60)
    print("Code Block Extractor - Robustness Features")
    print("=" * 60)

    # Example 1: Language detection
    print("\n1. Automatic Language Detection:")
    python_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

    javascript_code = """
const fibonacci = (n) => {
    if (n <= 1) return n;
    return fibonacci(n-1) + fibonacci(n-2);
};
"""

    extractor = CodeBlockExtractor()
    lang1 = extractor.detect_language(python_code)
    lang2 = extractor.detect_language(javascript_code)

    print(f"   Detected for first snippet: {lang1}")
    print(f"   Detected for second snippet: {lang2}")

    # Example 2: Extract all code blocks with metadata
    print("\n2. Extract Multiple Code Blocks:")
    multi_code = """
    Here's some Python:
    ```python
    print("Hello")
    ```

    And some JavaScript:
    ```javascript
    console.log("World");
    ```

    And some generic code:
    ```
    generic code here
    ```
    """

    blocks = extractor.extract_all_blocks(multi_code)
    print(f"   Found {len(blocks)} code blocks:")
    for block in blocks:
        print(f"     Language: {block['language']}")
        print(f"     Code: {block['code'][:30]}...")

    # Example 3: Strict vs non-strict mode
    print("\n3. Strict Mode (fenced only vs heuristic):")
    unfenced_code = """
def hello():
    print("This has no fence")
"""

    # Non-strict mode (default) - detects unfenced code
    extractor_lenient = CodeBlockExtractor(strict=False)
    try:
        result = extractor_lenient.extract(unfenced_code)
        print(f"   Lenient mode: Detected code")
    except ValueError as e:
        print(f"   Lenient mode: {e}")

    # Strict mode - requires fences
    extractor_strict = CodeBlockExtractor(strict=True)
    try:
        result = extractor_strict.extract(unfenced_code)
        print(f"   Strict mode: {result}")
    except ValueError as e:
        print(f"   Strict mode: Requires fenced blocks")

    # Example 4: Supported languages
    print("\n4. Supported Languages for Detection:")
    supported = extractor.get_supported_languages()
    print(f"   Languages: {', '.join(sorted(supported))}")


def error_handling_examples() -> None:
    """Demonstrate comprehensive error handling."""
    print("\n" + "=" * 60)
    print("Error Handling Examples")
    print("=" * 60)

    # Example 1: Type checking
    print("\n1. Input Type Validation:")
    try:
        extract(123, ContentType.JSON)  # type: ignore
    except TypeError as e:
        print(f"   Type error: {e}")

    # Example 2: Empty input handling
    print("\n2. Empty Input Handling:")
    try:
        extract("   ", ContentType.JSON)
    except ValueError as e:
        print(f"   Empty input error: {e}")

    # Example 3: Invalid content type
    print("\n3. Invalid Content Type:")
    try:
        extract('{"key": "value"}', "invalid_type")  # type: ignore
    except ValueError as e:
        print(f"   Invalid type error: {e}")


def main() -> None:
    """Run all advanced examples."""
    json_robustness_examples()
    xml_robustness_examples()
    html_robustness_examples()
    code_robustness_examples()
    error_handling_examples()

    print("\n" + "=" * 60)
    print("All advanced examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
