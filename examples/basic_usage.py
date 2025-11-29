"""Basic usage examples for llm-content-extractor."""

from llm_content_extractor import extract, ContentType


def json_examples() -> None:
    """Examples of JSON extraction."""
    print("=" * 50)
    print("JSON Extraction Examples")
    print("=" * 50)

    # Example 1: JSON with markdown fence
    text1 = """
Here's the configuration you requested:
```json
{
    "database": {
        "host": "localhost",
        "port": 5432,
        "name": "mydb"
    },
    "debug": true
}
```
Hope this helps!
"""
    result1 = extract(text1, ContentType.JSON)
    print("\n1. JSON with markdown fence:")
    print(f"   Result: {result1}")

    # Example 2: JSON with trailing comma
    text2 = '{"users": ["alice", "bob",], "count": 2,}'
    result2 = extract(text2, ContentType.JSON)
    print("\n2. JSON with trailing commas (auto-fixed):")
    print(f"   Input:  {text2}")
    print(f"   Result: {result2}")

    # Example 3: JSON embedded in text
    text3 = 'The API returned: {"status": "success", "data": [1, 2, 3]} - all done!'
    result3 = extract(text3, ContentType.JSON)
    print("\n3. JSON embedded in text:")
    print(f"   Result: {result3}")


def xml_examples() -> None:
    """Examples of XML extraction."""
    print("\n" + "=" * 50)
    print("XML Extraction Examples")
    print("=" * 50)

    # Example 1: XML with markdown fence
    text1 = """
```xml
<?xml version="1.0" encoding="UTF-8"?>
<config>
    <database>
        <host>localhost</host>
        <port>5432</port>
    </database>
    <debug>true</debug>
</config>
```
"""
    result1 = extract(text1, ContentType.XML)
    print("\n1. XML with markdown fence:")
    print(f"   Result:\n{result1}")


def html_examples() -> None:
    """Examples of HTML extraction."""
    print("\n" + "=" * 50)
    print("HTML Extraction Examples")
    print("=" * 50)

    # Example 1: HTML fragment
    text1 = """
Here's the HTML snippet:
```html
<div class="card">
    <h2>Title</h2>
    <p>This is some content.</p>
</div>
```
"""
    result1 = extract(text1, ContentType.HTML)
    print("\n1. HTML fragment:")
    print(f"   Result:\n{result1}")


def code_examples() -> None:
    """Examples of code block extraction."""
    print("\n" + "=" * 50)
    print("Code Block Extraction Examples")
    print("=" * 50)

    # Example 1: Python code
    text1 = """
Here's a Python function:
```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Test the function
print(fibonacci(10))
```
"""
    result1 = extract(text1, ContentType.CODE, language="python")
    print("\n1. Python code:")
    print(f"   Result:\n{result1}")

    # Example 2: JavaScript code
    text2 = """
```javascript
const greet = (name) => {
    console.log(`Hello, ${name}!`);
};

greet("World");
```
"""
    result2 = extract(text2, ContentType.CODE, language="javascript")
    print("\n2. JavaScript code:")
    print(f"   Result:\n{result2}")


def advanced_example() -> None:
    """Advanced usage with custom extractors."""
    print("\n" + "=" * 50)
    print("Advanced Example: Using Extractor Classes")
    print("=" * 50)

    from llm_content_extractor import JSONExtractor

    # Create extractor instance
    json_extractor = JSONExtractor()

    # Use directly
    text = '{"message": "Hello", "items": [1, 2, 3,]}'
    result = json_extractor.extract(text)
    print(f"\nDirect extractor usage:")
    print(f"   Input:  {text}")
    print(f"   Result: {result}")


def main() -> None:
    """Run all examples."""
    json_examples()
    xml_examples()
    html_examples()
    code_examples()
    advanced_example()

    print("\n" + "=" * 50)
    print("All examples completed!")
    print("=" * 50)


if __name__ == "__main__":
    main()
