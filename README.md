# LLM Content Extractor

[![Python Version](https://img.shields.io/pypi/pyversions/llm-content-extractor)](https://pypi.org/project/llm-content-extractor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A robust content extractor for LLM outputs with support for extracting and parsing JSON, XML, HTML, and code blocks from raw strings.

## ✨ Features

- 🎯 **Multiple Format Support**: Extract JSON, XML, HTML, and code blocks
- 🛡️ **Fault Tolerant**:
  - Automatically handle Markdown code fences (\`\`\`json ... \`\`\`)
  - Intelligently extract content embedded in text
  - Fix common LLM errors (e.g., trailing commas in JSON)
- 🏗️ **Strategy Pattern**: Easy to extend with custom extractors
- 📦 **Simple API**: Functional interface, ready to use
- 🧪 **Well Tested**: High test coverage for reliability
- 🔧 **Type Safe**: Full type annotations support

## 📦 Installation

Install with pip:

```bash
pip install llm-content-extractor
```

Install with Poetry:

```bash
poetry add llm-content-extractor
```

## 🚀 Quick Start

### Basic Usage

```python
from llm_content_extractor import extract, ContentType

# Extract JSON
json_text = '''
Here's the data you requested:
```json
{
    "name": "Alice",
    "age": 30,
    "hobbies": ["reading", "coding"],
}
```
'''

result = extract(json_text, ContentType.JSON)
print(result)  # {'name': 'Alice', 'age': 30, 'hobbies': ['reading', 'coding']}
```

### JSON Extraction Examples

```python
from llm_content_extractor import extract, ContentType

# 1. JSON with Markdown fence
text1 = '```json\n{"status": "success"}\n```'
extract(text1, ContentType.JSON)  # {'status': 'success'}

# 2. Plain JSON
text2 = '{"status": "success"}'
extract(text2, ContentType.JSON)  # {'status': 'success'}

# 3. JSON embedded in text
text3 = 'The result is: {"status": "success"} - done!'
extract(text3, ContentType.JSON)  # {'status': 'success'}

# 4. JSON with trailing commas (common LLM error)
text4 = '{"items": [1, 2, 3,],}'
extract(text4, ContentType.JSON)  # {'items': [1, 2, 3]}

# 5. Using string content type
extract(text1, "json")  # Also works
```

### XML Extraction Examples

Given text containing a fenced XML block:
```text
A response from the LLM:
```xml
<root>
    <item id="1">First</item>
    <item id="2">Second</item>
</root>
```
```

You can extract it with:
```python
from llm_content_extractor import extract, ContentType

# Assuming the text above is in a variable `xml_text`
result = extract(xml_text, ContentType.XML)
print(result)  # Returns cleaned XML string
```

### HTML Extraction Examples

Given text containing a fenced HTML block:
```text
LLM says:
```html
<div class="container">
    <h1>Title</h1>
    <p>Content here</p>
</div>
```
```

You can extract it with:
```python
from llm_content_extractor import extract, ContentType

# Assuming the text above is in a variable `html_text`
result = extract(html_text, ContentType.HTML)
print(result)  # Returns cleaned HTML string
```

### Code Block Extraction Examples

**1. Extract language-specific code**

Given a Python code block:
```text
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
```
```

Extract it by specifying the language:
```python
from llm_content_extractor import extract, ContentType

# Assuming the text above is in a variable `python_code_text`
code = extract(python_code_text, ContentType.CODE, language='python')
print(code)
# Output:
# def greet(name):
#     return f"Hello, {name}!"
#
# print(greet("World"))
```

**2. Extract any code block**

Given a generic code block (no language specified):
```text
```
const x = 42;
console.log(x);
```
```

Extract it without specifying a language:
```python
# Assuming the text above is in a variable `generic_code_text`
code = extract(generic_code_text, ContentType.CODE)
print(code)  # const x = 42;\nconsole.log(x);
```

## 🎨 Advanced Usage

### Using Extractor Classes Directly

```python
from llm_content_extractor import JSONExtractor, XMLExtractor

# Use extractor classes directly
json_extractor = JSONExtractor()
result = json_extractor.extract('{"key": "value"}')

xml_extractor = XMLExtractor()
result = xml_extractor.extract('<root><item>test</item></root>')
```

### Custom Extractors

Create custom extractors by inheriting from the `ContentExtractor` base class:

```python
from llm_content_extractor.base import ContentExtractor
from llm_content_extractor import extract, ContentType, register_extractor
import json

class CustomJSONExtractor(ContentExtractor):
    def extract(self, raw_text: str):
        # Custom extraction logic
        cleaned = raw_text.strip()
        # ... your logic here
        return json.loads(cleaned)

# Register custom extractor
register_extractor(ContentType.JSON, CustomJSONExtractor)

# Use the custom extractor
result = extract(text, ContentType.JSON)
```

### Using Custom Extractor Instances

```python
from llm_content_extractor import extract, JSONExtractor

# Create a custom configured extractor
my_extractor = JSONExtractor(strict=True)

# Pass the extractor instance directly
result = extract(raw_text, ContentType.JSON, extractor=my_extractor)
```

## 🧪 Fault Tolerance Features

LLM Content Extractor handles various common issues in LLM outputs:

### 1. Markdown Code Fences

```python
# ✅ Supports various fence formats
extract('```json\n{"a": 1}\n```', ContentType.JSON)
extract('```JSON\n{"a": 1}\n```', ContentType.JSON)  # Uppercase
extract('```\n{"a": 1}\n```', ContentType.JSON)      # No language identifier
```

### 2. Embedded Content

```python
# ✅ Extract content from surrounding text
text = '''
Here is the configuration:
{"enabled": true, "timeout": 30}
This will set the timeout to 30 seconds.
'''
extract(text, ContentType.JSON)  # Successfully extracts
```

### 3. JSON Syntax Error Fixing

```python
# ✅ Automatically fix trailing commas
extract('{"items": [1, 2,],}', ContentType.JSON)  # {'items': [1, 2]}
extract('[{"id": 1,}, {"id": 2,}]', ContentType.JSON)  # [{'id': 1}, {'id': 2}]
```

### 4. Nested Structures

```python
# ✅ Handle complex nested structures
nested = {
    "user": {
        "profile": {
            "name": "Alice",
            "contacts": ["email", "phone"]
        }
    }
}
# Fully supported
```

## 🏗️ Architecture

This project uses the **Strategy Pattern**:

```
ContentExtractor (Abstract Base Class)
    ├── JSONExtractor
    ├── XMLExtractor
    ├── HTMLExtractor
    └── CodeBlockExtractor
```

This design provides:
- ✅ Easy to add new extractor types
- ✅ Single responsibility for each extractor
- ✅ Flexible replacement and extension of extraction logic

## 📚 API Reference

### `extract(raw_text, content_type, language="", extractor=None)`

Main extraction function.

**Parameters:**
- `raw_text` (str): Raw string output from LLM
- `content_type` (ContentType | str): Content type (JSON, XML, HTML, CODE)
- `language` (str, optional): For CODE type, specify the programming language
- `extractor` (ContentExtractor, optional): Custom extractor instance

**Returns:**
- JSON: `dict` or `list`
- XML/HTML/CODE: `str`

**Raises:**
- `ValueError`: If valid content cannot be extracted
- `TypeError`: If an invalid extractor is provided

### `ContentType` Enum

```python
class ContentType(Enum):
    JSON = "json"
    XML = "xml"
    HTML = "html"
    CODE = "code"
```

### Extractor Options

#### JSONExtractor

```python
JSONExtractor(strict=False)
```
- `strict`: If True, disable auto-fixing of errors like trailing commas

#### XMLExtractor

```python
XMLExtractor(validate=True, recover=True)
```
- `validate`: If True and lxml is available, validate XML syntax
- `recover`: If True, attempt to recover from malformed XML

#### HTMLExtractor

```python
HTMLExtractor(validate=False, clean=False)
```
- `validate`: If True, validate HTML structure
- `clean`: If True, clean and normalize HTML

#### CodeBlockExtractor

```python
CodeBlockExtractor(language="", strict=False)
```
- `language`: Specific language to extract (e.g., 'python', 'javascript')
- `strict`: If True, only extract fenced code blocks

## 🔧 Development

### Setup

```bash
# Clone the repository
git clone https://github.com/aihes/llm-content-extractor.git
cd llm-content-extractor

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Format code
poetry run black .

# Type checking
poetry run mypy llm_content_extractor
```

### Running Tests

```bash
# Run all tests
poetry run pytest

# With coverage report
poetry run pytest --cov=llm_content_extractor --cov-report=html

# Run specific tests
poetry run pytest tests/test_json_extractor.py
```

## 📖 Publishing to PyPI

See [docs/PUBLISHING.md](docs/PUBLISHING.md) for detailed publishing instructions.

Quick steps:

```bash
# 1. Update version
poetry version patch

# 2. Build
poetry build

# 3. Publish
poetry publish
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Use Cases

LLM Content Extractor is particularly useful for:

- 🤖 **LLM Application Development**: Extract structured data from model outputs
- 🔄 **Data Pipelines**: Clean and standardize AI-generated content
- 🧪 **Testing Tools**: Validate LLM output formats
- 📊 **Data Processing**: Batch process LLM responses

## ❓ FAQ

**Q: Why is my JSON extraction failing?**

A: Ensure the text contains valid JSON structure. This library tries multiple strategies, but cannot recover completely corrupted JSON.

**Q: Can I extract multiple code blocks?**

A: The current version extracts the first matching code block. To extract multiple blocks, use the `extract_all_blocks()` method on `CodeBlockExtractor` or call the function multiple times.

**Q: Is there support for other formats?**

A: Yes! You can add support for new formats by inheriting from `ContentExtractor` and registering it in the system.

**Q: How do I enable strict mode?**

A: Use the extractor classes directly:
```python
extractor = JSONExtractor(strict=True)
result = extractor.extract(text)
```

## 🌟 Advanced Features

### Language Detection

```python
from llm_content_extractor.strategies import CodeBlockExtractor

extractor = CodeBlockExtractor()
code = "def hello(): return 'world'"
language = extractor.detect_language(code)  # Returns 'python'
```

### Extract All Code Blocks

```python
from llm_content_extractor.strategies import CodeBlockExtractor

extractor = CodeBlockExtractor()
blocks = extractor.extract_all_blocks(multi_code_text)
for block in blocks:
    print(f"{block['language']}: {block['code']}")
```

### Validate XML/HTML

```python
from llm_content_extractor.strategies import XMLExtractor, HTMLExtractor

xml_extractor = XMLExtractor()
is_valid = xml_extractor.is_valid_xml(xml_string)

html_extractor = HTMLExtractor()
is_valid = html_extractor.is_valid_html(html_string)
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - Detailed architecture documentation
- [Publishing Guide](docs/PUBLISHING.md) - How to publish to PyPI
- [Examples](examples/) - Usage examples

## 🙏 Acknowledgments

Thanks to all contributors and developers using this project!

## 📬 Contact

- Report Issues: [GitHub Issues](https://github.com/aihes/llm-content-extractor/issues)
- Feature Requests: [GitHub Discussions](https://github.com/aihes/llm-content-extractor/discussions)

---

If this project helps you, please consider giving it a ⭐️!
