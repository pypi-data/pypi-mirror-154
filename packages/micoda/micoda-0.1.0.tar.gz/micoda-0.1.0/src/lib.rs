use std::fs;
use std::collections::HashMap;

use pyo3::prelude::*;
use pulldown_cmark::{Parser, html, Options};

#[macro_use]
extern crate lazy_static;

lazy_static!(
    static ref PLUGINS: HashMap<&'static str, Options> = HashMap::from([
        ("tables", Options::ENABLE_TABLES),
        ("footnotes", Options::ENABLE_FOOTNOTES),
        ("strikethrough", Options::ENABLE_STRIKETHROUGH),
        ("tasklists", Options::ENABLE_TASKLISTS),
        ("smart_punctuation", Options::ENABLE_SMART_PUNCTUATION),
        ("heading_attributes", Options::ENABLE_HEADING_ATTRIBUTES)
    ]);
);

#[pyclass]
struct Markdown {
    options: Options
}

#[pymethods]
impl Markdown {
    // Generate `Markdown` with any plugins or without plugin.
    #[new]
    fn new(plugins: Option<Vec<&str>>) -> PyResult<Self> {
        if let Some(plugins) = plugins {
            let mut options = Options::empty();

            // Iterate over plugins and take corresponding `Option`
            for plugin_name in plugins.iter() {
                if let Some(option) = PLUGINS.get(plugin_name) {
                    options.insert(*option)
                }
            }

            return Ok(Self {
                options: options
            })
        } else {
            return Ok(Self {
                options: Options::empty()
            })
        }
    }

    // Convert Markdown to HTML.
    fn convert(&self, text: &str) -> PyResult<String> {
        let parser = Parser::new_ext(text, self.options);

        let mut output = String::new();
        html::push_html(&mut output, parser);
    
        Ok(output)
    }

    // Convert Markdown file to HTML.
    fn convert_file(&self, filename: &str) -> PyResult<String> {
        let content = fs::read_to_string(filename)?;

        self.convert(&content)
    }

    fn __call__(&self, text: &str) -> PyResult<String> {
        self.convert(text)
    }
}

// Create `Markdown` instance, the same as `Markdown()`.
#[pyfunction]
fn create_markdown(plugins: Option<Vec<&str>>) -> PyResult<Markdown> {
    let markdown = Markdown::new(plugins);

    markdown
}


// Convert Markdown to HTML(without plugin).
#[pyfunction]
fn convert(text: &str) -> PyResult<String> {
    let parser = Parser::new(text);

    let mut output = String::new();
    html::push_html(&mut output, parser);

    Ok(output)
}

// Convert Markdown file to HTML(without plugin).
#[pyfunction]
fn convert_file(filename: &str) -> PyResult<String> {
    let content = fs::read_to_string(filename)?;

    convert(&content)
}

/// A Python module implemented in Rust.
#[pymodule]
fn micoda(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert, m)?)?;
    m.add_function(wrap_pyfunction!(convert_file, m)?)?;
    m.add_function(wrap_pyfunction!(create_markdown, m)?)?;
    m.add_class::<Markdown>()?;
    Ok(())
}
