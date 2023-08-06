# Micoda

A Python module to parse Markdown. Powered by `PyO3` and `pulldown-cmark`.

## Install

```bash
pip install micoda
```

## Usage

Convert Markdown to HTML:

```python
import micoda

micoda.convert(your_markdown_text)
```

Convert Markdown file to HTML:

```python
import micoda

micoda.convert_file(your_markdown_file_path)
```
