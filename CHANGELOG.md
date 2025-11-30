# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.2] - 2025-11-30

### Fixed
- Fixed rendering issues in `README.md` for XML, HTML, and code extraction examples by refactoring nested code blocks.

## [1.0.1] - 2025-11-29

### Fixed
- Translated `CHANGELOG.md` and `docs/ARCHITECTURE.md` to English to align with the project's primary language.

## [1.0.0] - 2025-11-29

### Added
- Established version 1.0.0, providing stable and reliable core functionality for text extraction.

## [0.1.0] - 2025-01-29

### Added
- Initial release of llm-content-extractor
- Support for JSON extraction with fault tolerance
  - Handle markdown code fences (```json ... ```)
  - Extract JSON embedded in text
  - Fix trailing commas in JSON (common LLM error)
- Support for XML extraction
  - Handle markdown code fences
  - Extract XML from surrounding text
- Support for HTML extraction
  - Handle markdown code fences
  - Extract HTML fragments and full documents
- Support for code block extraction
  - Support language-specific extraction (e.g., Python, JavaScript)
  - Support generic code block extraction
- Strategy pattern architecture for extensibility
- Functional API with `extract()` function
- Custom extractor support via `ContentExtractor` base class
- Comprehensive test suite with high coverage
- Type annotations for all public APIs
- MIT License
- Documentation:
  - Comprehensive README with examples
  - Publishing guide for PyPI (docs/PUBLISHING.md)

[Unreleased]: https://github.com/aihes/llm-content-extractor/compare/v1.0.2...HEAD
[1.0.2]: https://github.com/aihes/llm-content-extractor/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/aihes/llm-content-extractor/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/aihes/llm-content-extractor/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/aihes/llm-content-extractor/releases/tag/v0.1.0
