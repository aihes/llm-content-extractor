# 🚀 LLM Content Extractor - 宣传文案

## 📱 社交媒体发布内容

### 微博/Twitter 短文案

```
🔥 LLM 输出太乱？一招搞定！

推荐一个超实用的 Python 库：LLM Content Extractor
专治 LLM 返回的混乱数据！

✅ 自动修复 JSON 尾部逗号
✅ 智能处理 Markdown 代码块
✅ 提取嵌入在文本中的内容
✅ 68% 测试覆盖率

一行代码解决问题：
pip install llm-content-extractor

#Python #LLM #AI #开源 #GPT #Claude
```

### 知乎/LinkedIn 专业文案

```
🎯 LLM 应用开发者的福音：彻底解决输出解析难题

如果你在开发 LLM 应用，一定遇到过这个头疼的问题：

LLM 返回的数据格式混乱——JSON 被包在 Markdown 代码块里，还有尾部逗号，混杂着大量解释性文字。解析这些响应简直是噩梦。

今天分享一个开源项目：**LLM Content Extractor**，优雅地解决了这个问题。

🔑 核心特性：
• 容错提取 JSON、XML、HTML 和代码块
• 自动处理 Markdown 围栏（```json ... ```）
• 修复常见 LLM 错误（尾部逗号、格式问题）
• 策略模式设计，易于扩展
• 完整的类型注解，开发体验极佳
• 68% 测试覆盖率，34 个测试全部通过

💡 实际案例：
不需要写复杂的正则表达式来处理：
"这是数据：```json\n{"items": [1,2,3,],}\n```"

只需一行代码：
extract(text, ContentType.JSON)  # 返回: {'items': [1, 2, 3]}

🎨 工程最佳实践：
• 策略模式架构，可扩展性强
• 严格模式支持生产环境
• 代码块语言检测（Python、JS、Java、Go、Rust、TypeScript）
• XML 解析安全加固（防 XXE 攻击）
• 多重提取策略，智能容错

🌟 适用场景：
- RAG（检索增强生成）数据管道
- LLM 自动化工具
- AI Agent 框架
- LLM 响应数据提取

⚡ 快速开始：
pip install llm-content-extractor

📚 完整文档、示例和源码都在 GitHub 上。

欢迎 Star ⭐ 和使用反馈！

#Python #机器学习 #人工智能 #LLM #开源 #软件工程 #GPT #Claude
```

---

## 📝 博客文章 / 长文案

# 告别 LLM 输出解析的痛苦：LLM Content Extractor 深度解析

## 每个 LLM 开发者都会遇到的问题

如果你使用过 GPT-4、Claude 或 Llama 等大语言模型，一定深有体会：

你向模型请求 JSON 数据，它却返回：
```
当然！这是您要的 JSON：
```json
{
    "status": "success",
    "items": [1, 2, 3,],
}
```
希望这能帮到您！
```

现在你需要：
1. 去掉 Markdown 代码围栏
2. 删除解释性文字
3. 修复尾部逗号（这是无效的 JSON！）
4. 祈祷没有其他问题

当这个过程重复成千上万次时，维护成本会变得非常高。

## 解决方案：LLM Content Extractor

**LLM Content Extractor** 是一个专为此问题设计的强大 Python 库。它能从混乱的 LLM 输出中提取干净、解析好的内容，只需极少的代码。

### ⚡ 快速示例

```python
from llm_content_extractor import extract, ContentType

# 混乱的 LLM 输出
llm_response = '''
这是您的数据：
```json
{"name": "张三", "scores": [95, 87, 92,]}
```
'''

# 一行代码提取干净数据
data = extract(llm_response, ContentType.JSON)
# 返回: {'name': '张三', 'scores': [95, 87, 92]}
```

### 🎯 核心功能

#### 1. **强大的容错能力**
- 自动移除 Markdown 代码围栏
- 修复尾部逗号（最常见的 LLM JSON 错误）
- 提取嵌入在解释性文字中的内容
- 同时处理 `JSON` 和 `json` 标识符

#### 2. **多种内容类型支持**
- **JSON**: 解析对象和数组
- **XML**: 验证和提取 XML 结构
- **HTML**: 清理和提取 HTML 片段
- **代码块**: 带语言检测的代码提取

#### 3. **智能提取**
```python
# 处理嵌入式内容
text = '结果是: {"status": "ok"} - 完成！'
extract(text, ContentType.JSON)  # 自动找到并提取 JSON

# 处理格式错误的 JSON
text = '{"items": [1, 2, 3,],}'
extract(text, ContentType.JSON)  # 自动修复尾部逗号
```

