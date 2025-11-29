# Architecture Documentation

This document provides a detailed overview of the architecture and code structure of `llm-content-extractor`.

## Project Structure

```
llm-content-extractor/
├── llm_content_extractor/          # Main package directory
│   ├── __init__.py                 # Package entry point, exports public API
│   ├── base.py                     # Abstract base classes and shared functionality
│   ├── extractor.py                # Main API interface and registration mechanism
│   └── strategies/                 # Directory for strategy implementations
│       ├── __init__.py             # Exports strategies
│       ├── json_extractor.py       # JSON extraction strategy
│       ├── xml_extractor.py        # XML extraction strategy
│       ├── html_extractor.py       # HTML extraction strategy
│       └── code_extractor.py       # Code block extraction strategy
├── tests/                          # Test directory
│   ├── __init__.py
│   ├── test_json_extractor.py      # Tests for JSON extractor
│   └── test_other_extractors.py    # Tests for other extractors
├── examples/                       # Example code
│   ├── basic_usage.py              # Basic usage examples
│   └── advanced_usage.py           # Advanced feature examples
├── docs/                           # Documentation directory
│   ├── PUBLISHING.md               # PyPI publishing guide
│   └── ARCHITECTURE.md             # This document
├── pyproject.toml                  # Poetry configuration file
├── README.md                       # Project overview
├── CHANGELOG.md                    # Version change history
└── LICENSE                         # MIT License
```

## Design Patterns

### Strategy Pattern

The project employs the Strategy Pattern to implement extraction logic for different content types:

```
ContentExtractor (Abstract Base Class)
    │
    ├── JSONExtractor       - JSON extraction strategy
    ├── XMLExtractor        - XML extraction strategy
    ├── HTMLExtractor       - HTML extraction strategy
    └── CodeBlockExtractor  - Code block extraction strategy
```

**Advantages:**
- **Open-Closed Principle**: Open for extension, closed for modification.
- **Single Responsibility**: Each strategy class is responsible for only one content type.
- **Easy to Test**: Each strategy can be tested independently.
- **Flexibility**: New extractors can be added or existing ones replaced easily.

### Registration Mechanism

The `register_extractor()` function allows users to register custom extractors:

```python
def register_extractor(content_type: ContentType, extractor_class: type) -> None:
    """Register a custom extractor."""
    _EXTRACTORS[content_type] = extractor_class
```

This enables users to:
1. Override default extractors.
2. Add support for new content types.
3. Customize extraction logic.

## Core Components

### 1. `base.py` - Abstract Base Class

Defines the interface and shared functionality for all extractors:

```python
class ContentExtractor(ABC):
    @abstractmethod
    def extract(self, raw_text: str) -> Union[str, Any]:
        """Core method for content extraction."""
        pass

    def _remove_markdown_fence(self, text: str, language: str = "") -> str:
        """Shared method to remove Markdown code fences."""
        pass
```

**Responsibilities:**
- Define the extractor interface.
- Provide common utilities (like removing Markdown fences).
- Ensure consistency across all strategies.

### 2. `extractor.py` - Main API

Provides a simple functional interface:

```python
def extract(
    raw_text: str,
    content_type: Union[ContentType, str],
    language: str = "",
    extractor: ContentExtractor = None,
) -> Union[str, Any]:
    """The main extraction function."""
    pass
```

**Responsibilities:**
- Unified entry point.
- Strategy selection and instantiation.
- Type conversion and validation.
- Error handling.

### 3. `strategies/` - Strategy Implementations

Each strategy is implemented in a separate file, providing:

#### JSONExtractor (`json_extractor.py`)

**Features:**
- Multiple fault-tolerance strategies (Markdown fences, embedded JSON, balanced brackets).
- Automatic fixing of common errors (trailing commas).
- Strict mode option.
- Detailed error messages.

**Core Methods:**
```python
def extract(self, raw_text: str) -> Union[Dict, List]:
    """Extract JSON, applying multiple fault-tolerance strategies."""

def _extract_balanced(self, text: str, open_char: str, close_char: str) -> str:
    """Extract content between balanced brackets/braces."""

def _fix_common_errors(self, json_text: str) -> str:
    """Fix common LLM errors."""
```

#### XMLExtractor (`xml_extractor.py`)

**Features:**
- Validation using `lxml` (if available).
- Recovery mode for malformed XML.
- Security enhancements (disabling entity expansion and network access).
- Support for XML declarations and fragments.

**Core Methods:**
```python
def extract(self, raw_text: str) -> str:
    """Extract and validate XML."""

def _validate_and_clean_xml(self, xml_text: str) -> str:
    """Validate and potentially recover XML."""

def is_valid_xml(self, xml_text: str) -> bool:
    """Check XML validity."""
```

#### HTMLExtractor (`html_extractor.py`)

**Features:**
- Extraction of full documents and fragments.
- Optional cleaning and normalization.
- Support for extracting multiple HTML fragments.
- Multiple strategies for DOCTYPE, full documents, and fragments.

**Core Methods:**
```python
def extract(self, raw_text: str) -> str:
    """Extract HTML."""

def extract_all_fragments(self, raw_text: str) -> List[str]:
    """Extract all HTML fragments."""

def is_valid_html(self, html_text: str) -> bool:
    """Check HTML validity."""
```

#### CodeBlockExtractor (`code_extractor.py`)

**Features:**
- Keyword detection for 6+ programming languages.
- Automatic language detection.
- Extraction of all code blocks with metadata.
- Strict mode (fenced only) vs. heuristic detection.
- Code scoring system.

