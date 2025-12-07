# 🚀 LLM Content Extractor - Promotional Content

## 📱 Social Media Posts

### Twitter/X Post (Short Version)

```
🔥 Tired of messy LLM outputs?

Introducing LLM Content Extractor - the robust Python library that extracts clean JSON, XML, HTML & code from LLM responses!

✅ Auto-fixes trailing commas
✅ Handles markdown fences
✅ Extracts embedded content
✅ 68% test coverage

pip install llm-content-extractor

#Python #LLM #AI #OpenSource
```

### LinkedIn Post (Professional Version)

```
🎯 Solving a Common Problem in LLM Applications

If you're building applications with Large Language Models, you've probably encountered this frustration:

LLMs return messy outputs - JSON wrapped in markdown code fences, trailing commas, mixed with explanatory text. Parsing these responses becomes a nightmare.

I'm excited to share LLM Content Extractor - an open-source Python library that solves this problem elegantly.

🔑 Key Features:
• Fault-tolerant extraction of JSON, XML, HTML, and code blocks
• Automatically handles markdown fences (```json ... ```)
• Fixes common LLM errors (trailing commas, malformed structures)
• Strategy pattern for easy extension
• Full type safety with comprehensive type annotations
• 68% test coverage with 34 passing tests

💡 Real-World Example:
Instead of writing complex regex patterns to extract JSON from:
"Here's the data: ```json\n{"items": [1,2,3,],}\n```"

Simply use:
extract(text, ContentType.JSON)  # Returns: {'items': [1, 2, 3]}

🎨 Built with Best Practices:
• Strategy Pattern for extensibility
• Strict mode for production environments
• Language detection for code blocks (Python, JS, Java, Go, Rust, TypeScript)
• Security-hardened XML parsing (XXE prevention)
• Multiple extraction strategies with intelligent fallbacks

Perfect for:
- RAG (Retrieval-Augmented Generation) pipelines
- LLM-powered automation tools
- AI agent frameworks
- Data extraction from LLM responses

⚡ Get Started:
pip install llm-content-extractor

📚 Full documentation, examples, and source code available on GitHub.

#Python #MachineLearning #AI #LLM #OpenSource #SoftwareEngineering
```

---

## 📝 Blog Post / Article (Long Form)

# Stop Wrestling with LLM Outputs: Introducing LLM Content Extractor

## The Problem Every LLM Developer Faces

If you've worked with Large Language Models like GPT-4, Claude, or Llama, you know the struggle:

You ask the model for JSON data, and it returns:
```
Sure! Here's the JSON you requested:
```json
{
    "status": "success",
    "items": [1, 2, 3,],
}
```
Hope this helps!
```

Now you need to:
1. Strip the markdown code fence
2. Remove the explanatory text
3. Fix the trailing comma (invalid JSON!)
4. Hope nothing else is broken

Multiply this by thousands of API calls, and you have a maintenance nightmare.

## The Solution: LLM Content Extractor

**LLM Content Extractor** is a robust Python library designed specifically for this problem. It extracts clean, parsed content from messy LLM outputs with minimal code.

### ⚡ Quick Example

```python
from llm_content_extractor import extract, ContentType

# Messy LLM output
llm_response = '''
Here's your data:
```json
{"name": "Alice", "scores": [95, 87, 92,]}
```
'''

# One line to extract clean data
data = extract(llm_response, ContentType.JSON)
# Returns: {'name': 'Alice', 'scores': [95, 87, 92]}
```

### 🎯 Key Features

