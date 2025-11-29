# LLM Content Extractor

[![Python Version](https://img.shields.io/pypi/pyversions/llm-content-extractor)](https://pypi.org/project/llm-content-extractor/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

一个强大的 LLM 输出内容提取器，支持从 LLM 返回的原始字符串中提取和解析 JSON、XML、HTML 和代码块。

## ✨ 特性

- 🎯 **多格式支持**：支持 JSON、XML、HTML 和代码块提取
- 🛡️ **容错能力强**：
  - 自动处理 Markdown 代码围栏（\`\`\`json ... \`\`\`）
  - 智能提取嵌入在文本中的内容
  - 修复常见的 LLM 错误（如 JSON 尾部逗号）
- 🏗️ **设计模式**：基于策略模式，易于扩展
- 📦 **简单易用**：函数式接口，开箱即用
- 🧪 **充分测试**：高测试覆盖率，保证质量
- 🔧 **类型安全**：完整的类型注解支持

## 📦 安装

使用 pip 安装：

```bash
pip install llm-content-extractor
```

使用 Poetry 安装：

```bash
poetry add llm-content-extractor
```

## 🚀 快速开始

### 基本用法

```python
from llm_content_extractor import extract, ContentType

# 提取 JSON
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

### JSON 提取示例

```python
from llm_content_extractor import extract, ContentType

# 1. 带 Markdown 围栏的 JSON
text1 = '```json\n{"status": "success"}\n```'
extract(text1, ContentType.JSON)  # {'status': 'success'}

# 2. 纯 JSON
text2 = '{"status": "success"}'
extract(text2, ContentType.JSON)  # {'status': 'success'}

# 3. 嵌入在文本中的 JSON
text3 = 'The result is: {"status": "success"} - done!'
extract(text3, ContentType.JSON)  # {'status': 'success'}

# 4. 带尾部逗号的 JSON（常见 LLM 错误）
text4 = '{"items": [1, 2, 3,],}'
extract(text4, ContentType.JSON)  # {'items': [1, 2, 3]}

# 5. 使用字符串类型参数
extract(text1, "json")  # 同样有效
```

### XML 提取示例

```python
from llm_content_extractor import extract, ContentType

xml_text = '''
```xml
<root>
    <item id="1">First</item>
    <item id="2">Second</item>
</root>
```
'''

result = extract(xml_text, ContentType.XML)
print(result)  # 返回清洗后的 XML 字符串
```

### HTML 提取示例

```python
from llm_content_extractor import extract, ContentType

html_text = '''
```html
<div class="container">
    <h1>Title</h1>
    <p>Content here</p>
</div>
```
'''

result = extract(html_text, ContentType.HTML)
print(result)  # 返回清洗后的 HTML 字符串
```

### 代码块提取示例

```python
from llm_content_extractor import extract, ContentType

# 提取特定语言的代码
python_code = '''
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
```
'''

code = extract(python_code, ContentType.CODE, language='python')
print(code)
# 输出：
# def greet(name):
#     return f"Hello, {name}!"
#
# print(greet("World"))

# 提取任意代码块
generic_code = '''
```
const x = 42;
console.log(x);
```
'''

code = extract(generic_code, ContentType.CODE)
print(code)  # const x = 42;\nconsole.log(x);
```

## 🎨 高级用法

### 使用策略类

```python
from llm_content_extractor import JSONExtractor, XMLExtractor

# 直接使用提取器类
json_extractor = JSONExtractor()
result = json_extractor.extract('{"key": "value"}')

xml_extractor = XMLExtractor()
result = xml_extractor.extract('<root><item>test</item></root>')
```

### 自定义提取器

通过继承 `ContentExtractor` 基类创建自定义提取器：

```python
from llm_content_extractor.base import ContentExtractor
from llm_content_extractor import extract, ContentType, register_extractor

class CustomJSONExtractor(ContentExtractor):
    def extract(self, raw_text: str):
        # 自定义提取逻辑
        cleaned = raw_text.strip()
        # ... 你的逻辑
        return json.loads(cleaned)

# 注册自定义提取器
register_extractor(ContentType.JSON, CustomJSONExtractor)

# 使用自定义提取器
result = extract(text, ContentType.JSON)
```

### 使用自定义提取器实例

```python
from llm_content_extractor import extract, JSONExtractor

# 创建自定义配置的提取器
my_extractor = JSONExtractor()

# 直接传入提取器实例
result = extract(raw_text, ContentType.JSON, extractor=my_extractor)
```

## 🧪 容错能力展示

LLM Content Extractor 能够处理多种常见的 LLM 输出问题：

### 1. Markdown 代码围栏

```python
# ✅ 支持各种围栏格式
extract('```json\n{"a": 1}\n```', ContentType.JSON)
extract('```JSON\n{"a": 1}\n```', ContentType.JSON)  # 大写
extract('```\n{"a": 1}\n```', ContentType.JSON)      # 无语言标识
```

### 2. 嵌入式内容

```python
# ✅ 从文本中提取内容
text = '''
Here is the configuration:
{"enabled": true, "timeout": 30}
This will set the timeout to 30 seconds.
'''
extract(text, ContentType.JSON)  # 成功提取
```

### 3. JSON 语法错误修复

```python
# ✅ 自动修复尾部逗号
extract('{"items": [1, 2,],}', ContentType.JSON)  # {'items': [1, 2]}
extract('[{"id": 1,}, {"id": 2,}]', ContentType.JSON)  # [{'id': 1}, {'id': 2}]
```

### 4. 嵌套结构

```python
# ✅ 处理复杂嵌套
nested = {
    "user": {
        "profile": {
            "name": "Alice",
            "contacts": ["email", "phone"]
        }
    }
}
# 完全支持
```

## 🏗️ 架构设计

本项目采用**策略模式**设计：

```
ContentExtractor (抽象基类)
    ├── JSONExtractor
    ├── XMLExtractor
    ├── HTMLExtractor
    └── CodeBlockExtractor
```

这种设计使得：
- ✅ 易于添加新的提取器类型
- ✅ 每个提取器职责单一，易于测试
- ✅ 可以灵活替换或扩展提取逻辑

## 📚 API 参考

### `extract(raw_text, content_type, language="", extractor=None)`

主要的提取函数。

**参数：**
- `raw_text` (str): LLM 返回的原始字符串
- `content_type` (ContentType | str): 内容类型（JSON, XML, HTML, CODE）
- `language` (str, optional): 对于 CODE 类型，指定编程语言
- `extractor` (ContentExtractor, optional): 自定义提取器实例

**返回：**
- JSON: `dict` 或 `list`
- XML/HTML/CODE: `str`

**异常：**
- `ValueError`: 无法提取有效内容
- `TypeError`: 提供了无效的提取器

### `ContentType` 枚举

```python
class ContentType(Enum):
    JSON = "json"
    XML = "xml"
    HTML = "html"
    CODE = "code"
```

## 🔧 开发

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/aihes/llm-content-extractor.git
cd llm-content-extractor

# 安装依赖
poetry install

# 运行测试
poetry run pytest

# 代码格式化
poetry run black .

# 类型检查
poetry run mypy llm_content_extractor
```

### 运行测试

```bash
# 运行所有测试
poetry run pytest

# 带覆盖率报告
poetry run pytest --cov=llm_content_extractor --cov-report=html

# 运行特定测试
poetry run pytest tests/test_json_extractor.py
```

## 📖 发布到 PyPI

详细的发布流程请参阅 [docs/PUBLISHING.md](docs/PUBLISHING.md)。

简要步骤：

```bash
# 1. 更新版本
poetry version patch

# 2. 构建
poetry build

# 3. 发布
poetry publish
```

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## 💡 使用场景

LLM Content Extractor 特别适用于：

- 🤖 LLM 应用开发：从模型输出中提取结构化数据
- 🔄 数据管道：清洗和标准化 AI 生成的内容
- 🧪 测试工具：验证 LLM 输出格式
- 📊 数据处理：批量处理 LLM 响应

## ❓ 常见问题

**Q: 为什么我的 JSON 提取失败？**

A: 确保文本中包含有效的 JSON 结构。本库会尝试多种策略，但如果 JSON 完全损坏则无法恢复。

**Q: 可以提取多个代码块吗？**

A: 当前版本提取第一个匹配的代码块。如需提取多个，请多次调用或实现自定义提取器。

**Q: 支持其他格式吗？**

A: 可以通过继承 `ContentExtractor` 并注册到系统中来添加新格式支持。

## 🙏 致谢

感谢所有贡献者和使用本项目的开发者！

## 📬 联系方式

- 问题反馈：[GitHub Issues](https://github.com/aihes/llm-content-extractor/issues)
- 功能请求：[GitHub Discussions](https://github.com/aihes/llm-content-extractor/discussions)

---

如果这个项目对你有帮助，请给个 ⭐️ 支持一下！