**Core Methods:**
```python
def extract(self, raw_text: str) -> str:
    """Extract a code block."""

def detect_language(self, code: str) -> Optional[str]:
    """Detect the programming language."""

def extract_all_blocks(self, raw_text: str) -> List[Dict[str, str]]:
    """Extract all code blocks with metadata."""

def get_supported_languages(self) -> Set[str]:
    """Get the list of supported languages."""
```

## Robustness by Design

### Input Validation

All extractors perform strict input validation:

```python
# Type checking
if not isinstance(raw_text, str):
    raise TypeError(f"Expected string input, got {type(raw_text).__name__}")

# Null/empty check
if not raw_text or not raw_text.strip():
    raise ValueError("Cannot extract from empty or whitespace-only string")
```

### Error Handling

Each extractor provides detailed error information:

```python
# JSON parsing error
raise ValueError(f"JSON parsing failed: {e.msg} at position {e.pos}")

# XML validation error
raise ValueError(f"Invalid XML syntax: {e.msg} at line {e.lineno}, column {e.offset}")
```

### Multi-Strategy Approach

Extractors try multiple strategies in order of priority:

1. **Direct Parsing** - The fastest path.
2. **Fence Removal & Parsing** - Handles Markdown.
3. **Embedded Content Extraction** - Finds content within text.
4. **Common Error Fixing** - Fault-tolerance mode.
5. **Heuristic Detection** - Last-ditch effort.

### Security Considerations

- **XML**: Disables entity expansion (prevents XXE attacks).
- **XML**: Disables network access.
- **All**: Strict input validation.
- **All**: Defensive programming.

## Extension Guide

### Adding a New Extractor

1. **Create a new strategy file**:
```python
# llm_content_extractor/strategies/my_extractor.py
from llm_content_extractor.base import ContentExtractor

class MyExtractor(ContentExtractor):
    def extract(self, raw_text: str):
        # Implement extraction logic
        pass
```

2. **Export it in `strategies/__init__.py`**:
```python
from llm_content_extractor.strategies.my_extractor import MyExtractor

__all__ = [..., "MyExtractor"]
```

3. **Register it with the system** (optional):
```python
from llm_content_extractor import ContentType, register_extractor

# Add a new content type
class ContentType(Enum):
    MY_TYPE = "my_type"

# Register the extractor
register_extractor(ContentType.MY_TYPE, MyExtractor)
```

### Customizing an Existing Extractor

```python
from llm_content_extractor.strategies import JSONExtractor

class CustomJSONExtractor(JSONExtractor):
    def _fix_common_errors(self, json_text: str) -> str:
        # Custom error-fixing logic
        json_text = super()._fix_common_errors(json_text)
        # Add additional fixes
        return json_text
```

## Testing Strategy

### Test Organization

- `test_json_extractor.py` - Comprehensive tests for the JSON extractor.
- `test_other_extractors.py` - Tests for XML, HTML, and code block extractors.

### Test Coverage

- **Unit Tests**: Core functionality of each strategy.
- **Integration Tests**: End-to-end tests through the main API.
- **Edge Cases**: Empty input, malformed content, special characters.
- **Error Handling**: Validation of exceptions and error messages.

### Running Tests

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=llm_content_extractor

# Verbose output
poetry run pytest -v
```

## Performance Considerations

### Optimization Strategies

1. **Fast Path First**: Try direct parsing first.
2. **Lazy Imports**: `lxml` is imported only when needed.
3. **Early Return**: Return immediately once valid content is found.
4. **Avoid Redundant Processing**: Cache intermediate results.

### Time Complexity

- **JSON Extraction**: O(n), where n is the text length.
- **XML/HTML Extraction**: O(n) for regex matching, O(n) for parsing.
- **Code Block Extraction**: O(n) for pattern matching.

## Dependency Management

### Core Dependencies

- **`lxml`** (optional): For XML/HTML validation and parsing.
  - Falls back to regex-only methods if not available.

### Development Dependencies

- **`pytest`**: Testing framework.
- **`pytest-cov`**: Coverage reporting.
- **`black`**: Code formatter.
- **`mypy`**: Type checker.
- **`ruff`**: Fast linter.

## Version Compatibility

- **Python**: 3.8+
- **Backward Compatibility**: API changes follow Semantic Versioning.

## Best Practices

### Code Style

- Follows PEP 8.
- Formatted with Black (line length 100).
- Full type annotations.
- Detailed docstrings.

### Documentation

- Docstrings for all public APIs.
- Explanations of parameters and return values.
- Usage examples.
- Exception details.

### Error Handling

- Use specific exception types.
- Provide detailed error messages.
- Include debugging information (position, line number, etc.).

## Future Improvements

### Planned Features

1. **More Format Support**:
   - YAML extraction
   - TOML extraction
   - Markdown table extraction

2. **Performance Optimizations**:
   - Parallel processing of multiple extraction requests.
   - Compiled regex caching.

3. **Enhanced Functionality**:
   - Streaming for large files.
   - Partial content extraction.
   - Custom repair rules.

### Contribution Guide

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch.
3. Add tests.
4. Ensure all tests pass.
5. Submit a Pull Request.

## Reference Resources

- [Strategy Pattern](https://refactoring.guru/design-patterns/strategy)
- [Python Type Annotations](https://docs.python.org/3/library/typing.html)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [lxml Documentation](https://lxml.de/)
