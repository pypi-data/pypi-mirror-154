import pytest

import micoda
# pip install markdown
import markdown
# pip install mistune
import mistune
# pip install paka.cmark
# from paka import cmark


text = """# Title

> This is a blockquote.

## Ordered list

1. **First**
2. *Second*
3. Third

## Code

- Code block:

    ```python
    def main() -> None:
        print("Hello, world.")
    ```

- Span of code:

    `print(Hello, world.)`

## Links and Image

### Links

Go to [Github](https://github.com).  
Go to [Google][Google].

[Google]: https://www.google.com

---

### Image

Rust logo:

![Rust](https://www.rust-lang.org/static/images/rust-logo-blk.svg)

""" # noqa


@pytest.mark.benchmark(group='convert')
def test_markdown_convert(benchmark):
    md = markdown.Markdown()
    benchmark(md.convert, text)


@pytest.mark.benchmark(group='convert')
def test_mistune_convert(benchmark):
    md = mistune.create_markdown()
    benchmark(md.parse, text)


# @pytest.mark.benchmark(group='convert')
# def test_cmark_convert(benchmark):
#     benchmark(cmark.to_html, text)


@pytest.mark.benchmark(group='convert')
def test_micoda_convert(benchmark):
    benchmark(micoda.convert, text)
