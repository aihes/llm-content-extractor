# 架构设计文档

本文档详细说明 `llm-content-extractor` 的架构设计和代码组织结构。

## 项目结构

```
llm-content-extractor/
├── llm_content_extractor/          # 主包目录
│   ├── __init__.py                 # 包入口，导出公共 API
│   ├── base.py                     # 抽象基类和共享功能
│   ├── extractor.py                # 主 API 接口和注册机制
│   └── strategies/                 # 策略实现包
│       ├── __init__.py             # 策略包导出
│       ├── json_extractor.py       # JSON 提取策略
│       ├── xml_extractor.py        # XML 提取策略
│       ├── html_extractor.py       # HTML 提取策略
│       └── code_extractor.py       # 代码块提取策略
├── tests/                          # 测试目录
│   ├── __init__.py
│   ├── test_json_extractor.py      # JSON 提取器测试
│   └── test_other_extractors.py    # 其他提取器测试
├── examples/                       # 示例代码
│   ├── basic_usage.py              # 基本使用示例
│   └── advanced_usage.py           # 高级功能示例
├── docs/                           # 文档目录
│   ├── PUBLISHING.md               # PyPI 发布指南
│   └── ARCHITECTURE.md             # 本文档
├── pyproject.toml                  # Poetry 配置文件
├── README.md                       # 项目说明
├── CHANGELOG.md                    # 版本变更记录
└── LICENSE                         # MIT 许可证
```

## 设计模式

### 策略模式 (Strategy Pattern)

项目采用策略模式实现不同内容类型的提取逻辑：

```
ContentExtractor (抽象基类)
    │
    ├── JSONExtractor       - JSON 提取策略
    ├── XMLExtractor        - XML 提取策略
    ├── HTMLExtractor       - HTML 提取策略
    └── CodeBlockExtractor  - 代码块提取策略
```

**优点：**
- **开放-封闭原则**：对扩展开放，对修改封闭
- **单一职责**：每个策略类只负责一种内容类型
- **易于测试**：每个策略可独立测试
- **灵活性**：可以轻松添加新的提取器或替换现有实现

### 注册机制

通过 `register_extractor()` 函数，用户可以注册自定义提取器：

```python
def register_extractor(content_type: ContentType, extractor_class: type) -> None:
    """注册自定义提取器"""
    _EXTRACTORS[content_type] = extractor_class
```

这允许用户：
1. 覆盖默认提取器
2. 添加新的内容类型支持
3. 自定义提取逻辑

## 核心组件

### 1. base.py - 抽象基类

定义了所有提取器的接口和共享功能：

```python
class ContentExtractor(ABC):
    @abstractmethod
    def extract(self, raw_text: str) -> Union[str, Any]:
        """提取内容的核心方法"""
        pass

    def _remove_markdown_fence(self, text: str, language: str = "") -> str:
        """移除 Markdown 代码围栏的共享方法"""
        pass
```

**职责：**
- 定义提取器接口
- 提供通用功能（如移除 Markdown 围栏）
- 确保所有策略的一致性

### 2. extractor.py - 主 API

提供简单的函数式接口：

```python
def extract(
    raw_text: str,
    content_type: Union[ContentType, str],
    language: str = "",
    extractor: ContentExtractor = None,
) -> Union[str, Any]:
    """主要的提取函数"""
    pass
```

**职责：**
- 统一的入口点
- 策略选择和实例化
- 类型转换和验证
- 错误处理

### 3. strategies/ - 策略实现

每个策略都在独立文件中实现，提供：

#### JSONExtractor (json_extractor.py)

**特性：**
- 多重容错策略（Markdown 围栏、嵌入式 JSON、括号平衡）
- 自动修复常见错误（尾部逗号）
- 严格模式选项
- 详细的错误信息

**核心方法：**
```python
def extract(self, raw_text: str) -> Union[Dict, List]:
    """提取 JSON，应用多重容错策略"""

def _extract_balanced(self, text: str, open_char: str, close_char: str) -> str:
    """提取平衡的括号/中括号内容"""

def _fix_common_errors(self, json_text: str) -> str:
    """修复常见 LLM 错误"""
```

#### XMLExtractor (xml_extractor.py)

**特性：**
- 使用 lxml 进行验证（如果可用）
- 恢复模式处理格式错误的 XML
- 安全性增强（禁用实体扩展和网络访问）
- 支持 XML 声明和片段

**核心方法：**
```python
def extract(self, raw_text: str) -> str:
    """提取并验证 XML"""

def _validate_and_clean_xml(self, xml_text: str) -> str:
    """验证并可能恢复 XML"""

def is_valid_xml(self, xml_text: str) -> bool:
    """检查 XML 有效性"""
```

#### HTMLExtractor (html_extractor.py)

**特性：**
- 提取完整文档和片段
- 可选的清理和规范化
- 支持提取多个 HTML 片段
- DOCTYPE、完整文档、片段的多重策略

**核心方法：**
```python
def extract(self, raw_text: str) -> str:
    """提取 HTML"""

def extract_all_fragments(self, raw_text: str) -> List[str]:
    """提取所有 HTML 片段"""

def is_valid_html(self, html_text: str) -> bool:
    """检查 HTML 有效性"""
```

#### CodeBlockExtractor (code_extractor.py)

**特性：**
- 支持 6+ 种编程语言的关键字检测
- 自动语言检测
- 提取所有代码块及元数据
- 严格模式（仅围栏）vs 启发式检测
- 代码评分系统

