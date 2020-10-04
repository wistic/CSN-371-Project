use pyo3::{Python, PyResult};
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use std::fs::File;
use std::error::Error;
use std::io::{BufReader, BufWriter};

mod corpus;

#[pymodule]
fn corpusconverter(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pyfunction!(convert))?;
    Ok(())
}

#[pyfunction]
fn convert(src: String, des: String, low: bool) -> PyResult<bool> {
    match convert_rs(src, des, low) {
        Ok(_) => Ok(true),
        Err(_) => Ok(false),
    }
}

fn convert_rs(src: String, des: String, low: bool) -> Result<(), Box<dyn Error>> {
    let src = File::open(src)?;
    let des = File::create(des)?;
    corpus::corpus_convert(BufReader::new(src), BufWriter::new(des), low)?;
    Ok(())
}