#### 1. **Fault Tolerance**
- Automatically removes markdown code fences
- Fixes trailing commas (the #1 LLM JSON error)
- Extracts content embedded in explanatory text
- Handles both `JSON` and `json` fence identifiers

#### 2. **Multiple Content Types**
- **JSON**: Parse objects and arrays
- **XML**: Validate and extract XML structures
- **HTML**: Clean and extract HTML fragments
- **Code Blocks**: Extract code with language detection

#### 3. **Intelligent Extraction**
```python
# Works with embedded content
text = 'The result is: {"status": "ok"} - done!'
extract(text, ContentType.JSON)  # Finds and extracts the JSON

# Works with malformed JSON
text = '{"items": [1, 2, 3,],}'
extract(text, ContentType.JSON)  # Auto-fixes trailing commas
```

#### 4. **Advanced Features**

**Strict Mode** for production:
```python
from llm_content_extractor.strategies import JSONExtractor

# Disable auto-fixing for strict validation
extractor = JSONExtractor(strict=True)
data = extractor.extract(llm_output)
```

**Language Detection** for code:
```python
from llm_content_extractor.strategies import CodeBlockExtractor

extractor = CodeBlockExtractor()
language = extractor.detect_language(code)  # 'python', 'javascript', etc.
```

**XML Validation** with security:
```python
from llm_content_extractor.strategies import XMLExtractor

# Validates and recovers from malformed XML
# Security: Disables entity expansion (XXE prevention)
extractor = XMLExtractor(validate=True, recover=True)
xml_data = extractor.extract(llm_output)
```

### 🏗️ Architecture

Built with the **Strategy Pattern** for extensibility:

```
ContentExtractor (Base Class)
    ├── JSONExtractor - Fault-tolerant JSON parsing
    ├── XMLExtractor - Secure XML validation
    ├── HTMLExtractor - HTML fragment extraction
    └── CodeBlockExtractor - Multi-language code detection
```

Want to add YAML support? Just create a new strategy:

```python
from llm_content_extractor.base import ContentExtractor

class YAMLExtractor(ContentExtractor):
    def extract(self, raw_text: str):
        # Your YAML extraction logic
        pass

# Register it
register_extractor(ContentType.YAML, YAMLExtractor)
```

### 🧪 Production-Ready

- **68% Test Coverage**: 34 passing tests
- **Type Safety**: Full type annotations for IDE support
- **Well Documented**: Comprehensive API reference and examples
- **Modern Python**: Supports Python 3.8+
- **Zero Dependencies**: Optional `lxml` for advanced XML/HTML features

### 💼 Use Cases

**1. RAG Pipelines**
Extract structured data from LLM responses in retrieval-augmented generation systems.

**2. AI Agents**
Parse tool calls and structured outputs from autonomous agents.

**3. Data Extraction**
Clean and standardize LLM-generated content in data pipelines.

**4. Testing**
Validate LLM outputs in your test suites.

### 🚀 Getting Started

Install via pip:
```bash
pip install llm-content-extractor
```

Or with Poetry:
```bash
poetry add llm-content-extractor
```

Basic usage:
```python
from llm_content_extractor import extract, ContentType

# Extract JSON
result = extract(llm_output, ContentType.JSON)

# Extract code
code = extract(llm_output, ContentType.CODE, language='python')

# Extract XML
xml = extract(llm_output, ContentType.XML)
```

### 📚 Learn More

- **GitHub**: [aihes/llm-content-extractor](https://github.com/aihes/llm-content-extractor)
- **Documentation**: See README for full API reference
- **Examples**: Check the `examples/` directory for advanced usage

### 🤝 Contributing

Contributions welcome! The project uses:
- Poetry for dependency management
- Pytest for testing
- Black for formatting
- Full type annotations with mypy

### 📄 License

MIT License - free for personal and commercial use.

---

## 🎬 Call to Action

**Try it today:**
```bash
pip install llm-content-extractor
```

**Star on GitHub** if you find it useful! ⭐

**Share your use case** - I'd love to hear how you're using it!

---

### Hashtags for Social Media

`#Python #LLM #MachineLearning #AI #OpenSource #GPT4 #Claude #RAG #AIEngineering #DevTools #Parsing #NLP #SoftwareEngineering #Developer #Coding`