**核心方法：**
```python
def extract(self, raw_text: str) -> str:
    """提取代码块"""

def detect_language(self, code: str) -> Optional[str]:
    """检测编程语言"""

def extract_all_blocks(self, raw_text: str) -> List[Dict[str, str]]:
    """提取所有代码块及元数据"""

def get_supported_languages(self) -> Set[str]:
    """获取支持的语言列表"""
```

## 健壮性设计

### 输入验证

所有提取器都执行严格的输入验证：

```python
# 类型检查
if not isinstance(raw_text, str):
    raise TypeError(f"Expected string input, got {type(raw_text).__name__}")

# 空值检查
if not raw_text or not raw_text.strip():
    raise ValueError("Cannot extract from empty or whitespace-only string")
```

### 错误处理

每个提取器提供详细的错误信息：

```python
# JSON 解析错误
raise ValueError(f"JSON parsing failed: {e.msg} at position {e.pos}")

# XML 验证错误
raise ValueError(f"Invalid XML syntax: {e.msg} at line {e.lineno}, column {e.offset}")
```

### 多重策略

提取器按优先级尝试多种策略：

1. **直接解析** - 最快路径
2. **移除围栏后解析** - 处理 Markdown
3. **提取嵌入内容** - 从文本中查找
4. **修复常见错误** - 容错模式
5. **启发式检测** - 最后的尝试

### 安全性考虑

- **XML**: 禁用实体扩展（防止 XXE 攻击）
- **XML**: 禁用网络访问
- **所有**: 严格的输入验证
- **所有**: 防御性编程

## 扩展指南

### 添加新的提取器

1. **创建新策略文件**：
```python
# llm_content_extractor/strategies/my_extractor.py
from llm_content_extractor.base import ContentExtractor

class MyExtractor(ContentExtractor):
    def extract(self, raw_text: str):
        # 实现提取逻辑
        pass
```

2. **在 strategies/__init__.py 中导出**：
```python
from llm_content_extractor.strategies.my_extractor import MyExtractor

__all__ = [..., "MyExtractor"]
```

3. **注册到系统**（可选）：
```python
from llm_content_extractor import ContentType, register_extractor

# 添加新的内容类型
class ContentType(Enum):
    MY_TYPE = "my_type"

# 注册提取器
register_extractor(ContentType.MY_TYPE, MyExtractor)
```

### 自定义现有提取器

```python
from llm_content_extractor.strategies import JSONExtractor

class CustomJSONExtractor(JSONExtractor):
    def _fix_common_errors(self, json_text: str) -> str:
        # 自定义错误修复逻辑
        json_text = super()._fix_common_errors(json_text)
        # 添加额外的修复
        return json_text
```

## 测试策略

### 测试组织

- `test_json_extractor.py` - JSON 提取器的全面测试
- `test_other_extractors.py` - XML、HTML、代码块提取器测试

### 测试覆盖

- **单元测试**：每个策略的核心功能
- **集成测试**：通过主 API 的端到端测试
- **边界情况**：空输入、格式错误、特殊字符
- **错误处理**：验证异常和错误消息

### 运行测试

```bash
# 运行所有测试
poetry run pytest

# 带覆盖率
poetry run pytest --cov=llm_content_extractor

# 详细输出
poetry run pytest -v
```

## 性能考虑

### 优化策略

1. **快速路径优先**：先尝试直接解析
2. **惰性导入**：lxml 仅在需要时导入
3. **早期返回**：找到有效内容后立即返回
4. **避免重复处理**：缓存中间结果

### 时间复杂度

- **JSON 提取**：O(n)，其中 n 是文本长度
- **XML/HTML 提取**：O(n) 用于正则匹配，O(n) 用于解析
- **代码块提取**：O(n) 用于模式匹配

## 依赖管理

### 核心依赖

- **lxml** (可选)：XML/HTML 验证和解析
  - 如果不可用，退回到纯正则表达式方法

### 开发依赖

- **pytest**: 测试框架
- **pytest-cov**: 覆盖率报告
- **black**: 代码格式化
- **mypy**: 类型检查
- **ruff**: 快速 linter

## 版本兼容性

- **Python**: 3.8+
- **向后兼容**：API 变更遵循语义化版本

## 最佳实践

### 代码风格

- 遵循 PEP 8
- 使用 Black 格式化（行长度 100）
- 完整的类型注解
- 详细的 docstring

### 文档

- 所有公共 API 都有 docstring
- 参数和返回值说明
- 使用示例
- 异常说明

### 错误处理

- 使用特定的异常类型
- 提供详细的错误消息
- 包含调试信息（位置、行号等）

## 未来改进

### 计划功能

1. **更多格式支持**：
   - YAML 提取
   - TOML 提取
   - Markdown 表格提取

2. **性能优化**：
   - 并行处理多个提取请求
   - 编译正则表达式缓存

3. **增强功能**：
   - 流式处理大文件
   - 部分内容提取
   - 自定义修复规则

### 贡献指南

欢迎贡献！请：
1. Fork 仓库
2. 创建功能分支
3. 添加测试
4. 确保所有测试通过
5. 提交 Pull Request

## 参考资源

- [策略模式](https://refactoring.guru/design-patterns/strategy)
- [Python 类型注解](https://docs.python.org/3/library/typing.html)
- [Poetry 文档](https://python-poetry.org/docs/)
- [lxml 文档](https://lxml.de/)
