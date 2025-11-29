# LLM Content Extractor

## 简介

`llm-content-extractor` 是一个用于从大语言模型（LLM）生成的文本中准确提取特定格式内容的工具。在与大语言模型交互时，我们经常会遇到生成内容中夹杂着多余的文本、解释或代码块标记。此工具旨在解决这一问题，帮助开发者轻松地提取出干净、格式正确的 JSON、XML、Markdown 或 HTML 内容。

## 功能特性

- **多种格式支持**: 支持从文本中提取 JSON、XML、Markdown 和 HTML。
- **高精度提取**: 能够处理并清除 LLM 生成内容中常见的多余字符和标记。
- **简单易用**: 提供简洁的 API，只需输入字符串即可获得提取后的内容。
- **可扩展性**: 易于扩展，未来可以支持更多格式的提取。

## 安装

```bash
# pip install llm-content-extractor
```

## 使用方法

以下是如何使用 `llm-content-extractor` 的基本示例：

```python
from llm_content_extractor import Extractor

# 包含 JSON 的示例文本
raw_text = """
这是 LLM 返回的一些文本。

```json
{
  "name": "llm-content-extractor",
  "version": "0.1.0",
  "description": "一个从文本中提取内容的工具"
}
```

希望这个 JSON 对你有帮助！
"""

# 提取 JSON 内容
try:
    json_content = Extractor.extract_json(raw_text)
    print(json_content)
except ValueError as e:
    print(e)
```

## 示例

### 提取 XML

```python
raw_text = """
这是一个 XML 示例：

<?xml version="1.0" encoding="UTF-8"?>
<note>
  <to>User</to>
  <from>LLM</from>
  <heading>Reminder</heading>
  <body>这是一个 XML 内容!</body>
</note>
"""
xml_content = Extractor.extract_xml(raw_text)
print(xml_content)
```

### 提取 Markdown

```python
raw_text = """
这里是一些 Markdown 内容：

---
### 这是一个标题

- 列表项 1
- 列表项 2

---
"""
markdown_content = Extractor.extract_markdown(raw_text)
print(markdown_content)
```

## 贡献

欢迎任何形式的贡献！如果你有好的想法或建议，请随时提交 Pull Request 或创建 Issue。

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 许可证

本项目使用 MIT 许可证。有关详细信息，请参阅 `LICENSE` 文件。
