# 发布到 PyPI 指南

本文档说明如何将 `llm-content-extractor` 包发布到 Python Package Index (PyPI)，以便其他用户可以通过 `pip install` 安装。

## 前置要求

1. **安装 Poetry**（如果尚未安装）：
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **注册 PyPI 账号**：
   - 访问 [https://pypi.org/account/register/](https://pypi.org/account/register/)
   - 完成注册流程
   - 启用双因素认证（2FA）以提高安全性

3. **创建 API Token**：
   - 登录 PyPI 后，访问 [https://pypi.org/manage/account/](https://pypi.org/manage/account/)
   - 滚动到 "API tokens" 部分
   - 点击 "Add API token"
   - 给 token 起个名字（如 "llm-content-extractor"）
   - 复制生成的 token（以 `pypi-` 开头）

## 配置 Poetry 认证

使用 API token 配置 Poetry：

```bash
poetry config pypi-token.pypi pypi-AgEIcHlwaS5vcmcC...
```

将上面的 token 替换为你自己的 API token。

## 发布流程

### 1. 更新版本号

在发布新版本之前，更新 `pyproject.toml` 中的版本号：

```bash
# 自动更新补丁版本号（0.1.0 -> 0.1.1）
poetry version patch

# 或更新次版本号（0.1.0 -> 0.2.0）
poetry version minor

# 或更新主版本号（0.1.0 -> 1.0.0）
poetry version major

# 或手动指定版本
poetry version 1.2.3
```

### 2. 更新 CHANGELOG

在 `CHANGELOG.md` 中记录本次版本的变更：

```markdown
## [0.1.1] - 2025-01-15

### Added
- 新增 XXX 功能

### Fixed
- 修复 XXX 问题

### Changed
- 改进 XXX 性能
```

### 3. 运行测试

确保所有测试通过：

```bash
poetry install
poetry run pytest
```

### 4. 构建发布包

```bash
poetry build
```

这将在 `dist/` 目录下创建两个文件：
- `llm_content_extractor-0.1.0-py3-none-any.whl`（wheel 格式）
- `llm_content_extractor-0.1.0.tar.gz`（源码包）

### 5. 发布到 TestPyPI（可选但推荐）

在发布到正式 PyPI 之前，建议先发布到 TestPyPI 进行测试：

```bash
# 配置 TestPyPI token
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config pypi-token.testpypi pypi-AgEIcHlwaS5vcmcC...

# 发布到 TestPyPI
poetry publish -r testpypi
```

测试安装：

```bash
pip install --index-url https://test.pypi.org/simple/ llm-content-extractor
```

### 6. 发布到 PyPI

确认一切正常后，发布到正式 PyPI：

```bash
poetry publish
```

### 7. 验证发布

访问包的 PyPI 页面验证发布成功：
```
https://pypi.org/project/llm-content-extractor/
```

测试安装：

```bash
pip install llm-content-extractor
```

### 8. 创建 Git Tag

为新版本创建 git tag：

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

## 自动化发布（GitHub Actions）

可以创建 GitHub Actions 工作流来自动化发布流程：

```yaml
# .github/workflows/publish.yml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install Poetry
        run: |
          curl -sSL https://install.python-poetry.org | python3 -

      - name: Build and publish
        env:
          POETRY_PYPI_TOKEN_PYPI: ${{ secrets.PYPI_API_TOKEN }}
        run: |
          poetry build
          poetry publish
```

在 GitHub 仓库设置中添加 secret `PYPI_API_TOKEN`。

## 常见问题

### 问题：发布失败，提示 "File already exists"

**解决方案**：PyPI 不允许重新上传相同版本的包。需要更新版本号后重新构建和发布。

### 问题：包名已被占用

**解决方案**：在 PyPI 上搜索确认包名是否可用。如果已被占用，需要在 `pyproject.toml` 中修改包名。

### 问题：依赖版本冲突

**解决方案**：检查 `pyproject.toml` 中的依赖版本范围是否合理，确保与常见的 Python 环境兼容。

## 版本管理建议

遵循 [语义化版本](https://semver.org/lang/zh-CN/)：

- **主版本号（Major）**：不兼容的 API 变更
- **次版本号（Minor）**：向后兼容的功能新增
- **修订号（Patch）**：向后兼容的问题修正

## 安全注意事项

1. **永远不要**将 API token 提交到代码仓库
2. 使用环境变量或 GitHub Secrets 存储敏感信息
3. 定期轮换 API tokens
4. 为不同项目使用不同的 tokens
5. 启用 PyPI 的双因素认证

## 撤回已发布的版本

如果发现严重问题，可以从 PyPI 移除版本：

1. 登录 PyPI
2. 进入项目管理页面
3. 选择要删除的版本
4. 点击 "Delete" 并确认

**注意**：删除后，该版本号不能再次使用。

## 参考资源

- [Poetry 官方文档 - Publishing](https://python-poetry.org/docs/cli/#publish)
- [PyPI 官方文档](https://pypi.org/help/)
- [Python 打包用户指南](https://packaging.python.org/)
- [语义化版本规范](https://semver.org/lang/zh-CN/)