#### 4. **高级特性**

**严格模式**用于生产环境：
```python
from llm_content_extractor.strategies import JSONExtractor

# 禁用自动修复，进行严格验证
extractor = JSONExtractor(strict=True)
data = extractor.extract(llm_output)
```

**代码语言检测**：
```python
from llm_content_extractor.strategies import CodeBlockExtractor

extractor = CodeBlockExtractor()
language = extractor.detect_language(code)  # 'python', 'javascript' 等
```

**安全的 XML 验证**：
```python
from llm_content_extractor.strategies import XMLExtractor

# 验证并修复格式错误的 XML
# 安全特性：禁用实体扩展（防止 XXE 攻击）
extractor = XMLExtractor(validate=True, recover=True)
xml_data = extractor.extract(llm_output)
```

### 🏗️ 架构设计

采用**策略模式**，可扩展性强：

```
ContentExtractor（基类）
    ├── JSONExtractor - 容错 JSON 解析
    ├── XMLExtractor - 安全 XML 验证
    ├── HTMLExtractor - HTML 片段提取
    └── CodeBlockExtractor - 多语言代码检测
```

想添加 YAML 支持？只需创建新策略：

```python
from llm_content_extractor.base import ContentExtractor

class YAMLExtractor(ContentExtractor):
    def extract(self, raw_text: str):
        # 你的 YAML 提取逻辑
        pass

# 注册它
register_extractor(ContentType.YAML, YAMLExtractor)
```

### 🧪 生产就绪

- **68% 测试覆盖率**：34 个测试全部通过
- **类型安全**：完整的类型注解，IDE 支持极佳
- **文档完善**：详尽的 API 参考和示例
- **现代 Python**：支持 Python 3.8+
- **零依赖**：可选的 `lxml` 用于高级 XML/HTML 功能

### 💼 使用场景

**1. RAG 数据管道**
在检索增强生成系统中提取 LLM 响应的结构化数据。

**2. AI Agent**
解析自主代理的工具调用和结构化输出。

**3. 数据提取**
在数据管道中清理和标准化 LLM 生成的内容。

**4. 测试**
在测试套件中验证 LLM 输出。

### 🚀 快速开始

通过 pip 安装：
```bash
pip install llm-content-extractor
```

或使用 Poetry：
```bash
poetry add llm-content-extractor
```

基本用法：
```python
from llm_content_extractor import extract, ContentType

# 提取 JSON
result = extract(llm_output, ContentType.JSON)

# 提取代码
code = extract(llm_output, ContentType.CODE, language='python')

# 提取 XML
xml = extract(llm_output, ContentType.XML)
```

### 📚 了解更多

- **GitHub**: [aihes/llm-content-extractor](https://github.com/aihes/llm-content-extractor)
- **文档**: 查看 README 了解完整 API 参考
- **示例**: 查看 `examples/` 目录了解高级用法

### 🤝 贡献

欢迎贡献！项目使用：
- Poetry 进行依赖管理
- Pytest 进行测试
- Black 进行代码格式化
- mypy 完整类型注解

### 📄 许可证

MIT 许可证 - 可免费用于个人和商业用途。

---

## 🎬 行动号召

**立即试用：**
```bash
pip install llm-content-extractor
```

**觉得有用就在 GitHub 上点个 Star！** ⭐

**分享你的使用场景** - 我很想听听你是如何使用它的！

---

## 🎯 发布渠道建议

### 微博
- 使用短文案
- 配上代码示例截图
- 添加话题标签

### 知乎
- 发布长文案作为回答或文章
- 可以回答"如何优雅地处理 LLM 输出"类问题
- 添加技术细节和对比

### CSDN / 掘金 / 开源中国
- 发布完整博客文章
- 包含架构图和代码示例
- 强调工程实践

### B站 / 抖音
- 制作快速演示视频（2-3分钟）
- 展示前后对比
- 突出"一行代码搞定"的简洁性

### 微信公众号
- 长文案，增加更多使用场景
- 可以添加实际项目案例
- 包含完整代码示例

---

### 推荐话题标签

**中文：** `#Python #机器学习 #人工智能 #LLM #开源 #GPT #Claude #RAG #AI工程 #开发工具 #数据解析 #NLP #软件工程 #程序员 #编程`

**英文：** `#Python #MachineLearning #AI #LLM #OpenSource #GPT4 #Claude #RAG #AIEngineering #DevTools #Parsing #NLP #SoftwareEngineering #Developer #Coding`
